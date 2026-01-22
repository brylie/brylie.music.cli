import pytest
from click.testing import CliRunner
from src.main import cli

def test_wizard():
    runner = CliRunner()
    result = runner.invoke(cli, ['wizard'], input='John\nDoe\n')
    assert result.exit_code == 0
    assert 'John Doe' in result.output
