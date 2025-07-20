# Architecture Overview

HelixHyper is organized around a graph of `Node` objects connected via weighted edges. Each node carries payload data and metadata about its creation and updates. The `HyperHelix` class manages these nodes and provides traversal helpers like `spiral_walk`.

Subsystems include analytics for scoring nodes, evolution engines for automatic pruning and weaving, and persistence adapters for different databases. Event hooks respond to node updates, recalculating metrics or invoking custom tasks. A FastAPI-based API exposes graph operations, while a lightweight CLI and React front-end provide additional interfaces.

The evolution layer continuously maintains graph health by pruning edges to removed nodes and linking new nodes with similar tags. Execution results are stored in each node's metadata so future analysis can learn from past runs.
