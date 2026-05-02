# IBM BOB & Supabase PostgreSQL Setup Guide

## Overview

This guide will help you configure DevFlow Checkpoint AI with:
1. **IBM BOB API** - For AI-powered planning, debugging, and testing
2. **Supabase PostgreSQL** - For cloud-hosted database

## Step 1: Configure Supabase PostgreSQL

### Your Supabase Connection Details
```
Host: db.whulvrnkotzizayydtrr.supabase.co
Port: 5432
Database: postgres
User: postgres
Password: [YOUR-PASSWORD]
```

### Update Environment Variables

Edit `backend/.env` and replace `[YOUR-PASSWORD]` with your actual Supabase password:

```env
# Database - Supabase PostgreSQL
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_ACTUAL_PASSWORD@db.whulvrnkotzizayydtrr.supabase.co:5432/postgres
```

**Example:**
If your password is `MySecurePass123`, the line should be:
```env
DATABASE_URL=postgresql+asyncpg://postgres:MySecurePass123@db.whulvrnkotzizayydtrr.supabase.co:5432/postgres
```

## Step 2: Configure IBM BOB API

### Update Environment Variables

Edit `backend/.env` and add your IBM BOB API key:

```env
# IBM BOB API
IBM_BOB_API_KEY=your-actual-ibm-bob-api-key
IBM_BOB_API_URL=https://api.ibm.com/bob/v1
BOB_MODEL=ibm-bob-v1
```

**Replace** `your-actual-ibm-bob-api-key` with your real IBM BOB API key.

### IBM BOB API Endpoints

The system expects IBM BOB to provide these endpoints:

1. **POST** `/messages` - Create a message
   ```json
   {
     "model": "ibm-bob-v1",
     "max_tokens": 100000,
     "temperature": 0.7,
     "system": "System prompt",
     "messages": [{"role": "user", "content": "User message"}]
   }
   ```

2. **POST** `/messages/stream` - Stream a message
   ```json
   {
     "model": "ibm-bob-v1",
     "max_tokens": 100000,
     "temperature": 0.7,
     "system": "System prompt",
     "messages": [{"role": "user", "content": "User message"}],
     "stream": true
   }
   ```

### Response Format

IBM BOB should return responses in this format:

```json
{
  "content": [
    {
      "text": "Generated response text here"
    }
  ]
}
```

For streaming, it should send Server-Sent Events (SSE):
```
data: {"text": "chunk of text"}
data: {"text": "another chunk"}
data: [DONE]
```

## Step 3: Install Dependencies

```bash
cd backend
pip install httpx python-dotenv
```

## Step 4: Run Database Migrations

Once your Supabase credentials are configured:

```bash
cd backend

# Run migrations to create tables in Supabase
alembic upgrade head
```

This will create the following tables in your Supabase database:
- `users`
- `projects`
- `checkpoints`
- `workflows`

## Step 5: Verify Configuration

### Test Database Connection

```bash
cd backend
python -c "from app.database import engine; import asyncio; asyncio.run(engine.connect()); print('✅ Database connected!')"
```

### Test API

Start the server:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

Test endpoints:

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Create Project (tests database):**
```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Project", "description": "Testing Supabase"}'
```

**Test IBM BOB Planning:**
```bash
curl -X POST http://localhost:8000/api/v1/bob/plan \
  -H "Content-Type: application/json" \
  -d '{"project_description": "Build a todo app", "context": {}}'
```

## Troubleshooting

### Database Connection Issues

**Error: "could not connect to server"**
- Verify your Supabase password is correct
- Check that your IP is allowed in Supabase dashboard
- Ensure the connection string format is correct

**Error: "SSL connection required"**
- Supabase requires SSL. The connection string should work as-is with `asyncpg`

### IBM BOB API Issues

**Error: "API key not configured"**
- Ensure `IBM_BOB_API_KEY` is set in `backend/.env`
- Restart the backend server after changing `.env`

**Error: "Connection refused" or "404"**
- Verify the `IBM_BOB_API_URL` is correct
- Check that your IBM BOB API key has the correct permissions
- Ensure the API endpoints match the expected format

**Fallback Mode**
If IBM BOB API is not configured or fails, the system will automatically use fallback responses with pre-defined templates.

### Supabase Dashboard

You can view your data in Supabase:
1. Go to https://supabase.com/dashboard
2. Select your project
3. Navigate to "Table Editor"
4. View `projects`, `checkpoints`, `workflows` tables

## Environment Variables Reference

### Complete `.env` Configuration

```env
# Application
APP_NAME=DevFlow Checkpoint AI
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development

# Server
HOST=0.0.0.0
PORT=8000

# Database - Supabase PostgreSQL
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@db.whulvrnkotzizayydtrr.supabase.co:5432/postgres
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# Redis (optional)
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_TTL=3600

# Legacy JSON storage (fallback)
DEVFLOW_DATA_PATH=data/devflow.json

# CORS
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# IBM BOB API
IBM_BOB_API_KEY=your-ibm-bob-api-key-here
IBM_BOB_API_URL=https://api.ibm.com/bob/v1
BOB_MODEL=ibm-bob-v1
BOB_MAX_TOKENS=100000
BOB_TEMPERATURE=0.7
BOB_STREAMING=true

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## Features Enabled

With IBM BOB and Supabase configured, you get:

✅ **AI-Powered Planning** - IBM BOB generates project milestones
✅ **AI-Powered Debugging** - IBM BOB analyzes errors and suggests fixes
✅ **AI-Powered Testing** - IBM BOB generates test cases
✅ **Cloud Database** - All data stored in Supabase PostgreSQL
✅ **Persistent Storage** - Data survives server restarts
✅ **Scalable** - Supabase handles scaling automatically
✅ **Backup** - Supabase provides automatic backups

## Next Steps

1. ✅ Configure Supabase password in `.env`
2. ✅ Configure IBM BOB API key in `.env`
3. ✅ Run database migrations
4. ✅ Start backend server
5. ✅ Test API endpoints
6. 🚀 Start building with DevFlow!

## Support

- **Supabase Issues**: Check https://supabase.com/docs
- **IBM BOB Issues**: Contact IBM BOB support
- **Application Issues**: Check logs in terminal

---

**Ready to build! 🚀**