"""Code Search Engine for Python functions based on TF-IDF and cosine similarity."""

import os
import ast
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Function for parsing Python files
def parse_pyfiles(directory):
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
        # Skip virtual environment and site-packages directories
        if ".venv" in root or "site-packages" in root:
            continue

        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)

                # Use UTF-8 to correctly read .py files regardless of Windows default encoding
                with open(filepath, "r", encoding="utf-8") as f:
                    try:
                        file_content = f.read()
                        tree = ast.parse(file_content)

                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                func_name = node.name
                                docstring = ast.get_docstring(node) or ""
                                line_no = node.lineno
                                source = ast.get_source_segment(file_content, node) or ""

                                # Create searchable content
                                search_content = f"{func_name} {docstring} {source}"
                                data.append({
                                    "filepath": filepath,
                                    "func_name": func_name,
                                    "docstring": docstring,
                                    "line_no": line_no,
                                    "search_content": search_content
                                })
                    except Exception as e:
                        print(f"Error parsing {filepath}: {e}")
                        continue
    df = pd.DataFrame(data)
    return df


# Function for searching code
def search_functions(query, df):
    """
    Searches for the query string in the 'search_content' column of the DataFrame.
    Returns matching rows.
    """
    if df.empty:
        print("No data available to search. ")
        return pd.DataFrame()

    # TF-IDF vectorization for text similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df["search_content"])
    query_vector = vectorizer.transform([query])

    # Calculate similarity and return top matches
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    df["similarity_score"] = similarity_scores
    top_3_similar_functions = df.sort_values(by="similarity_score", ascending=False).head(3)
    return top_3_similar_functions


# Main execution
if __name__ == "__main__":
    code_dir = "code_base_for_testing(private)"
    df_functions = parse_pyfiles(code_dir)

    if df_functions.empty:
        print("No functions found in the specified directory.")
    else:
        print(f"{len(df_functions)} functions found in the specified directory.")

        # Main search loop
        while True:
            user_query = input("Enter your search query (or 'exit' to quit): ")

            if user_query.lower() == "exit":
                print("Exiting search engine. Goodbye!")
                break

            if not user_query.strip():
                continue

            matches = search_functions(user_query, df_functions)

            # Display search results
            found = False
            for _, row in matches.iterrows():
                if row["similarity_score"] > 0:
                    found = True
                    print(f"\nFile: {row['filepath']}")
                    print(f"Similarity Score: {row['similarity_score'] * 100:.2f}%")
                    print(f"Function: {row['func_name']} (Line {row['line_no']})")
                    print(f"Docstring: {row['docstring']}")

            if not found:
                print("No relevant functions found for your query.")

            print()
            print()
