# ZONE3000 Test Project

---

## Project Setup

### Prerequisites

- Python 3.10
- Docker & Docker Compose (if using Docker setup)
- Make (if using Makefile)
- Pipenv (for dependency management)

### Docker Setup

1. Create a `.env` file based on the `.env.example` file:
   ```bash
   cp .env.example .env
   ```
2. Build and start the Docker services:
   ```bash
   docker-compose up --build -d
   ```
3. (Optional) If you need to create a superuser, run:
   ```bash
   docker-compose exec my_project_app python manage.py createsuperuser
   ```

### Makefile Setup

- **Initialize the project** (creates `.env`, runs Docker, applies migrations, creates superuser, loads fixtures):
   ```bash
   make init
   ```
- **Stop the containers**:
   ```bash
   make down
   ```
- **View logs from the containers**:
   ```bash
   make logs
   ```
- **Enter the app container**:
   ```bash
   make sh
   ```
- **Run tests**:
   ```bash
   make test
   ```
- **Clean unused Docker resources**:
   ```bash
   make clean
   ```

### Local Setup

If you prefer setting up and running the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/nyckolas-python/zone3000-test-task
   ```
2. Install Pipenv if not installed:
   ```bash
   pip install --user pipenv
   ```
3. Navigate to the project directory and install dependencies:
   ```bash
   cd backend
   pipenv install --dev
   ```
4. Activate the virtual environment:
   ```bash
   pipenv shell
   ```
5. Create a `.env` file based on the `.env.example` file:
   ```bash
   cp .env.example .env
   ```
6. Apply the migrations:
   ```bash
   python manage.py migrate
   ```
7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
8. Load test data to the database:
   ```bash
   python manage.py load_redirect_rules --username=<superuser>
   ```
9. Run the development server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
10. Optionally, run the tests:
    ```bash
    pytest
    ```

Swagger documentation will be available at [http://localhost:8000/swagger/](http://localhost:8000/swagger/). By default, it uses the SQLite3 database.
