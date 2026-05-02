# DevFlow Checkpoint AI - Setup Instructions

## Quick Start Guide

This guide will help you set up DevFlow Checkpoint AI with PostgreSQL database and IBM BOB (Anthropic Claude) integration.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**
- **Node.js 18+** and npm
- **PostgreSQL 14+**
- **Redis 7+** (optional, for caching)
- **Git**

## Step 1: Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd devflow-checkpoint-ai

# Create and activate Python virtual environment
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

## Step 2: Database Setup

### Install and Start PostgreSQL

**Windows:**
```bash
# Download from https://www.postgresql.org/download/windows/
# Or use chocolatey
choco install postgresql
```

**macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Linux:**
```bash
sudo apt-get install postgresql-14
sudo systemctl start postgresql
```

### Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE devflow_db;
CREATE USER devflow_user WITH PASSWORD 'devflow_pass';
GRANT ALL PRIVILEGES ON DATABASE devflow_db TO devflow_user;
\q
```

## Step 3: Redis Setup (Optional but Recommended)

**Windows:**
```bash
# Download from https://github.com/microsoftarchive/redis/releases
# Or use chocolatey
choco install redis-64
redis-server
```

**macOS:**
```bash
brew install redis
brew services start redis
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

**Using Docker:**
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

## Step 4: Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and configure:

```env
# Application
APP_NAME=DevFlow Checkpoint AI
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development

# Server
HOST=0.0.0.0
PORT=8000

# Database - Update with your credentials
DATABASE_URL=postgresql+asyncpg://devflow_user:devflow_pass@localhost:5432/devflow_db

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# IBM BOB / Anthropic - REQUIRED for AI features
ANTHROPIC_API_KEY=your-actual-anthropic-api-key-here
BOB_MODEL=claude-3-5-sonnet-20241022
BOB_MAX_TOKENS=100000
BOB_TEMPERATURE=0.7

# CORS
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

### Get Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and paste it in `.env` as `ANTHROPIC_API_KEY`

## Step 5: Run Database Migrations

```bash
cd backend

# Run migrations to create tables
alembic upgrade head
```

If you get an error about alembic not being found, ensure you've activated the virtual environment and installed dependencies.

## Step 6: Start the Backend

```bash
# Make sure you're in the backend directory with venv activated
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Step 7: Start the Frontend

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at:
- **Application**: http://localhost:5173

## Step 8: Verify Installation

### Test Database Connection

```bash
# In backend directory with venv activated
python -c "from app.database import engine; import asyncio; asyncio.run(engine.connect())"
```

### Test API

```bash
# Health check
curl http://localhost:8000/health

# Create a test project
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Project", "description": "Testing setup"}'
```

### Test IBM BOB Integration

```bash
# Test planning agent
curl -X POST http://localhost:8000/api/v1/bob/plan \
  -H "Content-Type: application/json" \
  -d '{"project_description": "Build a todo app", "context": {}}'
```

If you see a response with milestones and recommendations, IBM BOB is working!

## Troubleshooting

### Database Connection Issues

**Error: "could not connect to server"**
```bash
# Check if PostgreSQL is running
# Windows
sc query postgresql-x64-14

# macOS
brew services list

# Linux
sudo systemctl status postgresql

# Start if not running
# Windows
net start postgresql-x64-14

# macOS
brew services start postgresql@14

# Linux
sudo systemctl start postgresql
```

**Error: "password authentication failed"**
- Verify credentials in `.env` match those used in `CREATE USER`
- Check `pg_hba.conf` for authentication settings

### Redis Connection Issues

**Error: "Connection refused"**
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# Start Redis if not running
# Windows
redis-server

# macOS
brew services start redis

# Linux
sudo systemctl start redis
```

### Anthropic API Issues

**Error: "API key not configured"**
- Ensure `ANTHROPIC_API_KEY` is set in `.env`
- Verify the key is valid at https://console.anthropic.com/

**Fallback Mode**
- If API key is not configured, the system will use fallback responses
- BOB features will work but with pre-defined responses instead of AI-generated ones

### Port Already in Use

**Backend (port 8000)**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

**Frontend (port 5173)**
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5173
kill -9 <PID>
```

### Migration Issues

**Error: "Target database is not up to date"**
```bash
cd backend
alembic upgrade head
```

**Error: "Can't locate revision"**
```bash
# Check current revision
alembic current

# View migration history
alembic history

# Downgrade and upgrade
alembic downgrade base
alembic upgrade head
```

## Docker Setup (Alternative)

If you prefer using Docker:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Development Workflow

### Running Tests

```bash
# Backend tests
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html

# Frontend tests
cd frontend
npm test
```

### Code Formatting

```bash
# Backend
cd backend
black app tests
isort app tests
flake8 app tests

# Frontend
cd frontend
npm run lint
npm run format
```

### Creating New Migrations

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Features Overview

### Checkpoint System
- Automatic snapshots after each milestone (plan → code → debug → test)
- Version control for project states
- Restore from any checkpoint
- Diff calculation between checkpoints

### IBM BOB Integration
- **Planning Agent**: Generates project milestones and breakdown
- **Debugging Agent**: Analyzes errors and suggests fixes
- **Testing Agent**: Generates test cases and test code
- **Context Management**: Maintains workflow memory across sessions

### Workflow States
1. **Plan**: Initial project planning with BOB
2. **Code**: Development phase
3. **Debug**: Error analysis and fixing
4. **Test**: Test generation and execution

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Create a Project**: Use the frontend or API
3. **Test BOB Features**: Try planning, debugging, and testing agents
4. **Review Documentation**: Check ARCHITECTURE.md and MIGRATION-PLAN.md

## Support

For issues or questions:
- Check TROUBLESHOOTING section above
- Review MIGRATION-PLAN.md for detailed architecture
- Check GitHub issues
- Consult API documentation at /docs endpoint

## Production Deployment

For production deployment:
1. Set `DEBUG=false` in `.env`
2. Use strong database passwords
3. Configure proper CORS origins
4. Set up SSL/TLS
5. Use environment-specific configuration
6. Enable monitoring and logging
7. Set up automated backups

See ARCHITECTURE.md for detailed production deployment guidelines.

---

**Happy Coding! 🚀**