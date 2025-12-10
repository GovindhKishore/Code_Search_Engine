import os
import ast

import pandas as pd


# PARSING AST FOR ALL PYTHON FILES IN A DIRECTORY
def parse__pyfiles(directory):
    """
    Walks through the directory, finds .py files, and extracts functions
    with their docstrings and line numbers using AST.
    """
    data = []

    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return pd.DataFrame()

    print("Scanning directory for Python files...")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)

                with open(filepath, "r", encoding="utf-8") as f: # use UTF-8 to correctly read .py files regardless of Windows default encoding
                    try:
                        file_content = f.read()
                        tree = ast.parse(file_content)

                        for node in ast.walk(tree):
                            if isinstance(node, ast.FuntionDef):
                                func_name = node.name
                                docstring = ast.get_docstring(node) or ""
                                line_no = node.lineno

                                search_content = f"{func_name}: {docstring}"
                                data.append({
                                    "filepath": filepath,
                                    "function_name": func_name,
                                    "docstring": docstring,
                                    "line_no": line_no,
                                    "search_content": search_content
                                })
                    except Exception as e:
                        print(f"Error parsing {filepath}: {e}")
                        continue

