from setuptools import find_packages, setup

setup(
    name="task-cli",
    version="1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["task-cli=main:main"]},
)
