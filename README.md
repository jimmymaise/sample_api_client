# Sample API Client

This is a Python-based API client designed for interacting with the Jimmy Mai API. The client provides an intuitive and straightforward way to make API calls and manage responses.

## Features

- **Asynchronous API calls**: Utilizes `httpx` for non-blocking API requests.
- **Data Modeling**: Uses `pydantic` for robust data structures.
- **Automatic Case Conversion**: Converts between `snake_case` and `camelCase` automatically.
- **Pagination Support**: Handles pagination for API endpoints that return multiple items.

## Dependencies

This project is dependent on the following packages:

- Python 3.11
- pyhumps 3.8.0
- pydantic 2.0.3
- requests 2.31.0
- httpx 0.24.1

## Usage

### ApiClient Class

The `ApiClient` class is your main interface for making API requests. It comes with `get` and `post` methods for performing GET and POST operations, respectively.

### CandidateManager Class

The `CandidateManager` class offers various methods for managing candidates. This includes retrieving a candidate by their ID, creating new candidates, and updating existing ones.

### Note and Document Classes

Classes `Note` and `Document` are designed to manage notes and documents related to a candidate. They offer methods for retrieval and insertion of notes and documents.

## Examples

Refer to `main.py` for practical examples demonstrating how to use this API client.

## Running the Project

To run the project, execute the following command:

```python main.py```

## Inspiration

The design of this API client is inspired by the [python-gitlab](https://github.com/python-gitlab/python-gitlab) project. It follows similar design philosophies and patterns, including the utilization of manager classes for different types of resources.
