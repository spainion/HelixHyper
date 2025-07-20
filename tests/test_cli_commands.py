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
