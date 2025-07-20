from __future__ import annotations

from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    @abstractmethod
    def save_node(self, node_id: str, payload: dict) -> None: ...

    @abstractmethod
    def load_node(self, node_id: str) -> dict: ...

    @abstractmethod
    def save_edge(self, a: str, b: str, weight: float) -> None: ...

    @abstractmethod
    def load_edges(self, node_id: str) -> dict[str, float]: ...
