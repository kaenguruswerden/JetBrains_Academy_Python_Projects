import re
import os
import argparse
import string
import ast


class CodeAnalyzer:
    """A class to check the code in a file for errors."""

    ERRORS = {"S001": "Too long",
              "S002": "Indentation is not a multiple of four",
              "S003": "Unnecessary semicolon after a statement",
              "S004": "Less than two spaces before inline comment",
              "S005": "TODO found",
              "S006": "More than two blank lines used before this line",
              "S007": "Too many spaces after \"$name\"",
              "S008": "Class name \"$name\" should be written in CamelCase",
              "S009": "Function name \"$name\" should be written in snake_case",
              "S010": "Argument name \"$name\" should be written in snake_case",
              "S011": "Variable \"$name\" should be written in snake_case",
              "S012": "The default argument value is mutable"}

    PATTERNS = {"snake_case_func": re.compile(r"^_{0,2}[^A-Z^_]+?(_?[^A-Z^_])*?_{0,2}$"),
                "snake_case_var": re.compile(r"^_{0,2}[^A-Z^_]+?(_?[^A-Z^_])*?$"),
                "CamelCase": re.compile(r"^([A-Z][a-z\d]+)+$")}

    def __init__(self, code_file_path):
        self.path = code_file_path
        self.code_file_path = os.path.join(os.path.abspath(__file__), "..\\..\\", self.path)
        self.errors_found = {}
        self.tree = None

    def analyze_code(self) -> None:
        """Analyze the code of a file."""
        file = open(self.code_file_path, "r")
        code = file.read()
        file.close()
        self.tree = ast.parse(code)

        with open(self.code_file_path, "r") as code_file:
            previous_blank_lines = 0
            for i, line in enumerate(code_file, start=1):
                self._check_line_length(line, i, "S001")
                self._check_indentation(line, i, "S002")
                self._check_semicolons(line, i, "S003")
                self._check_spaces_inline_comments(line, i, "S004")
                self._check_todo_found(line, i, "S005")
                previous_blank_lines = self._check_blank_line(line, i, "S006", previous_blank_lines)
                self._check_construction_spaces(line, i, "S007")
            self._check_class_name("S008")
            self._check_function_name("S009")
            self._check_arg_name("S010")
            self._check_var_name("S011")
            self._check_default_arg_mutable("S012")

    def print_errors(self):
        """Print all the errors found and stored in self.errors_found.

        Format: path: line line_nr: error_code error_msg"""
        for key in sorted(list(self.errors_found.keys())):
            for error in self.errors_found[key]:
                if len(error) == 1:
                    print(f"{self.path}: Line {key}: {error[0]} {self.ERRORS[error[0]]}")
                else:
                    template = string.Template(self.ERRORS[error[0]])
                    msg = template.substitute(name=error[1])
                    print(f"{self.path}: Line {key}: {error[0]} {msg}")

    def _check_line_length(self, line: str, i: int, error_code) -> None:
        """Add an error if a line is longer than 79 characters."""
        if len(line) > 79:
            self._add_error(i, error_code)
    
    def _check_indentation(self, line: str, i: int, error_code) -> None:
        """Add an error if an indentation is not a multiple of four."""
        if not re.match(r"^( {4})*[^ ]", line):
            self._add_error(i, error_code)

    def _check_semicolons(self, line: str, i: int, error_code) -> None:
        """Add an error if an unnecessary semicolon is found."""
        if ";" in line:
            line = line.split(";")
            if "#" not in line[0] and line[0].count("'") % 2 == 0:
                self._add_error(i, error_code)

    def _check_spaces_inline_comments(self, line: str, i: int, error_code) -> None:
        """Add an error there are less than two spaces before an inline comment."""
        if re.search(r"^[^#]+(?<=[^ ]) ?#", line):
            self._add_error(i, error_code)

    def _check_todo_found(self, line: str, i: int, error_code) -> None:
        """Add an error if a "TODO" is found (not case sensitive)."""
        if re.search(r"^[^#]*#.*?todo", line, flags=re.IGNORECASE):
            self._add_error(i, error_code)

    def _check_blank_line(self, line: str, i: int, error_code, previous_blank_lines: int) -> int:
        """Return the number of previous blank lines.
        Add an error if a non-blank line has more than two previous blank lines."""
        if re.match(r"^\n$", line):
            previous_blank_lines += 1
        elif previous_blank_lines > 2:
            self._add_error(i, error_code)
            previous_blank_lines = 0
        else:
            previous_blank_lines = 0
        return previous_blank_lines

    def _check_construction_spaces(self, line: str, i: int, error_code) -> None:
        """Add en error with the function or class constructor if there are more or less than one space."""
        if re.search(r"(?<=class ) ", line):
            self._add_error(i, error_code, "class")
        elif re.search(r"(?<=def ) ", line):
            self._add_error(i, error_code, "def")

    def _check_class_name(self, error_code) -> None:
        """Add an error with the class' name if a class' name is not written in CamelCase."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                if not re.match(self.PATTERNS["CamelCase"], node.name):
                    self._add_error(node.lineno, error_code, node.name)

    def _check_function_name(self, error_code) -> None:
        """Add an error with the function's name if a function's name is not written in snake_case."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(self.PATTERNS["snake_case_func"], node.name):
                    self._add_error(node.lineno, error_code, node.name)

    def _check_arg_name(self, error_code) -> None:
        """Add an error with the argument's name if an argument's name is not written in snake_case."""
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            for arg in node.args.args:
                if not re.match(self.PATTERNS["snake_case_var"], arg.arg):
                    self._add_error(node.lineno, error_code, arg.arg)

    def _check_var_name(self, error_code) -> None:
        """Add an error with the variable's name if a variable's name is not written in snake_case."""
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Assign):
                continue
            for name in node.targets:
                if not isinstance(name, ast.Name):
                    continue
                if not re.match(self.PATTERNS["snake_case_var"], name.id):
                    self._add_error(node.lineno, error_code, name.id)

    def _check_default_arg_mutable(self, error_code) -> None:
        """Add an error if a mutable default argument is found."""
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            
            for el in node.args.defaults:
                if not (isinstance(el, ast.List) or isinstance(el, ast.Set) or isinstance(el, ast.Dict)):
                    continue

                if node.lineno not in list(self.errors_found.keys()):
                    self._add_error(node.lineno, error_code)

                if not [error_code] in self.errors_found[node.lineno]:
                    self._add_error(node.lineno, error_code)

    def _add_error(self, line_nr: int, error_code: str, value_name: str = None) -> None:
        """Create and add an error to self.errors_found.

        :param line_nr: An int representing the line number.
        :param error_code: A string representing the error code.
        :param value_name : (Optional) A string representing the name of a value. Defaults to None.
        """
        if value_name is None:
            self.errors_found.setdefault(line_nr, []).append([error_code])
        else:
            self.errors_found.setdefault(line_nr, []).append([error_code])
            index = self._get_index(line_nr, error_code)
            self.errors_found[line_nr][index].append(value_name)

    def _get_index(self, key: int, error_code: str) -> int:
        """Return index of error_code in self.errors_found[key]."""
        for element in self.errors_found[key]:
            if error_code in element:
                return self.errors_found[key].index(element)
        else:
            raise ValueError(f"{error_code} not in self.errors_found[{key}]")

    def __repr__(self):
        return f"CodeAnalyzer(code_file_path={self.path})"


def parse_args() -> str:
    """Return the parsed argument."""
    parser = argparse.ArgumentParser()
    parser.add_argument("directory_or_file_path", help="The path to a directory \
    that contains the python files you want to analyze.")
    args = parser.parse_args()
    path = args.directory_or_file_path

    return path


def main():

    # Get a relative path to a file or a directory from argument
    path = parse_args()

    # # for testing
    # if path == "test_file.py":
    #     path = os.path.join("analyzer", path)
    #     code_analyzer = CodeAnalyzer(path)
    #     code_analyzer.analyze_code()
    #     code_analyzer.print_errors()

    # Get the absolute path to the file/directory
    abs_path = os.path.join(os.path.abspath(__file__), "..\\..\\", path)

    if os.path.isfile(abs_path):
        code_analyzer = CodeAnalyzer(path)
        code_analyzer.analyze_code()
        code_analyzer.print_errors()

    # If the path is for a directory, analyze the code of every python file it contains
    elif os.path.isdir(abs_path):
        files = os.listdir(abs_path)
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(path, file)
                code_analyzer = CodeAnalyzer(file_path)
                code_analyzer.analyze_code()
                code_analyzer.print_errors()


if __name__ == "__main__":
    main()
