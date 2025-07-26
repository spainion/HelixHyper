"""Command parser for interactive commands used in tests.

This CLI recognises a handful of prefixed commands used in the unit
tests.  Commands beginning with ``!python`` execute arbitrary Python
code using the configured execution manager.  ``!script`` looks up
a named script module and invokes its ``run`` function.  ``!agent``
instantiates a registered agent and calls its ``act`` method with the
remainder of the line.  ``!task`` manages a list of tasks in the
query manager's task manager.  ``!save``, ``!load`` and
``!load_backup`` persist and restore the current graph via the
persistence layer and report the number of nodes loaded.  ``!version``
returns the graph's version string.  ``!scripts`` and ``!agents``
print the available names from the provided discovery mappings.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from pathlib import Path

from memory import persistence


def handle_command(
    command: str,
    manager: Any,
    context1: Optional[Dict[str, Any]] = None,
    context2: Optional[Dict[str, Any]] = None,
) -> str:
    """Parse and dispatch a single command string.

    :param command: the user command beginning with an exclamation mark
    :param manager: a :class:`QueryManager` providing access to graph,
        task manager and execution manager
    :param context1: optional mapping of script names to modules
    :param context2: optional mapping of agent names to classes
    :returns: a result string for the executed command
    """
    # Determine script and agent mappings based on which contexts are provided.
    # Many tests pass only a single mapping (e.g. agents for !agent) so we
    # treat context1 as the primary mapping and context2 as secondary.  For
    # script commands we prefer context1, and for agent commands we
    # prefer context2 if present, falling back to context1 otherwise.
    scripts_map = context1 or {}
    agents_map = context2 if context2 is not None else (context1 or {})

    cmd = command.strip()
    # !python <code>
    if cmd.startswith("!python "):
        code = cmd[len("!python ") :]
        return manager.executor.execute("python", code)
    # !script <name>
    if cmd.startswith("!script "):
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            return "Missing script name"
        name = parts[1].strip()
        # Use the scripts mapping; if not provided fall back to agents_map as a last resort
        module = scripts_map.get(name) if scripts_map else agents_map.get(name)
        if not module:
            return f"Script {name} not found"
        # run() may accept list of args; we pass empty list
        # Call the module's run function.  It may either return a string
        # or print to stdout; the tests expect a string or other simple type.
        result = module.run([])  # type: ignore[misc]
        return result if isinstance(result, str) else str(result)
    # !agent <name> <args>
    if cmd.startswith("!agent "):
        parts = cmd.split(maxsplit=2)
        if len(parts) < 2:
            return "Missing agent name"
        name = parts[1]
        payload = parts[2] if len(parts) > 2 else ""
        # Select the agent mapping: use context2 if provided, otherwise context1
        cls = agents_map.get(name)
        if not cls:
            return f"Agent {name} not found"
        agent = cls()
        # assume agent has an act() method taking a string
        result = agent.act(payload)
        return result if isinstance(result, str) else str(result)
    # !task operations
    if cmd.startswith("!task "):
        sub = cmd[len("!task ") :].strip()
        if sub.startswith("create "):
            desc = sub[len("create ") :]
            task_id = manager.task_manager.create(desc)
            return f"Created task {desc} {task_id}"
        if sub == "list":
            return manager.task_manager.list_tasks()
        if sub.startswith("done "):
            tid = sub[len("done ") :]
            if manager.task_manager.complete(tid):
                return f"Task {tid} marked done"
            return f"Task {tid} not found"
        return "Unknown task command"
    # !save <path>
    if cmd.startswith("!save "):
        path = cmd[len("!save ") :].strip()
        persistence.save(manager.graph, path)
        return f"Saved graph to {path}"
    # !load_backup <path>
    if cmd.startswith("!load_backup "):
        path = cmd[len("!load_backup ") :].strip()
        # determine backup path for message
        p = Path(path)
        if p.suffix == ".json":
            backup = p.with_suffix(p.suffix + ".bak")
        else:
            backup = p.with_name(p.name + ".bak")
        manager.graph = persistence.load_backup(path)
        count = len(manager.graph.nodes)
        return f"Loaded {count} nodes from {backup}"
    # !load <path>
    if cmd.startswith("!load "):
        path = cmd[len("!load ") :].strip()
        manager.graph = persistence.load(path)
        count = len(manager.graph.nodes)
        return f"Loaded {count} nodes from {path}"
    # !version
    if cmd == "!version":
        return manager.graph.version
    # !scripts lists available script names
    if cmd == "!scripts":
        # Print discovered script names.  Prefer the scripts mapping but fall back to agents_map
        names = scripts_map.keys() if scripts_map else agents_map.keys()
        return "\n".join(sorted(names))
    # !agents lists available agent names
    if cmd == "!agents":
        # Print discovered agent names.  Prefer the agents mapping but fall back to scripts_map
        names = agents_map.keys() if agents_map else scripts_map.keys()
        return "\n".join(sorted(names))
    return "Unknown command"