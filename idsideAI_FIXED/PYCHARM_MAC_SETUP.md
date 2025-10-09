# idsideAI PyCharm Setup for Mac

## Quick Start (5 minutes)

### 1. Open in PyCharm
- **File → Open** → Select this `idsideAI_FIXED` folder
- PyCharm will detect it as a Python project

### 2. Configure Python Interpreter
- **PyCharm → Settings → Project → Python Interpreter**
- **Add Interpreter → Virtualenv Environment → New**
- **Location:** `./venv` (in project folder)
- **Base interpreter:** `/usr/local/bin/python3` (or your Python 3.12 path)
- Click **OK**

### 3. Install Dependencies
- PyCharm will show a banner: "Package requirements file found"
- Click **Install requirements**
- OR manually: Terminal → `pip install -r requirements.txt`

### 4. Run Configuration (Already Created)
- Look for **"idsideAI Debug"** in the run configurations dropdown (top right)
- If not visible: **Run → Edit Configurations** → Should see "idsideAI Debug"
- **Script path:** `run.py`
- **Working directory:** Project root

### 5. Test It
- Click **green play button** or **debug button**
- Should see: "🚀 Starting IDECIDE AI..."
- Open: http://localhost:8013/docs

## Alternative: Command Line
```bash
./start_mac.sh
```

## Debugging
- Set breakpoints by clicking left margin in code
- Use **debug button** (green bug icon)
- Visit http://localhost:8013/healthz to trigger breakpoints

## Environment Variables
Add to PyCharm run configuration if needed:
- `OPENAI_API_KEY=your-key-here`
- `DATABASE_URL=sqlite:///./idsideai.db`

**Ready to code! 🚀**
