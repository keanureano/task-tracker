import os
import pytest
import subprocess


@pytest.fixture(scope="session", autouse=True)
def setup_env():
    """Sets up the test environment"""
    # Setup before the test
    os.environ["DATABASE"] = "./tests/test_database.json"
    DATABASE = os.getenv("DATABASE")

    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    yield

    # Clean up after the test
    del os.environ["DATABASE"]


def run_cli(args):
    """Helper function to run task-cli with given args"""
    result = subprocess.run(["task-cli"] + args, capture_output=True, text=True)
    print(result.stdout)
    return result


def test_cli():
    """Test the base cli commands"""
    result = run_cli([])
    assert result.returncode == 1
    assert "Usage: task-cli <command> [options]" in result.stdout

    result = run_cli(["foo"])
    assert result.returncode == 1
    assert "Usage: task-cli <command> [options]" in result.stdout


def test_add():
    """Test the add command"""
    result = run_cli(["add"])
    assert result.returncode == 1
    assert "Usage: task-cli add <description>" in result.stdout

    result = run_cli(["add", "Buy groceries"])
    assert result.returncode == 0
    assert "Task added successfully (ID: 1)" in result.stdout

    result = run_cli(["add", "Go to the gym"])
    assert result.returncode == 0
    assert "Task added successfully (ID: 2)" in result.stdout

    result = run_cli(["add", "Clean the house"])
    assert result.returncode == 0
    assert "Task added successfully (ID: 3)" in result.stdout

    result = run_cli(["add", "Cook dinner"])
    assert result.returncode == 0
    assert "Task added successfully (ID: 4)" in result.stdout


def test_update():
    """Test the update command"""
    result = run_cli(["update"])
    assert result.returncode == 1
    assert "Usage: task-cli update <id> <description>" in result.stdout

    result = run_cli(["update", "99", "Foo"])
    assert result.returncode == 1
    assert "Task not found (ID: 99)" in result.stdout

    result = run_cli(["update", "1"])
    assert result.returncode == 1
    assert "Usage: task-cli update <id> <description>" in result.stdout

    result = run_cli(["update", "1", "Buy groceries and cook dinner"])
    assert result.returncode == 0
    assert "Task updated successfully (ID: 1)" in result.stdout


def test_delete():
    """Test the delete command"""
    result = run_cli(["delete"])
    assert result.returncode == 1
    assert "Usage: task-cli delete <id>" in result.stdout

    result = run_cli(["delete", "99"])
    assert result.returncode == 1
    assert "Task not found (ID: 99)" in result.stdout

    result = run_cli(["delete", "4"])
    assert result.returncode == 0
    assert "Task deleted successfully (ID: 4)" in result.stdout


def test_mark():
    """Test the mark command"""
    result = run_cli(["mark"])
    assert result.returncode == 1
    assert "Usage: task-cli mark-<status> <id>" in result.stdout

    result = run_cli(["mark-"])
    assert result.returncode == 1
    assert "Usage: task-cli mark-<status> <id>" in result.stdout

    result = run_cli(["mark-foo", "99"])
    assert result.returncode == 1
    assert "Task not found (ID: 99)" in result.stdout

    result = run_cli(["mark-done", "1"])
    assert result.returncode == 0
    assert "Task marked as done successfully (ID: 1)" in result.stdout

    result = run_cli(["mark-todo", "2"])
    assert result.returncode == 0
    assert "Task marked as todo successfully (ID: 2)" in result.stdout

    result = run_cli(["mark-in-progress", "3"])
    assert result.returncode == 0
    assert "Task marked as in-progress successfully (ID: 3)" in result.stdout


def test_list():
    """Test the list command"""
    result = run_cli(["list", "foo"])
    assert result.returncode == 1
    assert "Unknown status: foo" in result.stdout
    assert "Usage: task-cli list <status>" in result.stdout

    result = run_cli(["list"])
    assert result.returncode == 0
    assert "[done] 1: Buy groceries and cook dinner" in result.stdout
    assert "[todo] 2: Go to the gym" in result.stdout
    assert "[in-progress] 3: Clean the house" in result.stdout

    result = run_cli(["list", "done"])
    assert result.returncode == 0
    assert "[done] 1: Buy groceries and cook dinner" in result.stdout

    result = run_cli(["list", "in-progress"])
    assert result.returncode == 0
    assert "[in-progress] 3: Clean the house" in result.stdout

    result = run_cli(["list", "todo"])
    assert result.returncode == 0
    assert "[todo] 2: Go to the gym" in result.stdout


def test_help():
    """Test the help command"""
    result = run_cli(["help"])
    assert result.returncode == 0
    assert "Usage: task-cli <command> [options]" in result.stdout


def main():
    pytest.main()


if __name__ == "__main__":
    main()
