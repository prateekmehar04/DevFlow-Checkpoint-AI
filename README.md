![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)


# DevFlow Checkpoint AI

**A stateful AI-powered development workflow system that saves structured snapshots after each milestone (plan → code → debug → test).**

Powered by **IBM BOB** as the persistent AI orchestrator for planning, debugging, and maintaining development context across sessions.

## 🚀 Features

- **Checkpoint-Based Workflow**: Automatic state snapshots at each milestone
- **IBM BOB Integration**: AI-powered planning, debugging, and testing assistance
- **PostgreSQL + Supabase**: Production-ready database with cloud hosting
- **FastAPI Backend**: High-performance async REST API
- **State Machine**: Guarded transitions between workflow states
- **Context Persistence**: Resume from last checkpoint after crashes or tool swaps
- **Streaming AI Responses**: Real-time BOB interactions via Server-Sent Events

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- IBM BOB API Key
- Supabase PostgreSQL Database (or local PostgreSQL)

## 🛠️ Setup

### 1. Clone and Install Dependencies

**Backend:**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example backend/.env
```

Edit `backend/.env` with your credentials:
```env
# IBM BOB API Configuration
IBM_BOB_API_KEY=your-ibm-bob-api-key-here
IBM_BOB_API_URL=https://api.ibm.com/bob/v1

# Supabase PostgreSQL Database
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@db.whulvrnkotzizayydtrr.supabase.co:5432/postgres

# Application Settings
DEBUG=true
SECRET_KEY=your-secret-key-here
```

### 3. Initialize Database

Run Alembic migrations to create database tables:
```bash
cd backend
alembic upgrade head
```

### 4. Run the Application

**Backend (Terminal 1):**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

**Access Points:**
- 🌐 **API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs
- 🎨 **Frontend**: http://localhost:5173

## 📖 Usage

### API Workflow

1. **Create Project**: `POST /api/v1/projects`
2. **Initialize Workflow**: `POST /api/v1/workflows`
3. **Create Checkpoint**: `POST /api/v1/checkpoints`
4. **Transition State**: `POST /api/v1/workflows/{workflow_id}/transition`
5. **Compare Checkpoints**: `GET /api/v1/checkpoints/diff?left_id=...&right_id=...`
6. **Chat with BOB**: `POST /api/v1/bob/chat`
7. **Stream BOB Response**: `GET /api/v1/bob/stream`

### BOB Agents

- **Planning Agent**: Generate project milestones and architecture
- **Debugging Agent**: Analyze errors and suggest fixes
- **Testing Agent**: Generate test cases and validation strategies

### Workflow States

```
plan → code → debug → test → done
  ↓      ↓       ↓       ↓
[checkpoint at each transition]
```

## 🏗️ Architecture

```
DevFlow Checkpoint AI/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes
│   │   ├── models/       # SQLAlchemy models
│   │   ├── services/     # Business logic
│   │   │   └── bob/      # IBM BOB integration
│   │   ├── config.py     # Configuration
│   │   ├── database.py   # Database connection
│   │   └── main.py       # FastAPI app
│   ├── alembic/          # Database migrations
│   └── tests/            # Backend tests
├── frontend/             # React + Vite UI
└── docs/                 # Documentation
```

## 🧪 Testing

**Backend Tests:**
```bash
cd backend
pytest
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

## 🐳 Docker Deployment

```bash
docker compose up --build
```

## 📚 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: System design and milestones
- **[IBM-BOB-SETUP.md](IBM-BOB-SETUP.md)**: IBM BOB API integration guide
- **[SETUP-INSTRUCTIONS.md](SETUP-INSTRUCTIONS.md)**: Detailed setup instructions
- **[MIGRATION-PLAN.md](MIGRATION-PLAN.md)**: Database migration strategy

## 🔧 Troubleshooting

### Database Connection Issues
- Verify Supabase credentials in `.env`
- Check network connectivity to Supabase
- Run `alembic upgrade head` to ensure schema is up-to-date

### IBM BOB API Issues
- Verify `IBM_BOB_API_KEY` is set correctly
- Check `IBM_BOB_API_URL` endpoint
- Review logs for API response errors

### Development Server Issues
- Ensure ports 8000 (backend) and 5173 (frontend) are available
- Check Python/Node.js versions meet requirements
- Clear `__pycache__` and `node_modules` if needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 🙏 Acknowledgments

- **IBM BOB**: AI orchestration and development assistance
- **Supabase**: PostgreSQL database hosting
- **FastAPI**: High-performance Python web framework
- **React**: Frontend UI framework
