# DevFlow Checkpoint AI - Project Plan (JSON Format)

```json
{
  "project_name": "DevFlow Checkpoint AI",
  "description": "A stateful development workflow system powered by IBM BOB that saves structured snapshots after each milestone (plan → code → debug → test). Enables seamless recovery from crashes or tool switches by resuming from the last checkpoint.",
  "technology_stack": {
    "backend": {
      "language": "Python 3.11+",
      "framework": "FastAPI",
      "orm": "SQLAlchemy",
      "async": "asyncio"
    },
    "frontend": {
      "language": "TypeScript",
      "framework": "React 18+",
      "state_management": "Redux Toolkit",
      "api_client": "RTK Query"
    },
    "database": {
      "primary": "PostgreSQL",
      "cache": "Redis"
    },
    "ai_integration": {
      "orchestrator": "IBM BOB",
      "provider": "Anthropic Claude API",
      "architecture": "Hybrid (Embedded + API)"
    },
    "testing": {
      "backend": "pytest",
      "frontend": "Jest + React Testing Library"
    },
    "deployment": {
      "containerization": "Docker",
      "orchestration": "Docker Compose",
      "ci_cd": "GitHub Actions"
    }
  },
  "milestones": [
    {
      "id": 1,
      "name": "Project Foundation & Setup",
      "description": "Establish project structure and development environment",
      "deliverables": [
        "Project scaffolding with proper directory structure",
        "Development environment configuration",
        "Database setup and migrations",
        "Basic FastAPI server with health check endpoint",
        "React app initialization with routing"
      ],
      "dependencies": [],
      "success_criteria": [
        "Backend server runs successfully",
        "Frontend app loads without errors",
        "Database connection established",
        "Development environment documented"
      ]
    },
    {
      "id": 2,
      "name": "Checkpoint State Management System",
      "description": "Build core checkpoint creation and recovery system",
      "deliverables": [
        "Database schema for checkpoints and workflow states",
        "Checkpoint creation and retrieval APIs",
        "State serialization/deserialization logic",
        "Version control for checkpoint history",
        "Checkpoint diff calculation"
      ],
      "dependencies": [1],
      "success_criteria": [
        "Checkpoints can be created and stored",
        "State can be restored from any checkpoint",
        "Diff calculation works between checkpoints",
        "Version history is maintained"
      ]
    },
    {
      "id": 3,
      "name": "BOB AI Orchestrator Integration",
      "description": "Integrate IBM BOB as the AI orchestration layer",
      "deliverables": [
        "BOB service layer with Anthropic Claude API integration",
        "Planning agent for milestone breakdown",
        "Debugging agent for error analysis",
        "Testing agent for test generation",
        "Context management and prompt engineering",
        "AI response streaming support"
      ],
      "dependencies": [1],
      "success_criteria": [
        "BOB can generate project plans",
        "BOB can analyze and debug code",
        "BOB can generate test cases",
        "Context is maintained across sessions",
        "Streaming responses work correctly"
      ]
    },
    {
      "id": 4,
      "name": "Workflow State Machine",
      "description": "Implement the plan → code → debug → test workflow",
      "deliverables": [
        "State machine implementation (plan → code → debug → test)",
        "Transition validation and guards",
        "Automatic checkpoint triggers",
        "Workflow progress tracking",
        "State rollback capabilities"
      ],
      "dependencies": [2],
      "success_criteria": [
        "State transitions work correctly",
        "Invalid transitions are blocked",
        "Checkpoints are auto-created on transitions",
        "Rollback functionality works",
        "Progress is tracked accurately"
      ]
    },
    {
      "id": 5,
      "name": "REST API Development",
      "description": "Build comprehensive REST API for all operations",
      "deliverables": [
        "Complete CRUD operations for projects and checkpoints",
        "Workflow management endpoints",
        "BOB AI interaction endpoints",
        "File upload/download for code artifacts",
        "WebSocket support for real-time updates"
      ],
      "dependencies": [2, 3, 4],
      "success_criteria": [
        "All endpoints are functional",
        "API documentation is complete",
        "WebSocket connections are stable",
        "File operations work correctly",
        "Error handling is comprehensive"
      ]
    },
    {
      "id": 6,
      "name": "Frontend Development",
      "description": "Build React frontend with all user interfaces",
      "deliverables": [
        "Dashboard with project overview",
        "Checkpoint timeline visualization",
        "Workflow editor with code preview",
        "BOB chat interface",
        "Real-time status updates",
        "Responsive design"
      ],
      "dependencies": [5],
      "success_criteria": [
        "All components render correctly",
        "Real-time updates work",
        "UI is responsive on all devices",
        "BOB chat is functional",
        "Timeline visualization is clear"
      ]
    },
    {
      "id": 7,
      "name": "Testing & Documentation",
      "description": "Comprehensive testing and documentation",
      "deliverables": [
        "Unit tests (80%+ coverage)",
        "Integration tests for API endpoints",
        "E2E tests for critical workflows",
        "API documentation (OpenAPI/Swagger)",
        "User guide and developer documentation"
      ],
      "dependencies": [6],
      "success_criteria": [
        "Test coverage exceeds 80%",
        "All critical paths are tested",
        "Documentation is complete",
        "API docs are auto-generated",
        "User guide is comprehensive"
      ]
    },
    {
      "id": 8,
      "name": "Deployment & CI/CD",
      "description": "Production deployment and automation",
      "deliverables": [
        "Docker containerization",
        "CI/CD pipeline setup",
        "Production deployment configuration",
        "Monitoring and logging setup",
        "Backup and recovery procedures"
      ],
      "dependencies": [7],
      "success_criteria": [
        "Application runs in containers",
        "CI/CD pipeline is automated",
        "Monitoring is active",
        "Backups are scheduled",
        "Recovery procedures are tested"
      ]
    }
  ],
  "file_structure": {
    "backend": {
      "app": {
        "main.py": "FastAPI application entry point",
        "config.py": "Configuration management",
        "database.py": "Database connection and session management",
        "models": {
          "project.py": "Project SQLAlchemy model",
          "checkpoint.py": "Checkpoint SQLAlchemy model",
          "workflow.py": "Workflow SQLAlchemy model",
          "user.py": "User SQLAlchemy model"
        },
        "schemas": {
          "project.py": "Project Pydantic schemas",
          "checkpoint.py": "Checkpoint Pydantic schemas",
          "workflow.py": "Workflow Pydantic schemas",
          "bob.py": "BOB AI Pydantic schemas"
        },
        "api": {
          "v1": {
            "projects.py": "Project CRUD endpoints",
            "checkpoints.py": "Checkpoint management endpoints",
            "workflows.py": "Workflow state endpoints",
            "bob.py": "BOB AI interaction endpoints"
          },
          "deps.py": "Dependency injection"
        },
        "services": {
          "checkpoint_service.py": "Checkpoint business logic",
          "workflow_service.py": "Workflow management logic",
          "state_manager.py": "State machine implementation",
          "bob": {
            "orchestrator.py": "Main BOB orchestrator",
            "planning_agent.py": "Planning agent implementation",
            "debugging_agent.py": "Debugging agent implementation",
            "testing_agent.py": "Testing agent implementation",
            "context_manager.py": "Context persistence and management"
          }
        },
        "core": {
          "security.py": "Authentication and authorization",
          "logging.py": "Logging configuration",
          "exceptions.py": "Custom exceptions"
        },
        "utils": {
          "serializers.py": "Data serialization utilities",
          "validators.py": "Input validation utilities",
          "diff_calculator.py": "Checkpoint diff calculation"
        }
      },
      "tests": {
        "conftest.py": "pytest configuration and fixtures",
        "test_checkpoints.py": "Checkpoint tests",
        "test_workflows.py": "Workflow tests",
        "test_bob.py": "BOB AI tests"
      },
      "alembic": {
        "versions": "Database migration versions",
        "env.py": "Alembic environment configuration"
      }
    },
    "frontend": {
      "src": {
        "App.tsx": "Main application component",
        "index.tsx": "Application entry point",
        "components": {
          "Dashboard": {
            "ProjectCard.tsx": "Project card component",
            "ProjectList.tsx": "Project list component",
            "StatsOverview.tsx": "Statistics overview component"
          },
          "Checkpoint": {
            "CheckpointTimeline.tsx": "Timeline visualization",
            "CheckpointDetail.tsx": "Checkpoint detail view",
            "CheckpointDiff.tsx": "Diff visualization"
          },
          "Workflow": {
            "WorkflowEditor.tsx": "Workflow editor component",
            "StateVisualization.tsx": "State machine visualization",
            "CodePreview.tsx": "Code preview component"
          },
          "BOB": {
            "ChatInterface.tsx": "BOB chat interface",
            "AgentStatus.tsx": "Agent status display",
            "ContextViewer.tsx": "Context viewer component"
          },
          "Common": {
            "Header.tsx": "Application header",
            "Sidebar.tsx": "Navigation sidebar",
            "LoadingSpinner.tsx": "Loading indicator"
          }
        },
        "pages": {
          "DashboardPage.tsx": "Dashboard page",
          "ProjectPage.tsx": "Project detail page",
          "CheckpointPage.tsx": "Checkpoint page",
          "WorkflowPage.tsx": "Workflow page"
        },
        "store": {
          "index.ts": "Redux store configuration",
          "slices": {
            "projectSlice.ts": "Project state slice",
            "checkpointSlice.ts": "Checkpoint state slice",
            "workflowSlice.ts": "Workflow state slice",
            "bobSlice.ts": "BOB AI state slice"
          },
          "api": {
            "apiSlice.ts": "RTK Query API slice"
          }
        },
        "services": {
          "api.ts": "API client configuration",
          "websocket.ts": "WebSocket client"
        },
        "hooks": {
          "useCheckpoint.ts": "Checkpoint custom hook",
          "useWorkflow.ts": "Workflow custom hook",
          "useBOB.ts": "BOB AI custom hook"
        },
        "types": {
          "project.ts": "Project TypeScript types",
          "checkpoint.ts": "Checkpoint TypeScript types",
          "workflow.ts": "Workflow TypeScript types",
          "bob.ts": "BOB AI TypeScript types"
        },
        "utils": {
          "formatters.ts": "Data formatting utilities",
          "validators.ts": "Input validation utilities"
        }
      }
    }
  },
  "key_apis": {
    "backend_services": [
      {
        "name": "CheckpointService",
        "file": "backend/app/services/checkpoint_service.py",
        "methods": [
          {
            "name": "create_checkpoint",
            "description": "Create a new checkpoint snapshot",
            "parameters": ["project_id", "milestone", "state_data", "metadata"],
            "returns": "Checkpoint"
          },
          {
            "name": "get_checkpoint",
            "description": "Retrieve a specific checkpoint",
            "parameters": ["checkpoint_id"],
            "returns": "Checkpoint"
          },
          {
            "name": "list_checkpoints",
            "description": "List all checkpoints for a project",
            "parameters": ["project_id", "milestone (optional)"],
            "returns": "List[Checkpoint]"
          },
          {
            "name": "restore_checkpoint",
            "description": "Restore project state from checkpoint",
            "parameters": ["checkpoint_id"],
            "returns": "dict"
          },
          {
            "name": "calculate_diff",
            "description": "Calculate differences between two checkpoints",
            "parameters": ["checkpoint_id_1", "checkpoint_id_2"],
            "returns": "dict"
          }
        ]
      },
      {
        "name": "WorkflowStateManager",
        "file": "backend/app/services/state_manager.py",
        "methods": [
          {
            "name": "initialize_workflow",
            "description": "Initialize a new workflow",
            "parameters": ["project_id", "initial_state"],
            "returns": "Workflow"
          },
          {
            "name": "transition_state",
            "description": "Transition workflow to next state",
            "parameters": ["workflow_id", "target_state", "auto_checkpoint"],
            "returns": "Workflow"
          },
          {
            "name": "get_current_state",
            "description": "Get current workflow state and context",
            "parameters": ["workflow_id"],
            "returns": "dict"
          },
          {
            "name": "rollback_state",
            "description": "Rollback workflow to previous checkpoint",
            "parameters": ["workflow_id", "target_checkpoint_id"],
            "returns": "Workflow"
          },
          {
            "name": "validate_transition",
            "description": "Validate if state transition is allowed",
            "parameters": ["current_state", "target_state"],
            "returns": "bool"
          }
        ]
      },
      {
        "name": "BOBOrchestrator",
        "file": "backend/app/services/bob/orchestrator.py",
        "methods": [
          {
            "name": "plan_milestones",
            "description": "Generate project milestones and breakdown",
            "parameters": ["project_description", "context"],
            "returns": "dict"
          },
          {
            "name": "debug_code",
            "description": "Analyze and suggest fixes for errors",
            "parameters": ["code", "error", "context"],
            "returns": "dict"
          },
          {
            "name": "generate_tests",
            "description": "Generate test cases for code",
            "parameters": ["code", "test_type", "context"],
            "returns": "dict"
          },
          {
            "name": "maintain_context",
            "description": "Update and persist workflow context",
            "parameters": ["workflow_id", "new_data"],
            "returns": "None"
          },
          {
            "name": "stream_response",
            "description": "Stream AI responses in real-time",
            "parameters": ["prompt", "context"],
            "returns": "AsyncGenerator[str, None]"
          }
        ]
      },
      {
        "name": "ContextManager",
        "file": "backend/app/services/bob/context_manager.py",
        "methods": [
          {
            "name": "save_context",
            "description": "Persist workflow context",
            "parameters": ["workflow_id", "context_data"],
            "returns": "None"
          },
          {
            "name": "load_context",
            "description": "Load workflow context",
            "parameters": ["workflow_id"],
            "returns": "dict"
          },
          {
            "name": "merge_contexts",
            "description": "Merge context from different sources",
            "parameters": ["base_context", "new_context"],
            "returns": "dict"
          },
          {
            "name": "compress_context",
            "description": "Compress context to fit token limits",
            "parameters": ["context", "max_tokens"],
            "returns": "dict"
          }
        ]
      }
    ],
    "rest_endpoints": {
      "projects": [
        {
          "method": "POST",
          "path": "/api/v1/projects",
          "description": "Create new project"
        },
        {
          "method": "GET",
          "path": "/api/v1/projects",
          "description": "List all projects"
        },
        {
          "method": "GET",
          "path": "/api/v1/projects/{project_id}",
          "description": "Get project details"
        },
        {
          "method": "PUT",
          "path": "/api/v1/projects/{project_id}",
          "description": "Update project"
        },
        {
          "method": "DELETE",
          "path": "/api/v1/projects/{project_id}",
          "description": "Delete project"
        }
      ],
      "checkpoints": [
        {
          "method": "POST",
          "path": "/api/v1/checkpoints",
          "description": "Create checkpoint"
        },
        {
          "method": "GET",
          "path": "/api/v1/checkpoints/{checkpoint_id}",
          "description": "Get checkpoint"
        },
        {
          "method": "GET",
          "path": "/api/v1/projects/{project_id}/checkpoints",
          "description": "List project checkpoints"
        },
        {
          "method": "POST",
          "path": "/api/v1/checkpoints/{checkpoint_id}/restore",
          "description": "Restore checkpoint"
        },
        {
          "method": "GET",
          "path": "/api/v1/checkpoints/diff",
          "description": "Compare checkpoints"
        }
      ],
      "workflows": [
        {
          "method": "POST",
          "path": "/api/v1/workflows",
          "description": "Initialize workflow"
        },
        {
          "method": "GET",
          "path": "/api/v1/workflows/{workflow_id}",
          "description": "Get workflow state"
        },
        {
          "method": "POST",
          "path": "/api/v1/workflows/{workflow_id}/transition",
          "description": "Transition state"
        },
        {
          "method": "POST",
          "path": "/api/v1/workflows/{workflow_id}/rollback",
          "description": "Rollback workflow"
        },
        {
          "method": "GET",
          "path": "/api/v1/workflows/{workflow_id}/history",
          "description": "Get workflow history"
        }
      ],
      "bob_ai": [
        {
          "method": "POST",
          "path": "/api/v1/bob/plan",
          "description": "Generate project plan"
        },
        {
          "method": "POST",
          "path": "/api/v1/bob/debug",
          "description": "Debug code with BOB"
        },
        {
          "method": "POST",
          "path": "/api/v1/bob/test",
          "description": "Generate tests"
        },
        {
          "method": "POST",
          "path": "/api/v1/bob/chat",
          "description": "Chat with BOB"
        },
        {
          "method": "GET",
          "path": "/api/v1/bob/stream",
          "description": "Stream AI responses (WebSocket)"
        }
      ]
    },
    "frontend_components": [
      {
        "name": "CheckpointTimeline",
        "file": "frontend/src/components/Checkpoint/CheckpointTimeline.tsx",
        "description": "Visualize checkpoints in chronological order with milestone markers"
      },
      {
        "name": "StateVisualization",
        "file": "frontend/src/components/Workflow/StateVisualization.tsx",
        "description": "Display state machine diagram with current state and available transitions"
      },
      {
        "name": "ChatInterface",
        "file": "frontend/src/components/BOB/ChatInterface.tsx",
        "description": "Real-time chat interface with BOB AI including streaming responses"
      }
    ]
  },
  "database_schema": {
    "tables": [
      {
        "name": "projects",
        "description": "Store project information",
        "columns": [
          {
            "name": "id",
            "type": "UUID",
            "constraints": "PRIMARY KEY"
          },
          {
            "name": "name",
            "type": "VARCHAR(255)",
            "constraints": "NOT NULL"
          },
          {
            "name": "description",
            "type": "TEXT",
            "constraints": ""
          },
          {
            "name": "tech_stack",
            "type": "JSONB",
            "constraints": ""
          },
          {
            "name": "status",
            "type": "VARCHAR(50)",
            "constraints": "DEFAULT 'active'"
          },
          {
            "name": "created_at",
            "type": "TIMESTAMP",
            "constraints": "DEFAULT NOW()"
          },
          {
            "name": "updated_at",
            "type": "TIMESTAMP",
            "constraints": "DEFAULT NOW()"
          }
        ]
      },
      {
        "name": "checkpoints",
        "description": "Store checkpoint snapshots",
        "columns": [
          {
            "name": "id",
            "type": "UUID",
            "constraints": "PRIMARY KEY"
          },
          {
            "name": "project_id",
            "type": "UUID",
            "constraints": "NOT NULL REFERENCES projects(id)"
          },
          {
            "name": "milestone",
            "type": "VARCHAR(50)",
            "constraints": "NOT NULL"
          },
          {
            "name": "state_data",
            "type": "JSONB",
            "constraints": "NOT NULL"
          },
          {
            "name": "metadata",
            "type": "JSONB",
            "constraints": ""
          },
          {
            "name": "created_at",
            "type": "TIMESTAMP",
            "constraints": "DEFAULT NOW()"
          },
          {
            "name": "created_by",
            "type": "UUID",
            "constraints": "REFERENCES users(id)"
          }
        ],
        "indexes": [
          "idx_checkpoints_project ON (project_id)",
          "idx_checkpoints_milestone ON (milestone)"
        ]
      },
      {
        "name": "workflows",
        "description": "Store workflow state and history",
        "columns": [
          {
            "name": "id",
            "type": "UUID",
            "constraints": "PRIMARY KEY"
          },
          {
            "name": "project_id",
            "type": "UUID",
            "constraints": "NOT NULL REFERENCES projects(id)"
          },
          {
            "name": "current_state",
            "type": "VARCHAR(50)",
            "constraints": "NOT NULL"
          },
          {
            "name": "context",
            "type": "JSONB",
            "constraints": "NOT NULL"
          },
          {
            "name": "state_history",
            "type": "JSONB[]",
            "constraints": ""
          },
          {
            "name": "created_at",
            "type": "TIMESTAMP",
            "constraints": "DEFAULT NOW()"
          },
          {
            "name": "updated_at",
            "type": "TIMESTAMP",
            "constraints": "DEFAULT NOW()"
          }
        ],
        "indexes": [
          "idx_workflows_project ON (project_id)"
        ]
      }
    ]
  },
  "bob_integration": {
    "architecture": "Hybrid (Embedded Service Layer + External API)",
    "rationale": {
      "performance": "Embedded logic reduces latency for context management",
      "scalability": "Can be extracted to microservice if needed",
      "simplicity": "Single deployment unit for MVP",
      "flexibility": "Easy to add external AI providers"
    },
    "components": [
      {
        "name": "Embedded Module",
        "location": "backend/app/services/bob/",
        "description": "Core BOB logic within FastAPI backend"
      },
      {
        "name": "API Gateway",
        "description": "External AI calls (Anthropic Claude) managed through dedicated service"
      },
      {
        "name": "Context Persistence",
        "description": "Redis for short-term context, PostgreSQL for long-term storage"
      },
      {
        "name": "Agent Specialization",
        "agents": ["Planning Agent", "Debugging Agent", "Testing Agent"]
      },
      {
        "name": "Streaming Support",
        "description": "WebSocket connections for real-time AI responses"
      }
    ]
  },
  "success_metrics": {
    "checkpoint_recovery": "< 2 seconds to restore any checkpoint",
    "context_persistence": "100% context retention across sessions",
    "ai_response_time": "< 5 seconds for BOB responses",
    "system_uptime": "99.9% availability",
    "test_coverage": "> 80% code coverage"
  },
  "next_steps": [
    "Review and approve this architecture plan",
    "Set up development environment",
    "Create initial project scaffolding",
    "Begin Milestone 1 implementation",
    "Establish regular checkpoint reviews"
  ]
}