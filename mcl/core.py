from pathlib import Path

import click
import git
import libcst as cst
from libcst._nodes.statement import ImportFrom


class Visitor(cst.CSTVisitor):
    def __init__(self, files: list[str]) -> None:
        super().__init__()
        self.files = files

    def visit_Import(self, node: cst.CSTNode):
        for alias in node.names:
            if alias.name.value in self.files:
                continue
            print(alias.name.value)

    def visit_ImportFrom(self, node: ImportFrom) -> bool | None:
        if node.module.value in self.files:
            return
        print(node.module.value)


def is_ignored_folder(path, ignored_folders):
    return any(folder in path.parts for folder in ignored_folders)


def get_ignored_folders():
    return "venv", "__pycache__"


@click.command(name="")
def main():
    """
    Get the most commonly used libraries in a given directory

    [NOTE: Current directory by default]
    """

    current_directory = Path()
    ignored_folders = get_ignored_folders()
    files = [
        file
        for file in current_directory.rglob("*.py")
        if not is_ignored_folder(file, ignored_folders)
    ]

    for file in files:
        node = cst.parse_module(file.read_text())
        node.visit(Visitor([file.stem for file in files]))
