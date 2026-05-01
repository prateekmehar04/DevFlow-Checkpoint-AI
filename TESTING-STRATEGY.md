# DevFlow Checkpoint AI - Testing Strategy & CI/CD

## Testing Philosophy

Our testing strategy follows the **Testing Pyramid** approach:
- **70% Unit Tests**: Fast, isolated tests for individual components
- **20% Integration Tests**: Tests for component interactions
- **10% E2E Tests**: Full workflow tests from user perspective

### Quality Goals
- **Code Coverage**: Minimum 80% overall, 90% for critical paths
- **Test Execution Time**: < 5 minutes for unit tests, < 15 minutes for full suite
- **Reliability**: Zero flaky tests in CI/CD pipeline
- **Maintainability**: Clear, readable tests that serve as documentation

## Backend Testing Strategy

### 1. Unit Tests

#### Test Structure
```python
# tests/unit/services/test_checkpoint_service.py

import pytest
from unittest.mock import Mock, patch
from app.services.checkpoint_service import CheckpointService

class TestCheckpointService:
    """Unit tests for CheckpointService"""
    
    @pytest.fixture
    def service(self):
        """Create service instance with mocked dependencies"""
        return CheckpointService()
    
    @pytest.fixture
    def mock_checkpoint_data(self):
        """Sample checkpoint data for testing"""
        return {
            "project_id": "123e4567-e89b-12d3-a456-426614174000",
            "milestone": "plan",
            "state_data": {"files": [], "context": {}},
            "metadata": {"author": "test_user"}
        }
    
    async def test_create_checkpoint_success(self, service, mock_checkpoint_data):
        """Test successful checkpoint creation"""
        # Arrange
        with patch('app.services.checkpoint_service.db') as mock_db:
            mock_db.add.return_value = None
            
            # Act
            result = await service.create_checkpoint(**mock_checkpoint_data)
            
            # Assert
            assert result.milestone == "plan"
            assert result.project_id == mock_checkpoint_data["project_id"]
            mock_db.add.assert_called_once()
    
    async def test_create_checkpoint_invalid_milestone(self, service):
        """Test checkpoint creation with invalid milestone"""
        # Arrange
        invalid_data = {
            "project_id": "123e4567-e89b-12d3-a456-426614174000",
            "milestone": "invalid_milestone",
            "state_data": {},
            "metadata": {}
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid milestone"):
            await service.create_checkpoint(**invalid_data)
```

#### Coverage Areas
- **Services**: All business logic methods
- **Models**: Validation, serialization, relationships
- **Utils**: Helper functions, formatters, validators
- **BOB Agents**: Planning, debugging, testing logic

### 2. Integration Tests

#### Test Structure
```python
# tests/integration/api/test_checkpoint_endpoints.py

import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.integration
class TestCheckpointEndpoints:
    """Integration tests for checkpoint API endpoints"""
    
    @pytest.fixture
    async def client(self):
        """Create test client"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
    
    @pytest.fixture
    async def test_project(self, client):
        """Create a test project"""
        response = await client.post(
            "/api/v1/projects",
            json={"name": "Test Project", "description": "Test"}
        )
        return response.json()
    
    async def test_create_checkpoint_flow(self, client, test_project):
        """Test complete checkpoint creation flow"""
        # Create checkpoint
        response = await client.post(
            "/api/v1/checkpoints",
            json={
                "project_id": test_project["id"],
                "milestone": "plan",
                "state_data": {"files": []},
                "metadata": {}
            }
        )
        
        assert response.status_code == 201
        checkpoint = response.json()
        assert checkpoint["milestone"] == "plan"
        
        # Retrieve checkpoint
        response = await client.get(f"/api/v1/checkpoints/{checkpoint['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == checkpoint["id"]
    
    async def test_workflow_state_transitions(self, client, test_project):
        """Test workflow state machine transitions"""
        # Initialize workflow
        response = await client.post(
            "/api/v1/workflows",
            json={"project_id": test_project["id"]}
        )
        workflow = response.json()
        assert workflow["current_state"] == "plan"
        
        # Transition to code
        response = await client.post(
            f"/api/v1/workflows/{workflow['id']}/transition",
            json={"target_state": "code"}
        )
        assert response.status_code == 200
        assert response.json()["current_state"] == "code"
```

#### Coverage Areas
- **API Endpoints**: All REST endpoints with various scenarios
- **Database Operations**: CRUD operations, transactions, rollbacks
- **State Machine**: Workflow transitions and validations
- **BOB Integration**: AI agent interactions with real API calls (mocked)

### 3. End-to-End Tests

#### Test Structure
```python
# tests/e2e/test_complete_workflow.py

import pytest
from playwright.async_api import async_playwright

@pytest.mark.e2e
class TestCompleteWorkflow:
    """E2E tests for complete user workflows"""
    
    async def test_project_lifecycle(self):
        """Test complete project lifecycle from creation to completion"""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            # Navigate to app
            await page.goto("http://localhost:3000")
            
            # Create new project
            await page.click("text=New Project")
            await page.fill("input[name='name']", "E2E Test Project")
            await page.fill("textarea[name='description']", "Test Description")
            await page.click("button:has-text('Create')")
            
            # Wait for project page
            await page.wait_for_selector("text=E2E Test Project")
            
            # Initialize workflow
            await page.click("text=Start Workflow")
            
            # Verify plan state
            await page.wait_for_selector("text=Planning Phase")
            
            # Interact with BOB
            await page.fill("textarea[placeholder='Chat with BOB']", "Create a plan")
            await page.click("button:has-text('Send')")
            
            # Wait for BOB response
            await page.wait_for_selector(".bob-response")
            
            # Create checkpoint
            await page.click("text=Create Checkpoint")
            await page.wait_for_selector("text=Checkpoint created")
            
            # Transition to code phase
            await page.click("text=Move to Code")
            await page.wait_for_selector("text=Coding Phase")
            
            await browser.close()
```

#### Coverage Areas
- **User Workflows**: Complete user journeys
- **UI Interactions**: All critical user interactions
- **Real-time Updates**: WebSocket functionality
- **Error Handling**: User-facing error scenarios

## Frontend Testing Strategy

### 1. Component Tests

#### Test Structure
```typescript
// frontend/src/components/Checkpoint/CheckpointTimeline.test.tsx

import { render, screen, fireEvent } from '@testing-library/react';
import { Provider } from 'react-redux';
import { CheckpointTimeline } from './CheckpointTimeline';
import { store } from '../../store';

describe('CheckpointTimeline', () => {
  const mockCheckpoints = [
    {
      id: '1',
      milestone: 'plan',
      created_at: '2024-01-01T00:00:00Z',
      state_data: {}
    },
    {
      id: '2',
      milestone: 'code',
      created_at: '2024-01-02T00:00:00Z',
      state_data: {}
    }
  ];

  it('renders checkpoint timeline correctly', () => {
    render(
      <Provider store={store}>
        <CheckpointTimeline 
          projectId="test-project" 
          onCheckpointSelect={jest.fn()} 
        />
      </Provider>
    );

    expect(screen.getByText('Checkpoint Timeline')).toBeInTheDocument();
  });

  it('displays all checkpoints', () => {
    render(
      <Provider store={store}>
        <CheckpointTimeline 
          projectId="test-project" 
          onCheckpointSelect={jest.fn()} 
        />
      </Provider>
    );

    expect(screen.getByText('plan')).toBeInTheDocument();
    expect(screen.getByText('code')).toBeInTheDocument();
  });

  it('calls onCheckpointSelect when checkpoint is clicked', () => {
    const mockSelect = jest.fn();
    
    render(
      <Provider store={store}>
        <CheckpointTimeline 
          projectId="test-project" 
          onCheckpointSelect={mockSelect} 
        />
      </Provider>
    );

    fireEvent.click(screen.getByText('plan'));
    expect(mockSelect).toHaveBeenCalledWith('1');
  });
});
```

### 2. Hook Tests

```typescript
// frontend/src/hooks/useCheckpoint.test.ts

import { renderHook, act } from '@testing-library/react';
import { useCheckpoint } from './useCheckpoint';

describe('useCheckpoint', () => {
  it('fetches checkpoint data', async () => {
    const { result } = renderHook(() => useCheckpoint('checkpoint-id'));

    await act(async () => {
      await result.current.fetchCheckpoint();
    });

    expect(result.current.checkpoint).toBeDefined();
    expect(result.current.loading).toBe(false);
  });

  it('handles errors correctly', async () => {
    const { result } = renderHook(() => useCheckpoint('invalid-id'));

    await act(async () => {
      await result.current.fetchCheckpoint();
    });

    expect(result.current.error).toBeDefined();
    expect(result.current.checkpoint).toBeNull();
  });
});
```

### 3. Redux Tests

```typescript
// frontend/src/store/slices/checkpointSlice.test.ts

import checkpointReducer, { 
  addCheckpoint, 
  removeCheckpoint 
} from './checkpointSlice';

describe('checkpointSlice', () => {
  const initialState = {
    checkpoints: [],
    loading: false,
    error: null
  };

  it('should handle addCheckpoint', () => {
    const checkpoint = {
      id: '1',
      milestone: 'plan',
      created_at: '2024-01-01T00:00:00Z'
    };

    const actual = checkpointReducer(
      initialState, 
      addCheckpoint(checkpoint)
    );

    expect(actual.checkpoints).toHaveLength(1);
    expect(actual.checkpoints[0]).toEqual(checkpoint);
  });

  it('should handle removeCheckpoint', () => {
    const stateWithCheckpoint = {
      ...initialState,
      checkpoints: [{ id: '1', milestone: 'plan' }]
    };

    const actual = checkpointReducer(
      stateWithCheckpoint,
      removeCheckpoint('1')
    );

    expect(actual.checkpoints).toHaveLength(0);
  });
});
```

## Test Configuration

### Backend (pytest.ini)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
asyncio_mode = auto
```

### Frontend (jest.config.js)

```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts?(x)', '**/?(*.)+(spec|test).ts?(x)'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.tsx',
    '!src/**/*.stories.tsx'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy'
  }
};
```

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/ci-cd.yml

name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Cache Python dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linting
        run: |
          cd backend
          black --check app tests
          flake8 app tests
          mypy app
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: backend

  frontend-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Cache Node modules
        uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run linting
        run: |
          cd frontend
          npm run lint
      
      - name: Run type checking
        run: |
          cd frontend
          npm run type-check
      
      - name: Run tests
        run: |
          cd frontend
          npm run test:coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./frontend/coverage/coverage-final.json
          flags: frontend

  e2e-tests:
    runs-on: ubuntu-latest
    needs: [backend-tests, frontend-tests]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Start services
        run: |
          docker-compose up -d
          sleep 10
      
      - name: Run E2E tests
        run: |
          cd backend
          pytest tests/e2e -v
      
      - name: Stop services
        if: always()
        run: docker-compose down

  build-and-deploy:
    runs-on: ubuntu-latest
    needs: [backend-tests, frontend-tests, e2e-tests]
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker images
        run: |
          docker build -t devflow-backend:latest ./backend
          docker build -t devflow-frontend:latest ./frontend
      
      - name: Push to registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker push devflow-backend:latest
          docker push devflow-frontend:latest
      
      - name: Deploy to production
        run: |
          # Add deployment commands here
          echo "Deploying to production..."
```

## Test Data Management

### Fixtures and Factories

```python
# tests/conftest.py

import pytest
from factory import Factory, Faker
from app.models import Project, Checkpoint, Workflow

class ProjectFactory(Factory):
    class Meta:
        model = Project
    
    name = Faker('company')
    description = Faker('text')
    tech_stack = {"backend": "Python", "frontend": "React"}

class CheckpointFactory(Factory):
    class Meta:
        model = Checkpoint
    
    milestone = Faker('random_element', elements=['plan', 'code', 'debug', 'test'])
    state_data = {}
    metadata = {}

@pytest.fixture
def sample_project():
    return ProjectFactory()

@pytest.fixture
def sample_checkpoint():
    return CheckpointFactory()
```

## Performance Testing

### Load Testing with Locust

```python
# tests/performance/locustfile.py

from locust import HttpUser, task, between

class DevFlowUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def list_projects(self):
        self.client.get("/api/v1/projects")
    
    @task(2)
    def create_checkpoint(self):
        self.client.post("/api/v1/checkpoints", json={
            "project_id": "test-id",
            "milestone": "plan",
            "state_data": {},
            "metadata": {}
        })
    
    @task(1)
    def chat_with_bob(self):
        self.client.post("/api/v1/bob/chat", json={
            "message": "Help me plan this project",
            "context": {}
        })
```

## Monitoring and Reporting

### Test Reports
- **Coverage Reports**: Generated in HTML and uploaded to Codecov
- **Test Results**: JUnit XML format for CI/CD integration
- **Performance Metrics**: Response times, throughput, error rates

### Quality Gates
- All tests must pass
- Code coverage ≥ 80%
- No critical security vulnerabilities
- Performance benchmarks met
- No linting errors

## Best Practices

1. **Write Tests First**: Follow TDD when possible
2. **Keep Tests Independent**: No test should depend on another
3. **Use Descriptive Names**: Test names should describe what they test
4. **Mock External Dependencies**: Don't rely on external services
5. **Test Edge Cases**: Include boundary conditions and error scenarios
6. **Maintain Test Data**: Keep fixtures up to date
7. **Review Test Coverage**: Regularly check coverage reports
8. **Optimize Test Speed**: Keep unit tests fast
9. **Document Complex Tests**: Add comments for non-obvious logic
10. **Refactor Tests**: Keep test code clean and maintainable

---

**Testing is not just about finding bugs—it's about building confidence in our system.**