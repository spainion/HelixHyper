# Architecture Overview

HelixHyper is organized around a graph of `Node` objects connected via weighted edges. Each node carries payload data and metadata about its creation and updates. The `HyperHelix` class manages these nodes and provides traversal helpers like `spiral_walk`.

Subsystems include analytics for scoring nodes, evolution engines for automatic pruning and weaving, and persistence adapters for different databases. A FastAPI-based API exposes graph operations, while a lightweight CLI and React front-end provide additional interfaces.
