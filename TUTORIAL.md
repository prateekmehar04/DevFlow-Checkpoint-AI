# DevFlow Checkpoint AI - Complete Tutorial

## 📚 Table of Contents
1. [System Overview](#system-overview)
2. [Core Concepts](#core-concepts)
3. [Getting Started](#getting-started)
4. [Step-by-Step Workflow](#step-by-step-workflow)
5. [API Reference](#api-reference)
6. [IBM BOB Integration](#ibm-bob-integration)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)

---

## System Overview

### What is DevFlow Checkpoint AI?

DevFlow Checkpoint AI is an **AI-powered development workflow system** that automatically saves your project's state at critical milestones. Think of it as "Git commits on steroids" - but instead of just tracking code changes, it tracks your entire development workflow with AI assistance.

### The Problem It Solves

**Traditional Development Pain Points:**
- 🔴 Lost context when switching between projects
- 🔴 AI chat sessions reset, losing valuable conversation history
- 🔴 Hard to track what worked and what didn't during debugging
- 🔴 No structured way to resume after interruptions

**DevFlow Solution:**
- ✅ Automatic checkpoints at each workflow milestone
- ✅ Persistent AI context via IBM BOB
- ✅ Structured workflow: plan → code → debug → test → done
- ✅ Resume from any checkpoint, even after crashes

### Architecture at a Glance

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│              User Interface & Dashboard                  │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST API
┌────────────────────▼────────────────────────────────────┐
│                 FastAPI Backend                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │           API Routes (Endpoints)                  │  │
│  └──────────────────┬───────────────────────────────┘  │
│  ┌──────────────────▼───────────────────────────────┐  │
│  │         Business Logic (Services)                 │  │
│  │  • Project Service  • Checkpoint Service          │  │
│  │  • Workflow Service • State Manager               │  │
│  └──────────────────┬───────────────────────────────┘  │
│  ┌──────────────────▼───────────────────────────────┐  │
│  │          IBM BOB Orchestrator                     │  │
│  │  • Planning Agent  • Debugging Agent              │  │
│  │  • Testing Agent   • Context Manager              │  │
│  └──────────────────┬───────────────────────────────┘  │
└────────────────────┬┴───────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐      ┌────────▼─────────┐
│   PostgreSQL   │      │   IBM BOB API    │
│   (Supabase)   │      │  (AI Services)   │
└────────────────┘      └──────────────────┘
```

---

## Core Concepts

### 1. Projects
A **Project** represents a software development initiative.

**Properties:**
- `name`: Project identifier
- `description`: What you're building
- `tech_stack`: Technologies used (e.g., "Python, FastAPI, React")
- `created_at`: Timestamp

**Example:**
```json
{
  "name": "E-commerce API",
  "description": "RESTful API for online shopping",
  "tech_stack": "Python, FastAPI, PostgreSQL, Stripe"
}
```

### 2. Workflows
A **Workflow** tracks the development lifecycle of a project through distinct states.

**States:**
1. **plan** - Initial planning and architecture
2. **code** - Implementation phase
3. **debug** - Bug fixing and troubleshooting
4. **test** - Testing and validation
5. **done** - Completed milestone

**State Transitions:**
```
plan ──→ code ──→ debug ──→ test ──→ done
 ↓        ↓         ↓         ↓
[checkpoint] [checkpoint] [checkpoint] [checkpoint]
```

**Rules:**
- Can only move forward (plan → code → debug → test → done)
- Can rollback to previous states
- Each transition creates an automatic checkpoint

### 3. Checkpoints
A **Checkpoint** is a snapshot of your project's state at a specific moment.

**Contains:**
- `workflow_state`: Current state (plan/code/debug/test/done)
- `code_snapshot`: Your code files (JSON format)
- `context`: AI conversation history, decisions made
- `metadata`: Additional information (git commit, dependencies, etc.)
- `created_at`: Timestamp

**Example:**
```json
{
  "workflow_id": "wf_123",
  "workflow_state": "code",
  "code_snapshot": {
    "src/main.py": "def hello():\n    return 'Hello'",
    "requirements.txt": "fastapi==0.104.1"
  },
  "context": {
    "decisions": ["Using FastAPI for REST API"],
    "ai_suggestions": ["Add input validation"]
  },
  "metadata": {
    "git_commit": "abc123",
    "dependencies_installed": true
  }
}
```

### 4. IBM BOB Agents

**BOB** (Builder, Orchestrator, Bot) is your AI assistant with three specialized agents:

#### Planning Agent
- Generates project architecture
- Creates milestone breakdowns
- Suggests tech stack
- Provides implementation roadmap

#### Debugging Agent
- Analyzes error messages
- Suggests fixes
- Identifies root causes
- Provides code corrections

#### Testing Agent
- Generates test cases
- Creates test strategies
- Suggests edge cases
- Validates implementations

---

## Getting Started

### Prerequisites Check

```bash
# Check Python version (need 3.11+)
python --version

# Check Node.js version (need 18+)
node --version

# Verify pip
pip --version

# Verify npm
npm --version
```

### Installation

**1. Clone the repository:**
```bash
git clone <your-repo-url>
cd DevFlow-Checkpoint-AI
```

**2. Backend Setup:**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

**3. Frontend Setup:**
```bash
cd frontend
npm install
```

**4. Configure Environment:**
```bash
# Copy example env file
cp .env.example backend/.env

# Edit backend/.env with your credentials
```

**Required Environment Variables:**
```env
# IBM BOB API
IBM_BOB_API_KEY=your-api-key-here
IBM_BOB_API_URL=https://api.ibm.com/bob/v1

# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@host:5432/dbname

# App Settings
DEBUG=true
SECRET_KEY=your-secret-key
```

**5. Initialize Database:**
```bash
cd backend
alembic upgrade head
```

**6. Start Services:**

Terminal 1 (Backend):
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

**7. Verify Installation:**
- Backend: http://localhost:8000/health
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

---

## Step-by-Step Workflow

### Scenario: Building a Todo API

Let's walk through a complete development workflow.

### Step 1: Create a Project

**Via API (curl):**
```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Todo API",
    "description": "Simple REST API for managing todos",
    "tech_stack": "Python, FastAPI, PostgreSQL"
  }'
```

**Response:**
```json
{
  "id": "proj_abc123",
  "name": "Todo API",
  "description": "Simple REST API for managing todos",
  "tech_stack": "Python, FastAPI, PostgreSQL",
  "created_at": "2026-05-02T10:00:00Z"
}
```

**Via Frontend:**
1. Open http://localhost:5173
2. Click "New Project"
3. Fill in the form
4. Click "Create"

### Step 2: Initialize Workflow

**API Request:**
```bash
curl -X POST http://localhost:8000/api/v1/workflows \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "proj_abc123",
    "initial_state": "plan"
  }'
```

**Response:**
```json
{
  "id": "wf_xyz789",
  "project_id": "proj_abc123",
  "current_state": "plan",
  "state_history": ["plan"],
  "created_at": "2026-05-02T10:01:00Z"
}
```

### Step 3: Get AI Planning Assistance

**Ask BOB for a Plan:**
```bash
curl -X POST http://localhost:8000/api/v1/bob/plan \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "proj_abc123",
    "requirements": "Build a REST API with CRUD operations for todos. Each todo has title, description, completed status."
  }'
```

**BOB's Response:**
```json
{
  "plan": {
    "milestones": [
      {
        "name": "Database Schema",
        "tasks": [
          "Create Todo model with SQLAlchemy",
          "Add migration for todos table",
          "Define relationships if needed"
        ]
      },
      {
        "name": "API Endpoints",
        "tasks": [
          "POST /todos - Create todo",
          "GET /todos - List all todos",
          "GET /todos/{id} - Get single todo",
          "PUT /todos/{id} - Update todo",
          "DELETE /todos/{id} - Delete todo"
        ]
      },
      {
        "name": "Validation & Error Handling",
        "tasks": [
          "Add Pydantic schemas",
          "Implement error responses",
          "Add input validation"
        ]
      }
    ],
    "architecture": {
      "models": ["Todo"],
      "routes": ["/todos"],
      "services": ["TodoService"]
    },
    "tech_recommendations": {
      "orm": "SQLAlchemy",
      "validation": "Pydantic",
      "testing": "pytest"
    }
  }
}
```

### Step 4: Create First Checkpoint

**Save the Planning Phase:**
```bash
curl -X POST http://localhost:8000/api/v1/checkpoints \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "wf_xyz789",
    "workflow_state": "plan",
    "code_snapshot": {},
    "context": {
      "plan": "BOB generated plan for Todo API",
      "decisions": ["Using FastAPI", "PostgreSQL for storage"]
    },
    "metadata": {
      "phase": "initial_planning"
    }
  }'
```

**Response:**
```json
{
  "id": "cp_001",
  "workflow_id": "wf_xyz789",
  "workflow_state": "plan",
  "created_at": "2026-05-02T10:05:00Z"
}
```

### Step 5: Transition to Code Phase

**Move to Implementation:**
```bash
curl -X POST http://localhost:8000/api/v1/workflows/wf_xyz789/transition \
  -H "Content-Type: application/json" \
  -d '{
    "new_state": "code"
  }'
```

**What Happens:**
1. System validates transition (plan → code is valid)
2. **Automatically creates a checkpoint** before transition
3. Updates workflow state to "code"
4. Returns updated workflow

**Response:**
```json
{
  "id": "wf_xyz789",
  "current_state": "code",
  "state_history": ["plan", "code"],
  "auto_checkpoint_created": "cp_002"
}
```

### Step 6: Implement Code

Now you write your code. Let's say you create:

**File: `models/todo.py`**
```python
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
```

**File: `routes/todos.py`**
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.todo import Todo
from database import get_db

router = APIRouter()

@router.post("/todos")
def create_todo(title: str, db: Session = Depends(get_db)):
    todo = Todo(title=title)
    db.add(todo)
    db.commit()
    return todo
```

### Step 7: Save Code Checkpoint

**Checkpoint Your Implementation:**
```bash
curl -X POST http://localhost:8000/api/v1/checkpoints \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "wf_xyz789",
    "workflow_state": "code",
    "code_snapshot": {
      "models/todo.py": "from sqlalchemy import Column...",
      "routes/todos.py": "from fastapi import APIRouter..."
    },
    "context": {
      "completed": ["Todo model", "Create endpoint"],
      "next": ["Add remaining CRUD endpoints"]
    }
  }'
```

### Step 8: Hit a Bug - Transition to Debug

**You encounter an error:**
```
sqlalchemy.exc.OperationalError: no such table: todos
```

**Transition to Debug State:**
```bash
curl -X POST http://localhost:8000/api/v1/workflows/wf_xyz789/transition \
  -H "Content-Type: application/json" \
  -d '{"new_state": "debug"}'
```

### Step 9: Get Debugging Help from BOB

**Ask BOB to Analyze the Error:**
```bash
curl -X POST http://localhost:8000/api/v1/bob/debug \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "proj_abc123",
    "error_message": "sqlalchemy.exc.OperationalError: no such table: todos",
    "code_context": {
      "models/todo.py": "class Todo(Base)...",
      "routes/todos.py": "@router.post..."
    }
  }'
```

**BOB's Analysis:**
```json
{
  "diagnosis": {
    "issue": "Database table not created",
    "root_cause": "Missing database migration",
    "severity": "high"
  },
  "solution": {
    "steps": [
      "Create Alembic migration: alembic revision --autogenerate -m 'Add todos table'",
      "Run migration: alembic upgrade head",
      "Verify table exists: Check database"
    ],
    "code_fix": "# Run these commands:\nalembic revision --autogenerate -m 'Add todos table'\nalembic upgrade head"
  },
  "prevention": "Always run migrations after creating new models"
}
```

### Step 10: Fix and Test

**After fixing, transition to test:**
```bash
curl -X POST http://localhost:8000/api/v1/workflows/wf_xyz789/transition \
  -H "Content-Type: application/json" \
  -d '{"new_state": "test"}'
```

**Get Test Suggestions from BOB:**
```bash
curl -X POST http://localhost:8000/api/v1/bob/test \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "proj_abc123",
    "code_to_test": "Todo API endpoints"
  }'
```

**BOB's Test Plan:**
```json
{
  "test_cases": [
    {
      "name": "test_create_todo",
      "description": "Verify todo creation",
      "code": "def test_create_todo():\n    response = client.post('/todos', json={'title': 'Test'})\n    assert response.status_code == 200"
    },
    {
      "name": "test_create_todo_without_title",
      "description": "Verify validation",
      "code": "def test_create_todo_without_title():\n    response = client.post('/todos', json={})\n    assert response.status_code == 422"
    }
  ]
}
```

### Step 11: Compare Checkpoints

**See what changed between planning and implementation:**
```bash
curl "http://localhost:8000/api/v1/checkpoints/diff?left_id=cp_001&right_id=cp_003"
```

**Response:**
```json
{
  "left_checkpoint": {
    "id": "cp_001",
    "state": "plan",
    "created_at": "2026-05-02T10:05:00Z"
  },
  "right_checkpoint": {
    "id": "cp_003",
    "state": "code",
    "created_at": "2026-05-02T10:30:00Z"
  },
  "differences": {
    "code_changes": {
      "added_files": ["models/todo.py", "routes/todos.py"],
      "modified_files": [],
      "deleted_files": []
    },
    "state_change": "plan → code",
    "context_evolution": {
      "plan_phase": "Architecture defined",
      "code_phase": "Implementation started"
    }
  }
}
```

### Step 12: Restore from Checkpoint (if needed)

**If something goes wrong, restore previous state:**
```bash
curl -X POST http://localhost:8000/api/v1/checkpoints/cp_002/restore
```

**What Happens:**
1. System loads checkpoint data
2. Restores code snapshot
3. Restores context
4. Rolls back workflow state
5. You can continue from that point

---

## API Reference

### Projects API

#### Create Project
```http
POST /api/v1/projects
Content-Type: application/json

{
  "name": "string",
  "description": "string",
  "tech_stack": "string"
}
```

#### Get Project
```http
GET /api/v1/projects/{project_id}
```

#### List Projects
```http
GET /api/v1/projects?skip=0&limit=10
```

#### Update Project
```http
PUT /api/v1/projects/{project_id}
Content-Type: application/json

{
  "name": "string",
  "description": "string",
  "tech_stack": "string"
}
```

#### Delete Project
```http
DELETE /api/v1/projects/{project_id}
```

### Workflows API

#### Create Workflow
```http
POST /api/v1/workflows
Content-Type: application/json

{
  "project_id": "string",
  "initial_state": "plan"
}
```

#### Get Workflow
```http
GET /api/v1/workflows/{workflow_id}
```

#### Transition State
```http
POST /api/v1/workflows/{workflow_id}/transition
Content-Type: application/json

{
  "new_state": "code"
}
```

#### Get State History
```http
GET /api/v1/workflows/{workflow_id}/history
```

#### Rollback State
```http
POST /api/v1/workflows/{workflow_id}/rollback
Content-Type: application/json

{
  "target_state": "plan"
}
```

### Checkpoints API

#### Create Checkpoint
```http
POST /api/v1/checkpoints
Content-Type: application/json

{
  "workflow_id": "string",
  "workflow_state": "code",
  "code_snapshot": {},
  "context": {},
  "metadata": {}
}
```

#### Get Checkpoint
```http
GET /api/v1/checkpoints/{checkpoint_id}
```

#### List Checkpoints
```http
GET /api/v1/checkpoints?workflow_id=wf_123&skip=0&limit=10
```

#### Compare Checkpoints
```http
GET /api/v1/checkpoints/diff?left_id=cp_001&right_id=cp_002
```

#### Restore Checkpoint
```http
POST /api/v1/checkpoints/{checkpoint_id}/restore
```

### BOB API

#### Chat with BOB
```http
POST /api/v1/bob/chat
Content-Type: application/json

{
  "message": "string",
  "context": {}
}
```

#### Stream BOB Response
```http
GET /api/v1/bob/stream?message=hello
Accept: text/event-stream
```

#### Get Planning Assistance
```http
POST /api/v1/bob/plan
Content-Type: application/json

{
  "project_id": "string",
  "requirements": "string"
}
```

#### Get Debugging Help
```http
POST /api/v1/bob/debug
Content-Type: application/json

{
  "project_id": "string",
  "error_message": "string",
  "code_context": {}
}
```

#### Get Testing Suggestions
```http
POST /api/v1/bob/test
Content-Type: application/json

{
  "project_id": "string",
  "code_to_test": "string"
}
```

---

## IBM BOB Integration

### How BOB Works

**1. Request Flow:**
```
Your App → DevFlow API → IBM BOB Client → IBM BOB API → AI Model
```

**2. Response Flow:**
```
AI Model → IBM BOB API → IBM BOB Client → DevFlow API → Your App
```

### BOB Client Architecture

**File: `backend/app/services/bob/ibm_bob_client.py`**

```python
class IBMBobClient:
    """Custom client for IBM BOB API"""
    
    async def create_message(self, model, max_tokens, temperature, 
                            system, messages):
        """Send message to BOB and get response"""
        # Constructs request
        # Calls IBM BOB API
        # Returns formatted response
        
    async def stream_message(self, ...):
        """Stream BOB responses in real-time"""
        # Opens SSE connection
        # Yields chunks as they arrive
```

### Customizing BOB Behavior

**Modify Agent Prompts:**

**File: `backend/app/services/bob/planning_agent.py`**
```python
system_prompt = """
You are an expert software architect.
Your role: Generate detailed project plans.
Output format: JSON with milestones and tasks.

# Customize this prompt for your needs
"""
```

**Adjust Temperature (Creativity):**
```python
response = await self.client.create_message(
    model="claude-3-sonnet",
    max_tokens=4000,
    temperature=0.7,  # 0.0 = deterministic, 1.0 = creative
    system=system_prompt,
    messages=messages
)
```

### BOB API Configuration

**Environment Variables:**
```env
IBM_BOB_API_KEY=your-key
IBM_BOB_API_URL=https://api.ibm.com/bob/v1
```

**Expected API Format:**
```http
POST https://api.ibm.com/bob/v1/messages
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "model": "claude-3-sonnet",
  "max_tokens": 4000,
  "temperature": 0.7,
  "system": "You are a helpful assistant",
  "messages": [
    {"role": "user", "content": "Hello"}
  ]
}
```

---

## Advanced Features

### 1. Automatic Checkpointing

**Enable auto-checkpoints on state transitions:**

**File: `backend/app/services/state_manager.py`**
```python
async def transition_state(workflow_id, new_state):
    # Get current workflow
    workflow = await get_workflow(workflow_id)
    
    # Create checkpoint before transition
    checkpoint = await create_checkpoint(
        workflow_id=workflow_id,
        workflow_state=workflow.current_state,
        auto_created=True
    )
    
    # Perform transition
    workflow.current_state = new_state
    await save_workflow(workflow)
    
    return workflow, checkpoint
```

### 2. Context Persistence

**Store AI conversation history:**
```python
context = {
    "conversation": [
        {"role": "user", "content": "How do I implement auth?"},
        {"role": "assistant", "content": "Use JWT tokens..."}
    ],
    "decisions": ["Using JWT", "Storing tokens in httpOnly cookies"],
    "references": ["https://jwt.io/introduction"]
}

await create_checkpoint(
    workflow_id=workflow_id,
    context=context
)
```

### 3. Diff Visualization

**Compare code changes between checkpoints:**
```python
from difflib import unified_diff

def generate_diff(left_code, right_code):
    diff = unified_diff(
        left_code.splitlines(),
        right_code.splitlines(),
        lineterm=''
    )
    return '\n'.join(diff)
```

### 4. Rollback with Confirmation

**Safe rollback mechanism:**
```python
async def rollback_with_backup(workflow_id, target_state):
    # Create backup of current state
    backup = await create_checkpoint(
        workflow_id=workflow_id,
        metadata={"type": "pre_rollback_backup"}
    )
    
    # Perform rollback
    await rollback_state(workflow_id, target_state)
    
    return {"backup_id": backup.id, "rolled_back": True}
```

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Failed
**Error:** `sqlalchemy.exc.OperationalError: could not connect to server`

**Solutions:**
- Verify DATABASE_URL in `.env`
- Check Supabase credentials
- Test connection: `psql $DATABASE_URL`
- Ensure firewall allows connection

#### 2. IBM BOB API Key Invalid
**Error:** `401 Unauthorized`

**Solutions:**
- Verify IBM_BOB_API_KEY in `.env`
- Check key hasn't expired
- Ensure correct API URL
- Test with curl:
```bash
curl -H "Authorization: Bearer YOUR_KEY" \
     https://api.ibm.com/bob/v1/health
```

#### 3. Migration Errors
**Error:** `alembic.util.exc.CommandError: Can't locate revision`

**Solutions:**
```bash
# Reset migrations
rm -rf backend/alembic/versions/*.py
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

#### 4. Port Already in Use
**Error:** `OSError: [Errno 48] Address already in use`

**Solutions:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

#### 5. Frontend Can't Connect to Backend
**Error:** `Network Error` or `CORS Error`

**Solutions:**
- Verify backend is running: http://localhost:8000/health
- Check CORS settings in `backend/app/main.py`
- Ensure frontend uses correct API URL
- Check browser console for details

### Debug Mode

**Enable detailed logging:**

**File: `backend/.env`**
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

**View logs:**
```bash
# Backend logs
tail -f backend/logs/app.log

# Or in terminal where uvicorn is running
```

### Health Checks

**Verify system status:**
```bash
# Backend health
curl http://localhost:8000/health

# Database connection
curl http://localhost:8000/health/db

# BOB API status
curl http://localhost:8000/health/bob
```

---

## Best Practices

### 1. Checkpoint Naming
Use descriptive metadata:
```json
{
  "metadata": {
    "phase": "authentication_implementation",
    "feature": "JWT login",
    "git_commit": "abc123",
    "notes": "Added password hashing"
  }
}
```

### 2. Context Management
Keep context focused and relevant:
```json
{
  "context": {
    "current_task": "Implementing user registration",
    "blockers": ["Need to decide on email validation"],
    "next_steps": ["Add email verification", "Create welcome email"]
  }
}
```

### 3. State Transitions
Always validate before transitioning:
```python
# Good
if can_transition(current_state, new_state):
    await transition_state(workflow_id, new_state)
else:
    raise InvalidTransitionError()

# Bad
await transition_state(workflow_id, new_state)  # No validation
```

### 4. Error Handling
Provide context in error messages:
```python
try:
    await create_checkpoint(...)
except Exception as e:
    logger.error(f"Checkpoint creation failed: {e}", extra={
        "workflow_id": workflow_id,
        "state": current_state
    })
    raise
```

---

## Next Steps

### Extend the System

**1. Add Authentication:**
- Implement user login/signup
- Protect API endpoints
- Add user-specific projects

**2. Add Collaboration:**
- Share projects with team members
- Real-time updates via WebSockets
- Comment on checkpoints

**3. Add Integrations:**
- GitHub integration for code sync
- Slack notifications for state changes
- Jira integration for task tracking

**4. Add Analytics:**
- Track time spent in each state
- Measure debugging efficiency
- Generate progress reports

### Learn More

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org
- **React Docs**: https://react.dev
- **IBM BOB Docs**: [Your IBM BOB documentation]

---

## Support

**Need Help?**
- 📧 Email: support@devflow.ai
- 💬 Discord: discord.gg/devflow
- 📚 Docs: docs.devflow.ai
- 🐛 Issues: github.com/devflow/issues

---

**Happy Coding! 🚀**