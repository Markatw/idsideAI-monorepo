# PyCharm Setup Guide - Frictionless Development

## 🚀 One-Click Setup for PyCharm

This idsideAI project is **PyCharm-optimized** with pre-configured run configurations, project settings, and zero-friction setup.

## Quick Start (30 seconds)

### 1. Open Project in PyCharm
```bash
# Extract the package
unzip idsideAI_COMPLETE_APPLICATION.zip
cd idsideAI_COMPLETE_APPLICATION

# Open in PyCharm
pycharm .
# OR: File → Open → Select the idsideAI folder
```

### 2. PyCharm Will Auto-Configure
- ✅ **Project structure** - All source roots configured
- ✅ **Python interpreter** - Auto-detected Python 3.11+
- ✅ **Run configurations** - 5 pre-built configurations ready
- ✅ **Dependencies** - requirements.txt auto-recognized
- ✅ **Code inspection** - Optimized for FastAPI/Python

### 3. Install Dependencies (One Click)
PyCharm will show a notification: **"Package requirements file found"**
- Click **"Install requirements"** 
- OR manually: `pip install -r requirements.txt`

### 4. Run Application (One Click)
In PyCharm toolbar, select **"Run idsideAI Application"** and click ▶️

**That's it!** Application starts at `http://localhost:8000`

## Pre-Configured Run Configurations

PyCharm includes 5 ready-to-use run configurations:

### 🎯 **Run idsideAI Application** (Main)
- **Purpose**: Start the complete application
- **Script**: `run.py`
- **URL**: `http://localhost:8000`
- **Use**: Primary development and testing

### 🔧 **Setup Database & Environment**
- **Purpose**: Initialize database and create .env file
- **Script**: `setup.py`
- **Use**: First-time setup or reset

### 🖥️ **Run Backend Only**
- **Purpose**: Start just the FastAPI backend
- **Script**: `backend/app.py`
- **URL**: `http://localhost:8000`
- **Use**: Backend-only development

### ✅ **Validate Application**
- **Purpose**: Run comprehensive validation tests
- **Script**: `application_validation.py`
- **Use**: Verify zero issues before deployment

### 🧪 **Run Tests**
- **Purpose**: Execute pytest test suite
- **Target**: `tests/` directory
- **Use**: Unit testing and coverage

## PyCharm Features Enabled

### 🔍 **Smart Code Completion**
- FastAPI route completion
- SQLAlchemy model hints
- Pydantic schema validation
- Import auto-completion

### 🐛 **Debugging**
- Breakpoints in FastAPI routes
- Step-through debugging
- Variable inspection
- Call stack analysis

### 📊 **Code Quality**
- PEP 8 compliance checking
- Import optimization
- Code inspection
- Refactoring tools

### 🔧 **Project Structure**
```
idsideAI/
├── backend/          # FastAPI backend (source root)
├── idsideai/         # Core engine (source root)  
├── security_toolkit/ # Security utils (source root)
├── frontend/         # React frontend
├── tests/           # Test suite
├── .idea/           # PyCharm configuration
└── run.py           # Main entry point
```

## Environment Configuration

### Automatic .env Creation
Running any configuration will auto-create `.env` with:
```env
DATABASE_URL=sqlite+aiosqlite:///./idsideai.db
OPENAI_API_KEY=${OPENAI_API_KEY:-}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
AZURE_OPENAI_ENDPOINT=${AZURE_OPENAI_ENDPOINT:-}
AZURE_OPENAI_KEY=${AZURE_OPENAI_KEY:-}
ALLOW_FAKE_PROVIDER=true
```

### API Keys (Optional)
- **Development**: Works with `ALLOW_FAKE_PROVIDER=true`
- **Production**: Set real API keys in environment variables

## Debugging Guide

### 🐛 **Debug Mode**
1. Select **"Run idsideAI Application"** configuration
2. Click the **Debug** button (🐛) instead of Run
3. Set breakpoints by clicking line numbers
4. Application starts in debug mode

### 🔍 **Common Debug Points**
- `backend/app.py:health()` - Health endpoint
- `backend/routers/graphs.py` - Graph operations
- `idsideai/services/engine.py` - Decision engine
- `backend/auth/middleware.py` - Authentication

### 📊 **Performance Profiling**
1. Right-click run configuration
2. Select **"Profile 'Run idsideAI Application'"**
3. Analyze performance bottlenecks

## Troubleshooting

### ❌ **"No Python interpreter configured"**
**Solution**: File → Settings → Project → Python Interpreter → Add → System Interpreter

### ❌ **"Module not found" errors**
**Solution**: File → Settings → Project → Project Structure → Mark directories as "Sources Root"

### ❌ **"Requirements not installed"**
**Solution**: Terminal in PyCharm → `pip install -r requirements.txt`

### ❌ **"Port already in use"**
**Solution**: Stop previous runs → Run → Stop All

## Advanced Features

### 🔄 **Hot Reload Development**
- FastAPI auto-reloads on code changes
- Frontend hot-reloads with Vite
- Database changes require restart

### 📝 **Code Templates**
PyCharm includes templates for:
- FastAPI routes
- Pydantic models
- SQLAlchemy models
- Test functions

### 🧪 **Testing Integration**
- Run individual tests with ▶️ button
- Coverage reports in PyCharm
- Test discovery automatic
- Pytest integration enabled

## Production Deployment

### 🐳 **Docker (from PyCharm)**
1. Open `docker-compose.yml`
2. Click ▶️ next to services
3. Or Terminal: `docker-compose up`

### ☸️ **Kubernetes**
1. Open `k8s/` directory
2. Right-click → Deploy to Kubernetes
3. Or Terminal: `kubectl apply -f k8s/`

## Performance Tips

### ⚡ **Faster Startup**
- Use **"Run Backend Only"** for API-only development
- Exclude large directories in Project Structure
- Enable "Power Save Mode" for battery life

### 🧠 **Memory Optimization**
- File → Settings → Appearance → Memory Indicator
- Help → Change Memory Settings (increase if needed)
- Close unused tool windows

## Summary

This PyCharm setup provides:
- ✅ **Zero configuration** - Everything pre-configured
- ✅ **One-click run** - 5 ready-to-use configurations  
- ✅ **Full debugging** - Breakpoints, profiling, testing
- ✅ **Smart completion** - FastAPI, SQLAlchemy, Pydantic
- ✅ **Production ready** - Docker, Kubernetes integration

**Just open the project and click Run!** 🚀
