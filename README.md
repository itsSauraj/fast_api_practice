# FastAPI Small Project

This project is a small practice application using FastAPI. It demonstrates the basic setup and functionality of a FastAPI application.

## Features

- Basic FastAPI setup
- Example endpoints
- CORS configuration for testing with a React app

## React App

A simple React app is included in this project. Please note that this React app is not fully detailed and is only created for the purpose of testing CORS (Cross-Origin Resource Sharing) with the FastAPI backend.

## Getting Started

### Prerequisites

- Python 3.7+
- FastAPI
- React

### Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/itsSauraj/fast_api_practice.git
  ```
2. Navigate to the project directory:
  ```bash
  cd fast_api_practice
  ```
3. Install the required Python packages:
  ```bash
  pip install -r requirements.txt
  ```

### Running the FastAPI Server

Start the FastAPI server with the following command:
```bash
uvicorn main:app --reload
```

You can view and test the APIs by navigating to `/docs` in your browser:
```
http://127.0.0.1:8000/docs
```

The OpenAPI schema can be accessed at:
```
http://127.0.0.1:8000/openapi.json
```

### Running the React App

Navigate to the React app directory and start the development server:
```bash
cd react-app
npm install
npm start
```

## License

This project is licensed under the MIT License.

## Acknowledgements

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
