from hyperhelix.core import HyperHelix
from hyperhelix.agents.chat_adapter import handle_chat_message
from hyperhelix.agents.llm import BaseChatModel

class DummyModel(BaseChatModel):
    def generate_response(self, messages):
        return "reply"

def test_handle_chat_message_with_model():
    graph = HyperHelix()
    handle_chat_message(graph, "hi", DummyModel())
    assert "hi" in graph.nodes
    assert "response:hi" in graph.nodes
