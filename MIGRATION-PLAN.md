# DevFlow Checkpoint AI - Migration Plan

## Current State Analysis

### Existing Implementation
The project currently has:
- ✅ FastAPI backend with API routes structure
- ✅ Pydantic schemas for data validation
- ✅ Service layer architecture (checkpoint, project, workflow, BOB services)
- ✅ BOB orchestrator with planning, debugging, and testing agents
- ✅ React frontend with TypeScript
- ✅ Docker setup
- ❌ **JSON file storage** (needs PostgreSQL migration)
- ❌ **Mock BOB responses** (needs real IBM BOB/Anthropic integration)

### Architecture Gaps

| Component | Planned | Current | Status |
|-----------|---------|---------|--------|
| Database | PostgreSQL + Redis | JSON file | ❌ Missing |
| ORM | SQLAlchemy | None | ❌ Missing |
| Migrations | Alembic | None | ❌ Missing |
| BOB Integration | Anthropic Claude API | Mock responses | ❌ Missing |
| Context Persistence | PostgreSQL + Redis | JSON file | ❌ Missing |
| Auto Checkpoints | On milestone transitions | Manual only | ❌ Missing |
| Database Models | Full schema | None | ❌ Missing |

## Migration Strategy

### Phase 1: Database Infrastructure Setup

#### 1.1 Add Required Dependencies
```python
# Add to requirements.txt
sqlalchemy==2.0.23
alembic==1.13.1
psycopg2-binary==2.9.9
asyncpg==0.29.0
redis==5.0.1
anthropic==0.8.1
```

#### 1.2 Update Configuration
```python
# backend/app/config.py - Add database settings
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://devflow_user:devflow_pass@localhost:5432/devflow_db"
)
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
BOB_MODEL: str = os.getenv("BOB_MODEL", "claude-3-5-sonnet-20241022")
BOB_MAX_TOKENS: int = int(os.getenv("BOB_MAX_TOKENS", "100000"))
BOB_TEMPERATURE: float = float(os.getenv("BOB_TEMPERATURE", "0.7"))
```

#### 1.3 Create Database Connection Module
```python
# backend/app/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_async_engine(settings.DATABASE_URL, echo=settings.debug)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
```

### Phase 2: Database Models Implementation

#### 2.1 Create SQLAlchemy Models

**Projects Model**
```python
# backend/app/models/project.py
from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    tech_stack = Column(JSON)
    status = Column(String(50), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    checkpoints = relationship("Checkpoint", back_populates="project", cascade="all, delete-orphan")
    workflows = relationship("Workflow", back_populates="project", cascade="all, delete-orphan")
```

**Checkpoints Model**
```python
# backend/app/models/checkpoint.py
class Checkpoint(Base):
    __tablename__ = "checkpoints"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    milestone = Column(String(50), nullable=False)
    state_data = Column(JSON, nullable=False)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    project = relationship("Project", back_populates="checkpoints")
    
    # Indexes
    __table_args__ = (
        Index('idx_checkpoints_project', 'project_id'),
        Index('idx_checkpoints_milestone', 'milestone'),
    )
```

**Workflows Model**
```python
# backend/app/models/workflow.py
class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    current_state = Column(String(50), nullable=False, default="plan")
    context = Column(JSON, nullable=False, default={})
    state_history = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="workflows")
    
    # Indexes
    __table_args__ = (
        Index('idx_workflows_project', 'project_id'),
    )
```

**Users Model** (for future authentication)
```python
# backend/app/models/user.py
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

#### 2.2 Initialize Alembic
```bash
cd backend
alembic init alembic
```

#### 2.3 Create Initial Migration
```python
# alembic/versions/001_initial_schema.py
"""Initial schema

Revision ID: 001
Create Date: 2024-01-01 00:00:00
"""

def upgrade():
    # Create tables
    op.create_table('users', ...)
    op.create_table('projects', ...)
    op.create_table('checkpoints', ...)
    op.create_table('workflows', ...)

def downgrade():
    op.drop_table('workflows')
    op.drop_table('checkpoints')
    op.drop_table('projects')
    op.drop_table('users')
```

### Phase 3: Service Layer Migration

#### 3.1 Update Services to Use SQLAlchemy

**Project Service**
```python
# backend/app/services/project_service.py
class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_project(self, project_data: ProjectCreate) -> Project:
        project = Project(**project_data.dict())
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project
    
    async def get_project(self, project_id: UUID) -> Optional[Project]:
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()
```

**Checkpoint Service**
```python
# backend/app/services/checkpoint_service.py
class CheckpointService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_checkpoint(
        self,
        project_id: UUID,
        milestone: str,
        state_data: dict,
        metadata: dict
    ) -> Checkpoint:
        checkpoint = Checkpoint(
            project_id=project_id,
            milestone=milestone,
            state_data=state_data,
            metadata=metadata
        )
        self.db.add(checkpoint)
        await self.db.commit()
        await self.db.refresh(checkpoint)
        return checkpoint
```

**Workflow Service with Auto-Checkpoint**
```python
# backend/app/services/state_manager.py
class WorkflowStateManager:
    def __init__(self, db: AsyncSession, checkpoint_service: CheckpointService):
        self.db = db
        self.checkpoint_service = checkpoint_service
    
    async def transition_state(
        self,
        workflow_id: UUID,
        target_state: str,
        auto_checkpoint: bool = True
    ) -> Workflow:
        # Get workflow
        workflow = await self.get_workflow(workflow_id)
        
        # Validate transition
        if not self.validate_transition(workflow.current_state, target_state):
            raise ValueError(f"Invalid transition: {workflow.current_state} -> {target_state}")
        
        # Create checkpoint before transition
        if auto_checkpoint:
            await self.checkpoint_service.create_checkpoint(
                project_id=workflow.project_id,
                milestone=workflow.current_state,
                state_data=workflow.context,
                metadata={
                    "transition_from": workflow.current_state,
                    "transition_to": target_state,
                    "auto_created": True
                }
            )
        
        # Update workflow state
        workflow.current_state = target_state
        workflow.state_history.append({
            "state": target_state,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        await self.db.commit()
        await self.db.refresh(workflow)
        return workflow
```

### Phase 4: IBM BOB Integration

#### 4.1 Update BOB Orchestrator with Anthropic API

```python
# backend/app/services/bob/orchestrator.py
import anthropic
from anthropic import AsyncAnthropic

class BOBOrchestrator:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        self.context_manager = ContextManager()
        self.planning_agent = PlanningAgent(self.client)
        self.debugging_agent = DebuggingAgent(self.client)
        self.testing_agent = TestingAgent(self.client)
    
    async def plan_milestones(
        self,
        project_description: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        return await self.planning_agent.run(project_description, context)
    
    async def stream_response(
        self,
        prompt: str,
        context: Dict[str, Any]
    ) -> AsyncGenerator[str, None]:
        # Build system prompt with context
        system_prompt = self._build_system_prompt(context)
        
        # Stream from Claude
        async with self.client.messages.stream(
            model=settings.bob_model,
            max_tokens=settings.bob_max_tokens,
            temperature=settings.bob_temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            async for text in stream.text_stream:
                yield f"data: {text}\n\n"
```

#### 4.2 Update Planning Agent

```python
# backend/app/services/bob/planning_agent.py
class PlanningAgent:
    def __init__(self, client: AsyncAnthropic):
        self.client = client
    
    async def run(
        self,
        project_description: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        system_prompt = """You are IBM BOB, an AI architect specializing in breaking down 
        software projects into structured, checkpoint-based milestones. Analyze the project 
        description and create a detailed plan with milestones, deliverables, and risks."""
        
        user_prompt = f"""
        Project Description: {project_description}
        
        Context: {json.dumps(context, indent=2)}
        
        Please create a detailed project plan with:
        1. 5-8 milestones with clear goals
        2. Deliverables for each milestone
        3. Potential risks and mitigation strategies
        4. Recommended technology stack
        
        Return the response in JSON format.
        """
        
        response = await self.client.messages.create(
            model=settings.bob_model,
            max_tokens=settings.bob_max_tokens,
            temperature=settings.bob_temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        # Parse response
        content = response.content[0].text
        try:
            plan_data = json.loads(content)
        except json.JSONDecodeError:
            # Fallback if response isn't valid JSON
            plan_data = {
                "agent": "planning",
                "mode": "ibm-bob",
                "raw_response": content,
                "milestones": []
            }
        
        return plan_data
```

#### 4.3 Update Debugging Agent

```python
# backend/app/services/bob/debugging_agent.py
class DebuggingAgent:
    def __init__(self, client: AsyncAnthropic):
        self.client = client
    
    async def run(
        self,
        code: str,
        error: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        system_prompt = """You are IBM BOB, an expert debugging assistant. Analyze code 
        errors and provide clear, actionable solutions with step-by-step fixes."""
        
        user_prompt = f"""
        Code:
        ```
        {code}
        ```
        
        Error:
        {error}
        
        Context: {json.dumps(context, indent=2)}
        
        Please provide:
        1. Root cause analysis
        2. Step-by-step fix instructions
        3. Preventive measures
        4. Code examples if applicable
        
        Return the response in JSON format with fields: diagnosis, suggestions, fixes.
        """
        
        response = await self.client.messages.create(
            model=settings.bob_model,
            max_tokens=settings.bob_max_tokens,
            temperature=settings.bob_temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        content = response.content[0].text
        try:
            debug_data = json.loads(content)
        except json.JSONDecodeError:
            debug_data = {
                "agent": "debugging",
                "mode": "ibm-bob",
                "raw_response": content
            }
        
        return debug_data
```

#### 4.4 Update Testing Agent

```python
# backend/app/services/bob/testing_agent.py
class TestingAgent:
    def __init__(self, client: AsyncAnthropic):
        self.client = client
    
    async def run(
        self,
        code: str,
        test_type: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        system_prompt = """You are IBM BOB, a testing expert. Generate comprehensive 
        test cases and test code for the provided code."""
        
        user_prompt = f"""
        Code to test:
        ```
        {code}
        ```
        
        Test Type: {test_type}
        Context: {json.dumps(context, indent=2)}
        
        Please generate:
        1. Test cases covering happy paths, edge cases, and error scenarios
        2. Actual test code (pytest format)
        3. Test data fixtures
        4. Assertions and expected outcomes
        
        Return the response in JSON format with fields: test_cases, test_code, fixtures.
        """
        
        response = await self.client.messages.create(
            model=settings.bob_model,
            max_tokens=settings.bob_max_tokens,
            temperature=settings.bob_temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        content = response.content[0].text
        try:
            test_data = json.loads(content)
        except json.JSONDecodeError:
            test_data = {
                "agent": "testing",
                "mode": "ibm-bob",
                "raw_response": content
            }
        
        return test_data
```

#### 4.5 Update Context Manager with Redis

```python
# backend/app/services/bob/context_manager.py
import redis.asyncio as redis
import json

class ContextManager:
    def __init__(self):
        self.redis_client = redis.from_url(settings.redis_url)
        self.cache_ttl = 3600  # 1 hour
    
    async def save_context(
        self,
        workflow_id: str,
        context_data: Dict[str, Any]
    ) -> None:
        # Save to Redis for quick access
        await self.redis_client.setex(
            f"context:{workflow_id}",
            self.cache_ttl,
            json.dumps(context_data)
        )
        
        # Also save to PostgreSQL for persistence
        # (via workflow update in database)
    
    async def load_context(self, workflow_id: str) -> Dict[str, Any]:
        # Try Redis first
        cached = await self.redis_client.get(f"context:{workflow_id}")
        if cached:
            return json.loads(cached)
        
        # Fallback to database
        # (load from workflow in database)
        return {}
```

### Phase 5: API Updates

#### 5.1 Update API Dependencies

```python
# backend/app/api/deps.py
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db():
        yield session
```

#### 5.2 Update API Endpoints

```python
# backend/app/api/v1/projects.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...api.deps import get_db_session

@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db_session)
):
    service = ProjectService(db)
    result = await service.create_project(project)
    return result
```

### Phase 6: Environment Configuration

#### 6.1 Update .env.example

```env
# Application
APP_NAME=DevFlow Checkpoint AI
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql+asyncpg://devflow_user:devflow_pass@localhost:5432/devflow_db
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_TTL=3600

# CORS
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# IBM BOB / Anthropic
ANTHROPIC_API_KEY=your-api-key-here
BOB_MODEL=claude-3-5-sonnet-20241022
BOB_MAX_TOKENS=100000
BOB_TEMPERATURE=0.7
BOB_STREAMING=true

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### Phase 7: Testing Strategy

#### 7.1 Database Tests
```python
# tests/test_database.py
@pytest.fixture
async def db_session():
    # Create test database
    async with async_session_maker() as session:
        yield session
        await session.rollback()

async def test_create_project(db_session):
    service = ProjectService(db_session)
    project = await service.create_project(ProjectCreate(
        name="Test Project",
        description="Test"
    ))
    assert project.id is not None
```

#### 7.2 BOB Integration Tests
```python
# tests/test_bob_integration.py
@pytest.mark.asyncio
async def test_planning_agent():
    orchestrator = BOBOrchestrator()
    result = await orchestrator.plan_milestones(
        "Build a todo app",
        {"focus": "MVP"}
    )
    assert "milestones" in result
    assert len(result["milestones"]) > 0
```

## Migration Execution Plan

### Step-by-Step Execution

1. **Backup Current Data**
   ```bash
   cp data/devflow.json data/devflow.json.backup
   ```

2. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Setup PostgreSQL**
   ```bash
   # Create database
   psql -U postgres
   CREATE DATABASE devflow_db;
   CREATE USER devflow_user WITH PASSWORD 'devflow_pass';
   GRANT ALL PRIVILEGES ON DATABASE devflow_db TO devflow_user;
   ```

4. **Run Migrations**
   ```bash
   alembic upgrade head
   ```

5. **Migrate Existing Data** (if needed)
   ```python
   # scripts/migrate_json_to_postgres.py
   # Read from JSON, insert into PostgreSQL
   ```

6. **Test Database Connection**
   ```bash
   python -c "from app.database import engine; print('Connected!')"
   ```

7. **Configure BOB API Key**
   ```bash
   # Add to .env
   ANTHROPIC_API_KEY=your-actual-key
   ```

8. **Test BOB Integration**
   ```bash
   pytest tests/test_bob_integration.py -v
   ```

9. **Run Full Test Suite**
   ```bash
   pytest tests/ -v --cov=app
   ```

10. **Start Application**
    ```bash
    uvicorn app.main:app --reload
    ```

## Rollback Plan

If migration fails:

1. **Restore JSON Storage**
   ```bash
   cp data/devflow.json.backup data/devflow.json
   git checkout backend/app/storage.py
   ```

2. **Revert Dependencies**
   ```bash
   git checkout backend/requirements.txt
   pip install -r requirements.txt
   ```

3. **Remove Database Changes**
   ```bash
   alembic downgrade base
   ```

## Success Criteria

- ✅ All API endpoints work with PostgreSQL
- ✅ BOB returns real AI-generated responses
- ✅ Checkpoints auto-create on state transitions
- ✅ Context persists across sessions
- ✅ All tests pass
- ✅ Frontend continues working without changes
- ✅ No hardcoded credentials in code

## Timeline Estimate

- **Phase 1-2**: Database setup and models (2-3 hours)
- **Phase 3**: Service migration (3-4 hours)
- **Phase 4**: BOB integration (4-5 hours)
- **Phase 5-6**: API and config updates (2-3 hours)
- **Phase 7**: Testing and validation (2-3 hours)

**Total**: 13-18 hours of development time

---

**Ready to proceed with implementation in Code mode.**