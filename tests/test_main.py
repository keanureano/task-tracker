import os
import pytest
import subprocess


@pytest.fixture(autouse=True)
def set_test_env():
    """Helper function to set test environment variables"""
    os.environ["DATABASE"] = "test_database.json"

    yield
    # Cleanup
    DATABASE = os.getenv("DATABASE")

    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    del os.environ["DATABASE"]


def run_cli(args):
    """Helper function to run task-cli with given args"""
    result = subprocess.run(["task-cli"] + args, capture_output=True, text=True)
    print(result.stdout)
    return result


def test_cli_empty():
    """Test the empty command"""
    result = run_cli([])
    assert result.returncode == 1
    assert "Usage: task-cli <command> [options]" in result.stdout


def test_cli_add():
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


def main():
    pytest.main()


if __name__ == "__main__":
    main()
