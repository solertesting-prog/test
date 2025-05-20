# Lexy BE
Welcome to the Interview Backend Challenge! This project is built with **FastAPI** for serving the API and **Pydantic** for robust data validation, following a clean architecture approach to ensure maintainability and scalability.

## 🎯 Objectives

The objectives are described in the PDF you received.

## ⚙️ Requirements

- 🐍 Python 3.13 or higher
- ⚡ [UV](https://github.com/astral-sh/uv) (Python package manager and virtual environment tool)
- 🐳 Docker (for containerized development)

## 🚀 Getting Started

### 1️⃣ Install Python

Make sure you have Python 3.13 or higher installed. You can download it from the [official Python website](https://www.python.org/downloads/).

### 2️⃣ Install UV

UV is a fast Python package manager that also allows you to create and manage virtual environments.


For installation details, see the [UV documentation](https://docs.astral.sh/uv/#installation).

### 3️⃣ Create a Virtual Environment

UV automatically creates a virtual environment for the project by installing the required dependencies.
At this point it is necessary to have Python version 3.13 or higher installed.
To create a virtual environment and install the dependencies, run the following command in the project directory:

```sh
uv sync --extra dev
```

### 4️⃣ Run the Project
To run the project, use the following command:

```sh
docker-compose build
docker-compose up
```

### 5️⃣ Access the Application
Once the application is running, you can access it at `http://localhost:3001/docs`.

### 6️⃣ Run Tests
To run the tests, use the following command:
```sh
uv run pytest ./tests
```
 
## 🏗️ Project Architecture Overview

The codebase is organized into three main layers:

### 1. `api/` – Presentation Layer 🌐
- Exposes the HTTP API using FastAPI.
- Contains route definitions for users and news (`routes/`).
- Handles authentication and security logic (`auth/`).
- Manages dependency injection and wiring via `container.py`, which connects protocol interfaces to their concrete implementations for loose coupling and easy testing.

### 2. `core/` – Domain Layer 🧠
- Defines the business logic and domain entities.
- Organized by feature (e.g., `news/`, `users/`), each with:
  - `entities/`: Pydantic models and DTOs for data validation and transfer.
  - `protocols/`: Abstract repository interfaces (Python Protocols) that describe required data operations, independent of the database or framework.
  - `services/`: Business logic and use cases, operating only on protocols and entities, never on infrastructure details.

### 3. `infraestructure/` – Infrastructure Layer 🗄️
- Implements the actual data access logic.
- Contains database models (Beanie ODM for MongoDB) and repository implementations that fulfill the contracts defined in `core/protocols/`.
- Includes database connection setup and seeding utilities.

### 🔗 Dependency Injection
- The `api/container.py` file is responsible for dependency injection.
- It binds protocol interfaces from `core/protocols/` to their concrete implementations in `infraestructure/database/repositories/`.
- This design allows you to swap implementations (e.g., for testing) without changing business logic.

  ## 📝 Notes
- Ensure you have Docker installed and running to use docker-compose commands.
- The project is designed to be run in a virtual environment for better dependency management.
- The `uv` command is used to manage the virtual environment and dependencies.
- If you want to add a new dependency with `uv` you can use the command:
```sh
uv add <package_name>
```

## 💻 Recommended IDEs
- [Visual Studio Code](https://code.visualstudio.com/)
  - If you are using Visual Studio Code, you can install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) for better support.
  - And the black formatter for code formatting.
