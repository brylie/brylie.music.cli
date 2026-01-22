import pytest
from click.testing import CliRunner
from src.main import cli
from unittest.mock import patch
from src.models import ProjectMetadata

def test_wizard():
    runner = CliRunner()
    result = runner.invoke(cli, ['wizard'], input='John\nDoe\n')
    assert result.exit_code == 0
    assert 'John Doe' in result.output

@patch('src.main.create_project')
def test_create_project_cmd(mock_create_project):
    # Setup mock return value
    mock_project = ProjectMetadata(
        project_number=1,
        project_url="https://github.com/orgs/me/projects/1",
        title="My Album",
        owner="@me",
        field_ids={}
    )
    mock_create_project.return_value = mock_project

    runner = CliRunner()
    result = runner.invoke(cli, ['create-project'], input='My Album\n')
    
    assert result.exit_code == 0
    assert "Release title: My Album" in result.output
    assert "Project created successfully: https://github.com/orgs/me/projects/1" in result.output
    
    mock_create_project.assert_called_once_with(title="My Album", dry_run=False)

@patch('src.main.create_project')
def test_create_project_cmd_dry_run(mock_create_project):
    mock_create_project.return_value = None

    runner = CliRunner()
    result = runner.invoke(cli, ['create-project', '--dry-run'], input='My Album\n')
    
    assert result.exit_code == 0
    assert "Dry run complete." in result.output
    
    mock_create_project.assert_called_once_with(title="My Album", dry_run=True)