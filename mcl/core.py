from collections import Counter
from pathlib import Path

import click
import libcst as cst
import tabulate
from libcst._nodes.statement import ImportFrom


class Visitor(cst.CSTVisitor):
    def __init__(self, user_defined_modules: set[str]) -> None:
        super().__init__()
        self.user_defined_modules = user_defined_modules
        self.count = {}

    def recursive_value(self, node) -> str:
        if isinstance(node, str):
            return node
        return self.recursive_value(node.value)

    def gain_count(self, package: str) -> None:
        if package not in self.count:
            self.count[package] = 0

        self.count[package] += 1

    def visit_Import(self, node: cst.CSTNode):
        for alias in node.names:
            package = self.recursive_value(alias.name.value)
            if package in self.user_defined_modules:
                continue

            self.gain_count(package)

    def visit_ImportFrom(self, node: ImportFrom) -> bool | None:
        if not hasattr(node.module, "value"):
            return
        package = self.recursive_value(node.module.value)

        if package in self.user_defined_modules:
            return
        self.gain_count(package)


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
    user_defined_modules = {
        str(file.parent.stem)
        for file in files
        if file.name in ("__main__.py", "__init__.py")
    }
    user_defined_modules.update({file.stem for file in files})
    counter = Counter()
    for file in files:
        try:
            node = cst.parse_module(file.read_text())
        except UnicodeDecodeError:
            continue
        visitor = Visitor(user_defined_modules)
        node.visit(visitor)
        counter.update(visitor.count)

    items = [(key, value) for key, value in counter.items()]
    items.sort(key=lambda x: x[1], reverse=True)
    print(tabulate.tabulate(items, ("packages", "count")))
