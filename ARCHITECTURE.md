# DevFlow Checkpoint AI - Architecture Plan

## Project Overview
DevFlow Checkpoint AI is a stateful development workflow system that saves structured snapshots after each milestone (plan → code → debug → test). It uses IBM BOB as the AI orchestrator to maintain context across sessions and enable seamless recovery from crashes or tool switches.

## Technology Stack
- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: React 18+ with TypeScript
- **Database**: PostgreSQL (primary) + Redis (caching/sessions)
- **AI Integration**: IBM BOB (Anthropic Claude API) as orchestration layer
- **State Management**: Redux Toolkit (frontend) + SQLAlchemy (backend)
- **Testing**: pytest (backend), Jest + React Testing Library (frontend)

## System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Dashboard   │  │  Checkpoint  │  │   Workflow   │     │
│  │   View       │  │   Manager    │  │   Editor     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                    REST API (JSON)
                            │
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              BOB AI Orchestrator                     │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐    │  │
│  │  │  Planning  │  │  Debugging │  │   Testing  │    │  │
│  │  │   Agent    │  │   Agent    │  │   Agent    │    │  │
│  │  └────────────┘  └────────────┘  └────────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Checkpoint State Manager                     │  │
│  │  - Snapshot Creation    - Context Persistence        │  │
│  │  - State Recovery       - Version Control            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
┌───────▼────────┐                    ┌────────▼────────┐
│   PostgreSQL   │                    │     Redis       │
│  (Checkpoints) │                    │  (Cache/Queue)  │
└────────────────┘                    └─────────────────┘
```

## Milestones

### Milestone 1: Project Foundation & Setup
**Deliverables**:
- Project scaffolding with proper directory structure
- Development environment configuration
- Database setup and migrations
- Basic FastAPI server with health check endpoint
- React app initialization with routing

### Milestone 2: Checkpoint State Management System
**Deliverables**:
- Database schema for checkpoints and workflow states
- Checkpoint creation and retrieval APIs
- State serialization/deserialization logic
- Version control for checkpoint history
- Checkpoint diff calculation

### Milestone 3: BOB AI Orchestrator Integration
**Deliverables**:
- BOB service layer with Anthropic Claude API integration
- Planning agent for milestone breakdown
- Debugging agent for error analysis
- Testing agent for test generation
- Context management and prompt engineering
- AI response streaming support

### Milestone 4: Workflow State Machine
**Deliverables**:
- State machine implementation (plan → code → debug → test)
- Transition validation and guards
- Automatic checkpoint triggers
- Workflow progress tracking
- State rollback capabilities

### Milestone 5: REST API Development
**Deliverables**:
- Complete CRUD operations for projects and checkpoints
- Workflow management endpoints
- BOB AI interaction endpoints
- File upload/download for code artifacts
- WebSocket support for real-time updates

### Milestone 6: Frontend Development
**Deliverables**:
- Dashboard with project overview
- Checkpoint timeline visualization
- Workflow editor with code preview
- BOB chat interface
- Real-time status updates
- Responsive design

### Milestone 7: Testing & Documentation
**Deliverables**:
- Unit tests (80%+ coverage)
- Integration tests for API endpoints
- E2E tests for critical workflows
- API documentation (OpenAPI/Swagger)
- User guide and developer documentation

### Milestone 8: Deployment & CI/CD
**Deliverables**:
- Docker containerization
- CI/CD pipeline setup
- Production deployment configuration
- Monitoring and logging setup
- Backup and recovery procedures

## Suggested File Structure

```
devflow-checkpoint-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI application entry
│   │   ├── config.py                  # Configuration management
│   │   ├── database.py                # Database connection
│   │   │
│   │   ├── models/                    # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── project.py
│   │   │   ├── checkpoint.py
│   │   │   ├── workflow.py
│   │   │   └── user.py
│   │   │
│   │   ├── schemas/                   # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── project.py
│   │   │   ├── checkpoint.py
│   │   │   ├── workflow.py
│   │   │   └── bob.py
│   │   │
│   │   ├── api/                       # API routes
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── projects.py
│   │   │   │   ├── checkpoints.py
│   │   │   │   ├── workflows.py
│   │   │   │   └── bob.py
│   │   │   └── deps.py                # Dependencies
│   │   │
│   │   ├── services/                  # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── checkpoint_service.py
│   │   │   ├── workflow_service.py
│   │   │   ├── state_manager.py
│   │   │   └── bob/
│   │   │       ├── __init__.py
│   │   │       ├── orchestrator.py    # Main BOB orchestrator
│   │   │       ├── planning_agent.py
│   │   │       ├── debugging_agent.py
│   │   │       ├── testing_agent.py
│   │   │       └── context_manager.py
│   │   │
│   │   ├── core/                      # Core utilities
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   ├── logging.py
│   │   │   └── exceptions.py
│   │   │
│   │   └── utils/                     # Helper functions
│   │       ├── __init__.py
│   │       ├── serializers.py
│   │       ├── validators.py
│   │       └── diff_calculator.py
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_checkpoints.py
│   │   ├── test_workflows.py
│   │   └── test_bob.py
│   │
│   ├── alembic/                       # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── Dockerfile
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   │
│   ├── src/
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   │
│   │   ├── components/
│   │   │   ├── Dashboard/
│   │   │   │   ├── ProjectCard.tsx
│   │   │   │   ├── ProjectList.tsx
│   │   │   │   └── StatsOverview.tsx
│   │   │   │
│   │   │   ├── Checkpoint/
│   │   │   │   ├── CheckpointTimeline.tsx
│   │   │   │   ├── CheckpointDetail.tsx
│   │   │   │   └── CheckpointDiff.tsx
│   │   │   │
│   │   │   ├── Workflow/
│   │   │   │   ├── WorkflowEditor.tsx
│   │   │   │   ├── StateVisualization.tsx
│   │   │   │   └── CodePreview.tsx
│   │   │   │
│   │   │   ├── BOB/
│   │   │   │   ├── ChatInterface.tsx
│   │   │   │   ├── AgentStatus.tsx
│   │   │   │   └── ContextViewer.tsx
│   │   │   │
│   │   │   └── Common/
│   │   │       ├── Header.tsx
│   │   │       ├── Sidebar.tsx
│   │   │       └── LoadingSpinner.tsx
│   │   │
│   │   ├── pages/
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── ProjectPage.tsx
│   │   │   ├── CheckpointPage.tsx
│   │   │   └── WorkflowPage.tsx
│   │   │
│   │   ├── store/                     # Redux store
│   │   │   ├── index.ts
│   │   │   ├── slices/
│   │   │   │   ├── projectSlice.ts
│   │   │   │   ├── checkpointSlice.ts
│   │   │   │   ├── workflowSlice.ts
│   │   │   │   └── bobSlice.ts
│   │   │   └── api/
│   │   │       └── apiSlice.ts        # RTK Query
│   │   │
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   └── websocket.ts
│   │   │
│   │   ├── hooks/
│   │   │   ├── useCheckpoint.ts
│   │   │   ├── useWorkflow.ts
│   │   │   └── useBOB.ts
│   │   │
│   │   ├── types/
│   │   │   ├── project.ts
│   │   │   ├── checkpoint.ts
│   │   │   ├── workflow.ts
│   │   │   └── bob.ts
│   │   │
│   │   └── utils/
│   │       ├── formatters.ts
│   │       └── validators.ts
│   │
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
└── ARCHITECTURE.md
```

## Key APIs and Functions

### Backend Core APIs

#### 1. Checkpoint Management Service
```python
# backend/app/services/checkpoint_service.py

class CheckpointService:
    async def create_checkpoint(
        self,
        project_id: str,
        milestone: str,
        state_data: dict,
        metadata: dict
    ) -> Checkpoint:
        """Create a new checkpoint snapshot"""
        
    async def get_checkpoint(
        self,
        checkpoint_id: str
    ) -> Checkpoint:
        """Retrieve a specific checkpoint"""
        
    async def list_checkpoints(
        self,
        project_id: str,
        milestone: Optional[str] = None
    ) -> List[Checkpoint]:
        """List all checkpoints for a project"""
        
    async def restore_checkpoint(
        self,
        checkpoint_id: str
    ) -> dict:
        """Restore project state from checkpoint"""
        
    async def calculate_diff(
        self,
        checkpoint_id_1: str,
        checkpoint_id_2: str
    ) -> dict:
        """Calculate differences between two checkpoints"""
```

#### 2. Workflow State Manager
```python
# backend/app/services/state_manager.py

class WorkflowStateManager:
    async def initialize_workflow(
        self,
        project_id: str,
        initial_state: str = "plan"
    ) -> Workflow:
        """Initialize a new workflow"""
        
    async def transition_state(
        self,
        workflow_id: str,
        target_state: str,
        auto_checkpoint: bool = True
    ) -> Workflow:
        """Transition workflow to next state"""
        
    async def get_current_state(
        self,
        workflow_id: str
    ) -> dict:
        """Get current workflow state and context"""
        
    async def rollback_state(
        self,
        workflow_id: str,
        target_checkpoint_id: str
    ) -> Workflow:
        """Rollback workflow to previous checkpoint"""
        
    def validate_transition(
        self,
        current_state: str,
        target_state: str
    ) -> bool:
        """Validate if state transition is allowed"""
```

#### 3. BOB AI Orchestrator
```python
# backend/app/services/bob/orchestrator.py

class BOBOrchestrator:
    async def plan_milestones(
        self,
        project_description: str,
        context: dict
    ) -> dict:
        """Generate project milestones and breakdown"""
        
    async def debug_code(
        self,
        code: str,
        error: str,
        context: dict
    ) -> dict:
        """Analyze and suggest fixes for errors"""
        
    async def generate_tests(
        self,
        code: str,
        test_type: str,
        context: dict
    ) -> dict:
        """Generate test cases for code"""
        
    async def maintain_context(
        self,
        workflow_id: str,
        new_data: dict
    ) -> None:
        """Update and persist workflow context"""
        
    async def stream_response(
        self,
        prompt: str,
        context: dict
    ) -> AsyncGenerator[str, None]:
        """Stream AI responses in real-time"""
```

#### 4. Context Manager
```python
# backend/app/services/bob/context_manager.py

class ContextManager:
    async def save_context(
        self,
        workflow_id: str,
        context_data: dict
    ) -> None:
        """Persist workflow context"""
        
    async def load_context(
        self,
        workflow_id: str
    ) -> dict:
        """Load workflow context"""
        
    async def merge_contexts(
        self,
        base_context: dict,
        new_context: dict
    ) -> dict:
        """Merge context from different sources"""
        
    def compress_context(
        self,
        context: dict,
        max_tokens: int = 100000
    ) -> dict:
        """Compress context to fit token limits"""
```

### REST API Endpoints

#### Projects
- `POST /api/v1/projects` - Create new project
- `GET /api/v1/projects` - List all projects
- `GET /api/v1/projects/{project_id}` - Get project details
- `PUT /api/v1/projects/{project_id}` - Update project
- `DELETE /api/v1/projects/{project_id}` - Delete project

#### Checkpoints
- `POST /api/v1/checkpoints` - Create checkpoint
- `GET /api/v1/checkpoints/{checkpoint_id}` - Get checkpoint
- `GET /api/v1/projects/{project_id}/checkpoints` - List project checkpoints
- `POST /api/v1/checkpoints/{checkpoint_id}/restore` - Restore checkpoint
- `GET /api/v1/checkpoints/diff` - Compare checkpoints

#### Workflows
- `POST /api/v1/workflows` - Initialize workflow
- `GET /api/v1/workflows/{workflow_id}` - Get workflow state
- `POST /api/v1/workflows/{workflow_id}/transition` - Transition state
- `POST /api/v1/workflows/{workflow_id}/rollback` - Rollback workflow
- `GET /api/v1/workflows/{workflow_id}/history` - Get workflow history

#### BOB AI
- `POST /api/v1/bob/plan` - Generate project plan
- `POST /api/v1/bob/debug` - Debug code with BOB
- `POST /api/v1/bob/test` - Generate tests
- `POST /api/v1/bob/chat` - Chat with BOB
- `GET /api/v1/bob/stream` - Stream AI responses (WebSocket)

### Frontend Key Components

#### 1. Checkpoint Timeline Component
```typescript
// frontend/src/components/Checkpoint/CheckpointTimeline.tsx

interface CheckpointTimelineProps {
  projectId: string;
  onCheckpointSelect: (checkpointId: string) => void;
}

export const CheckpointTimeline: React.FC<CheckpointTimelineProps> = ({
  projectId,
  onCheckpointSelect
}) => {
  // Visualize checkpoints in chronological order
  // Show milestone markers (plan, code, debug, test)
  // Enable checkpoint comparison
  // Support restore functionality
};
```

#### 2. Workflow State Visualization
```typescript
// frontend/src/components/Workflow/StateVisualization.tsx

interface StateVisualizationProps {
  workflowId: string;
  currentState: string;
  onStateTransition: (targetState: string) => void;
}

export const StateVisualization: React.FC<StateVisualizationProps> = ({
  workflowId,
  currentState,
  onStateTransition
}) => {
  // Display state machine diagram
  // Highlight current state
  // Show available transitions
  // Enable state navigation
};
```

#### 3. BOB Chat Interface
```typescript
// frontend/src/components/BOB/ChatInterface.tsx

interface ChatInterfaceProps {
  workflowId: string;
  context: WorkflowContext;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  workflowId,
  context
}) => {
  // Real-time chat with BOB
  // Stream AI responses
  // Display agent status
  // Show context awareness
  // Support code snippets and formatting
};
```

### Database Schema

#### Checkpoints Table
```sql
CREATE TABLE checkpoints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id),
    milestone VARCHAR(50) NOT NULL,
    state_data JSONB NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

CREATE INDEX idx_checkpoints_project ON checkpoints(project_id);
CREATE INDEX idx_checkpoints_milestone ON checkpoints(milestone);
```

#### Workflows Table
```sql
CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id),
    current_state VARCHAR(50) NOT NULL,
    context JSONB NOT NULL,
    state_history JSONB[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_workflows_project ON workflows(project_id);
```

#### Projects Table
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    tech_stack JSONB,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## BOB Integration Strategy

### Hybrid Architecture Approach
BOB will be implemented as a **service layer within the FastAPI backend** with the following characteristics:

1. **Embedded Module**: Core BOB logic lives in `backend/app/services/bob/`
2. **API Gateway**: External AI calls (Anthropic Claude) managed through dedicated service
3. **Context Persistence**: Redis for short-term context, PostgreSQL for long-term storage
4. **Agent Specialization**: Separate agents for planning, debugging, and testing
5. **Streaming Support**: WebSocket connections for real-time AI responses

### Why Hybrid?
- **Performance**: Embedded logic reduces latency for context management
- **Scalability**: Can be extracted to microservice if needed
- **Simplicity**: Single deployment unit for MVP
- **Flexibility**: Easy to add external AI providers

## Development Workflow

### Phase 1: Foundation
1. Set up project structure
2. Configure development environment
3. Initialize database and migrations
4. Create basic FastAPI endpoints
5. Set up React app with routing

### Phase 2: Core Features
1. Implement checkpoint system
2. Build workflow state machine
3. Integrate BOB orchestrator
4. Develop REST APIs
5. Create frontend components

### Phase 3: Integration
1. Connect frontend to backend
2. Implement real-time updates
3. Add error handling
4. Optimize performance
5. Conduct integration testing

### Phase 4: Polish
1. Write comprehensive tests
2. Create documentation
3. Set up CI/CD pipeline
4. Deploy to staging
5. User acceptance testing

## Success Metrics

1. **Checkpoint Recovery**: < 2 seconds to restore any checkpoint
2. **Context Persistence**: 100% context retention across sessions
3. **AI Response Time**: < 5 seconds for BOB responses
4. **System Uptime**: 99.9% availability
5. **Test Coverage**: > 80% code coverage

## Next Steps

1. Review and approve this architecture plan
2. Set up development environment
3. Create initial project scaffolding
4. Begin Milestone 1 implementation
5. Establish regular checkpoint reviews

---

**Note**: This architecture is designed to be flexible and can be adjusted based on feedback and evolving requirements.