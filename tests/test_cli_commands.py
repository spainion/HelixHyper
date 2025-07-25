from click.testing import CliRunner
from hyperhelix.core import HyperHelix

from hyperhelix.cli import commands


def test_cli_serve(monkeypatch):
    called = {}
    def fake_run(app, host='0.0.0.0', port=8000):
        called['args'] = (app, host, port)
    monkeypatch.setattr('uvicorn.run', fake_run)
    runner = CliRunner()
    result = runner.invoke(commands.cli, ['serve'])
    assert result.exit_code == 0
    assert called['args'][0] == 'hyperhelix.api.main:app'


def test_cli_scan(tmp_path, monkeypatch):
    path = tmp_path / 'x.py'
    path.write_text('print("x")')
    from hyperhelix.api import main
    main.app.state.graph = HyperHelix()
    runner = CliRunner()
    result = runner.invoke(commands.cli, ['scan', str(tmp_path)])
    assert result.exit_code == 0
    assert f'file:{path.name}' in main.app.state.graph.nodes


def test_cli_issues(monkeypatch):
    def fake_get(url, headers=None, timeout=10):
        class Resp:
            def raise_for_status(self):
                pass

            def json(self):
                return [{"number": 1, "title": "demo"}]

        fake_get.called_url = url
        return Resp()

    monkeypatch.setattr("httpx.get", fake_get)
    runner = CliRunner()
    result = runner.invoke(commands.cli, ["issues", "owner/repo"])
    assert result.exit_code == 0
    assert "#1: demo" in result.output
    assert fake_get.called_url == "https://api.github.com/repos/owner/repo/issues"


def test_cli_codex(monkeypatch):
    class FakeModel:
        def __init__(self, *a, **kw):
            pass

        def generate_response(self, messages):
            return "pong"

    monkeypatch.setattr("hyperhelix.agents.llm.OpenRouterChatModel", FakeModel)
    runner = CliRunner()
    result = runner.invoke(commands.cli, ["codex", "ping"])
    assert result.exit_code == 0
    assert "pong" in result.output


def test_cli_codex_local(monkeypatch):
    class FakeModel:
        def __init__(self, *a, **kw):
            pass

        def generate_response(self, messages):
            return "loc"

    monkeypatch.setattr("hyperhelix.agents.llm.TransformersChatModel", FakeModel)
    runner = CliRunner()
    result = runner.invoke(commands.cli, ["codex", "hello", "--provider", "local"])
    assert result.exit_code == 0
    assert "loc" in result.output


def test_cli_codex_stream(monkeypatch):
    class FakeModel:
        def __init__(self, model="openai/gpt-4o", api_key=None):
            FakeModel.used_model = model

        def stream_response(self, messages):
            return "stream"

    monkeypatch.setattr("hyperhelix.agents.llm.OpenRouterChatModel", FakeModel)
    runner = CliRunner()
    result = runner.invoke(
        commands.cli,
        ["codex", "ping", "--stream", "--model", "foo-model"],
    )
    assert result.exit_code == 0
    assert "stream" in result.output
    assert FakeModel.used_model == "foo-model"


def test_cli_models_openrouter(monkeypatch):
    monkeypatch.setattr(
        "hyperhelix.agents.llm.list_openrouter_models",
        lambda api_key=None: ["a", "b"],
    )
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    runner = CliRunner()
    result = runner.invoke(commands.cli, ["models", "--provider", "openrouter"])
    assert result.exit_code == 0
    assert "a" in result.output


def test_cli_models_huggingface(monkeypatch):
    monkeypatch.setattr(
        "hyperhelix.agents.llm.list_huggingface_models",
        lambda search="gpt2", limit=5: ["hf"],
    )
    runner = CliRunner()
    result = runner.invoke(
        commands.cli,
        ["models", "--provider", "huggingface", "--query", "gpt2", "--limit", "1"],
    )
    assert result.exit_code == 0
    assert "hf" in result.output
