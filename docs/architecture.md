# Architecture Overview

HyperHelix is a powerful context management system organized around a graph of `Node` objects connected via weighted edges. Each node carries payload data and metadata about its creation and updates. The `HyperHelix` class manages these nodes and provides traversal helpers like `spiral_walk`.

Nodes and individual edges can be deleted via the API. Removing a node automatically drops all edges that reference it.
Edges connected to a specific node can also be retrieved using the `/edges/{id}` endpoint.
Simple operations such as creating or deleting resources return a standard `StatusOut` message to indicate success.
Subsystems include analytics for scoring nodes, evolution engines for automatic pruning and weaving, and persistence adapters for different databases. Event hooks respond to node updates, recalculating metrics or invoking custom tasks. A FastAPI-based API exposes graph operations, while a lightweight CLI and React front-end provide additional interfaces. The CLI can also query GitHub and send quick prompts to LLMs, including local Transformers models.

The evolution layer continuously maintains graph health by pruning edges to removed nodes and linking new nodes with similar tags. Execution results are stored in each node's metadata so future analysis can learn from past runs.
