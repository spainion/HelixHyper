import builtins
from click.testing import CliRunner
import types

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
