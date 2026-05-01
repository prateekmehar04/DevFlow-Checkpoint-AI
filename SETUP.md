# DevFlow Checkpoint AI - Development Environment Setup

## Prerequisites

### Required Software
- **Python**: 3.11 or higher
- **Node.js**: 18.x or higher
- **npm**: 9.x or higher (comes with Node.js)
- **PostgreSQL**: 14.x or higher
- **Redis**: 7.x or higher
- **Git**: Latest version
- **Docker**: 20.x or higher (optional, for containerized development)
- **Docker Compose**: 2.x or higher (optional)

### Recommended Tools
- **VS Code**: Latest version with Python and TypeScript extensions
- **Postman** or **Insomnia**: For API testing
- **pgAdmin** or **DBeaver**: For database management
- **Redis Commander**: For Redis management

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/devflow-checkpoint-ai.git
cd devflow-checkpoint-ai
```

### 2. Backend Setup

#### Create Python Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

#### Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development tools
```

#### Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Application
APP_NAME=DevFlow Checkpoint AI
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://devflow_user:devflow_pass@localhost:5432/devflow_db
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_TTL=3600

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# AI Integration (IBM BOB)
ANTHROPIC_API_KEY=your-anthropic-api-key-here
BOB_MODEL=claude-3-5-sonnet-20241022
BOB_MAX_TOKENS=100000
BOB_TEMPERATURE=0.7
BOB_STREAMING=True

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

#### Set Up PostgreSQL Database

```bash
# Create database and user
psql -U postgres

CREATE DATABASE devflow_db;
CREATE USER devflow_user WITH PASSWORD 'devflow_pass';
GRANT ALL PRIVILEGES ON DATABASE devflow_db TO devflow_user;
\q
```

#### Run Database Migrations

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

#### Start Redis

```bash
# On Windows (if installed via MSI)
redis-server

# On macOS (via Homebrew)
brew services start redis

# On Linux
sudo systemctl start redis

# Or using Docker
docker run -d -p 6379:6379 redis:7-alpine
```

#### Run Backend Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the provided script
python -m app.main
```

The backend API will be available at:
- **API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

### 3. Frontend Setup

#### Install Node.js Dependencies

```bash
cd frontend
npm install
```

#### Configure Environment Variables

Create a `.env` file in the `frontend` directory:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws

# Application
VITE_APP_NAME=DevFlow Checkpoint AI
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_ENABLE_BOB_CHAT=true
VITE_ENABLE_REAL_TIME_UPDATES=true
VITE_ENABLE_ANALYTICS=false

# Development
VITE_DEBUG=true
```

#### Run Frontend Development Server

```bash
npm run dev
```

The frontend will be available at:
- **Application**: http://localhost:5173 (or http://localhost:3000 depending on your setup)

### 4. Docker Setup (Alternative)

If you prefer using Docker for development:

#### Create docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14-alpine
    environment:
      POSTGRES_DB: devflow_db
      POSTGRES_USER: devflow_user
      POSTGRES_PASSWORD: devflow_pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://devflow_user:devflow_pass@postgres:5432/devflow_db
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      VITE_API_BASE_URL: http://localhost:8000/api/v1
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev -- --host

volumes:
  postgres_data:
  redis_data:
```

#### Start All Services

```bash
docker-compose up -d
```

#### Stop All Services

```bash
docker-compose down
```

## Development Workflow

### Running Tests

#### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_checkpoints.py

# Run with verbose output
pytest -v
```

#### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

### Code Quality

#### Backend Linting and Formatting

```bash
cd backend

# Format code with Black
black app tests

# Sort imports with isort
isort app tests

# Lint with flake8
flake8 app tests

# Type checking with mypy
mypy app
```

#### Frontend Linting and Formatting

```bash
cd frontend

# Lint with ESLint
npm run lint

# Fix linting issues
npm run lint:fix

# Format with Prettier
npm run format

# Type checking
npm run type-check
```

### Database Management

#### Create New Migration

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

#### Apply Migrations

```bash
alembic upgrade head
```

#### Rollback Migration

```bash
alembic downgrade -1
```

#### View Migration History

```bash
alembic history
```

### API Testing

#### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Create project
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Project", "description": "A test project"}'

# List projects
curl http://localhost:8000/api/v1/projects
```

#### Using Python requests

```python
import requests

# Create project
response = requests.post(
    "http://localhost:8000/api/v1/projects",
    json={"name": "Test Project", "description": "A test project"}
)
print(response.json())
```

## Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Find process using port 8000
# On Windows
netstat -ano | findstr :8000

# On macOS/Linux
lsof -i :8000

# Kill the process
# On Windows
taskkill /PID <PID> /F

# On macOS/Linux
kill -9 <PID>
```

#### Database Connection Issues

```bash
# Check if PostgreSQL is running
# On Windows
sc query postgresql-x64-14

# On macOS
brew services list

# On Linux
sudo systemctl status postgresql

# Test connection
psql -U devflow_user -d devflow_db -h localhost
```

#### Redis Connection Issues

```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# Check Redis info
redis-cli info
```

#### Python Virtual Environment Issues

```bash
# Deactivate current environment
deactivate

# Remove old environment
rm -rf venv

# Create new environment
python -m venv venv

# Activate and reinstall
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Node Modules Issues

```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall dependencies
npm install
```

### Getting Help

- **Documentation**: Check the [ARCHITECTURE.md](./ARCHITECTURE.md) file
- **API Docs**: Visit http://localhost:8000/docs when the backend is running
- **Issues**: Report bugs on the GitHub issues page
- **Discussions**: Join the project discussions for questions

## Next Steps

After setting up your development environment:

1. Review the [ARCHITECTURE.md](./ARCHITECTURE.md) to understand the system design
2. Check the [PROJECT-PLAN.md](./PROJECT-PLAN.md) for the implementation roadmap
3. Start with Milestone 1: Project Foundation & Setup
4. Follow the development workflow for making changes
5. Submit pull requests for review

## Additional Resources

### Python/FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

### React/TypeScript
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Redux Toolkit Documentation](https://redux-toolkit.js.org/)
- [Vite Documentation](https://vitejs.dev/)

### Database
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/docs/)

### AI Integration
- [Anthropic Claude API Documentation](https://docs.anthropic.com/)

### DevOps
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

**Happy Coding! 🚀**