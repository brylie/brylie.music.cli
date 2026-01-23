import pytest
from click.testing import CliRunner
from main import cli
from unittest.mock import patch
from models import ProjectMetadata

def test_wizard():
    runner = CliRunner()
    result = runner.invoke(cli, ['wizard'], input='John\nDoe\n')
    assert result.exit_code == 0
    assert 'John Doe' in result.output

@patch('main.add_tasks_to_project')
@patch('main.load_tasks')
@patch('main.create_project_fields')
@patch('main.create_project')
def test_create_project_cmd(mock_create_project, mock_create_fields, mock_load_tasks, mock_add_tasks):
    # Setup mock return value
    mock_project = ProjectMetadata(
        id="PVT_kwDO...",
        project_number=1,
        project_url="https://github.com/orgs/me/projects/1",
        title="My Album",
        owner="@me",
        field_ids={}
    )
    mock_create_project.return_value = mock_project
    
    # Mock task list
    mock_load_tasks.return_value.tasks = []

    runner = CliRunner()
    result = runner.invoke(cli, ['create-project'], input='My Album\n')
    
    assert result.exit_code == 0
    assert "Release title: My Album" in result.output
    assert "Project created successfully: https://github.com/orgs/me/projects/1" in result.output
    assert "Creating custom fields..." in result.output
    assert "Loading and creating tasks..." in result.output
    
    mock_create_project.assert_called_once_with(title="My Album", dry_run=False)
    mock_create_fields.assert_called_once_with(project_number=1, owner="@me")
    mock_add_tasks.assert_called_once()

@patch('main.add_tasks_to_project')
@patch('main.load_tasks')
@patch('main.create_project_fields')
@patch('main.create_project')
def test_create_project_cmd_dry_run(mock_create_project, mock_create_fields, mock_load_tasks, mock_add_tasks):
    mock_create_project.return_value = None
    mock_load_tasks.return_value.tasks = []

    runner = CliRunner()
    result = runner.invoke(cli, ['create-project', '--dry-run'], input='My Album\n')
    
    assert result.exit_code == 0
    assert "Dry run complete." in result.output
    
    mock_create_project.assert_called_once_with(title="My Album", dry_run=True)
    mock_create_fields.assert_called_once_with(project_number=0, dry_run=True)
    mock_add_tasks.assert_called_once()