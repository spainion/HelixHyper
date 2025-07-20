# Advanced Evolution

Event-driven evolution hooks allow the graph to adjust itself whenever nodes or edges change. Customize the `evented_engine` module to prune outdated nodes or introduce new connections automatically.

The default implementation now performs several actions:

- **Metric updates** recalculate importance and permanence on inserts and updates.
- **Tag weaving** connects a newly inserted node to existing nodes that share tags.
- **Pruning** removes edges pointing to nodes that no longer exist, keeping the graph healthy.
