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
    assert "Unknown command: foo" in result.stdout


def test_add():
    """Test the add command"""
    result = run_cli(["add"])
    assert result.returncode == 1
    assert "Usage: task-cli add <description>" in result.stdout

    result = run_cli(["add", '"Buy groceries"'])
    assert result.returncode == 0
    assert "Task added successfully (ID: 1)" in result.stdout

    result = run_cli(["add", '"Buy other groceries"'])
    assert result.returncode == 0
    assert "Task added successfully (ID: 2)" in result.stdout


def test_list():
    """Test the list command"""
    result = run_cli(["list"])
    assert result.returncode == 0
    assert "Buy groceries" in result.stdout
    assert "Buy other groceries" in result.stdout

    result = run_cli(["list", "todo"])
    assert result.returncode == 0
    assert "Buy groceries" in result.stdout
    assert "Buy other groceries" in result.stdout

    result = run_cli(["list", "foo"])
    assert result.returncode == 1
    assert "Unknown status: foo" in result.stdout


def main():
    pytest.main()


if __name__ == "__main__":
    main()
