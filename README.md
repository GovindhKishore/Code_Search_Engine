# Python Code Search Engine

A powerful search engine for Python functions based on TF-IDF and cosine similarity. This tool helps you find relevant functions in your Python codebase by searching through function names, docstrings, and source code.

## Features

- Parses Python files to extract functions with their docstrings and line numbers
- Uses TF-IDF vectorization and cosine similarity for intelligent searching
- Ranks search results by relevance
- Displays top matches with similarity scores
- Skips virtual environments and site-packages directories

## Installation

### Prerequisites

- Python 3.6 or higher
- Git

### Steps

1. Clone the repository:
   ```
   git clone https://github.com/GovindhKishore/Code_Search_Engine
   cd Code_Search_Engine
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Place the directory you want to search in the `codebase` directory. 

2. Run the search engine:
   ```
   python search_engine.py
   ```

3. Enter your search queries when prompted. The engine will display the most relevant functions based on your query.

4. Type `exit` to quit the search engine.

## How It Works

The search engine works in two main steps:

1. **Parsing Phase**: The `parse_pyfiles()` function walks through the specified directory, finds all Python files, and extracts functions along with their docstrings and line numbers using Python's Abstract Syntax Tree (AST) module.

2. **Search Phase**: The `search_functions()` function uses TF-IDF (Term Frequency-Inverse Document Frequency) vectorization to convert the function content into numerical vectors. It then calculates the cosine similarity between the query vector and all function vectors to find the most relevant matches.

## Example

```
Enter your search query (or 'exit' to quit): predict app success

File: code_base_for_testing/App_Success_Predictor/predict.py
Similarity Score: 78.45%
Function: predict_app_success (Line 15)
Docstring: Predicts the success rate of a mobile application based on various features.
```

## Requirements

- pandas ~= 2.3.3
- scikit-learn ~= 1.8.0

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.