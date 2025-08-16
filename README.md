# LeetCode Help Buddy

A Python + FastAPI + Gradio application that helps with LeetCode problems by:

1. **Generating high-quality test cases** from problem constraints and examples
2. **Explaining problems** with progressive hints (no full solutions)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key

### Installation

1. Clone and navigate to the project:
```bash
git clone <your-repo>
cd LeetcodeHelpBuddy
```

2. **Create and activate virtual environment** (Recommended):

**Windows Command Prompt:**
```cmd
python -m venv leetcode_env
leetcode_env\Scripts\activate.bat
pip install -r requirements.txt
```

**Windows PowerShell:**
```powershell
python -m venv leetcode_env
# If execution policy allows:
leetcode_env\Scripts\Activate.ps1
# Otherwise use: python run_venv.py (see below)
pip install -r requirements.txt
```

**Linux/macOS:**
```bash
python -m venv leetcode_env
source leetcode_env/bin/activate
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your_key_here"
```

4. Run the application:

**With activated virtual environment:**
```bash
python run.py
```

**Or use the virtual environment runner (works without activation):**
```bash
python run_venv.py
```

**Or use helper scripts:**
- **Windows**: Double-click `activate_venv.bat`
- **PowerShell**: Run `.\activate_venv.ps1`

5. Open your browser to: http://localhost:8000/app

## 🎯 Features

### Test Case Generation
- Paste a problem with **Constraints** and **Examples**
- Get boundary cases, edge cases, and pairwise combinations
- Download results as JSON

### Problem Explanation
- Get progressive hints without full solutions
- Understand I/O shapes, edge cases, and common patterns
- Streaming explanations for responsiveness

## 📁 Project Structure

```
LeetcodeHelpBuddy/
├── app/
│   ├── main.py           # FastAPI app with Gradio mounted
│   ├── ui/
│   │   └── gradio_app.py # Gradio interface
│   ├── api/              # REST endpoints (coming soon)
│   ├── parser/           # Constraint/example extraction (coming soon)
│   ├── generator/        # Test case generation (coming soon)
│   └── llm/              # OpenAI integration (coming soon)
├── requirements.txt      # Dependencies
├── run.py               # Development server
└── v1-feature-spec.md   # Complete feature specification
```

## 🔧 Development

The app uses:
- **FastAPI** for the backend API
- **Gradio** for the web interface (mounted at `/app`)
- **OpenAI SDK** with Structured Outputs for explanations
- **JSON Schema 2020-12** for test case validation

### 🐍 Virtual Environment Benefits

Using a virtual environment isolates your project dependencies:
- **No conflicts** with other Python projects
- **Reproducible** installations
- **Clean** system Python
- **Easy deployment** and sharing

### 📂 Virtual Environment Files

- `leetcode_env/` - Virtual environment directory (auto-created)
- `run_venv.py` - Run app using venv (works without activation)
- `activate_venv.bat` - Windows Command Prompt activation
- `activate_venv.ps1` - Windows PowerShell activation

### 🔄 Virtual Environment Workflow

```bash
# One-time setup
python -m venv leetcode_env
leetcode_env\Scripts\activate.bat  # Windows
pip install -r requirements.txt

# Daily usage
leetcode_env\Scripts\activate.bat  # Activate
python run.py                      # Run app
deactivate                         # Exit venv

# Or use the runner (no activation needed)
python run_venv.py
```

## 📋 Compliance

- No crawling or scraping of LeetCode
- Operates only on user-provided content
- Respects LeetCode's Terms of Service

## 🎨 UI Features

- Large text input for problem statements
- Two primary actions: "Generate Tests" and "Explain Problem"
- Streaming explanations with live token display
- Clear error messages and guidance
- Download buttons for generated content
- Responsive design with accessibility considerations

---

**Status**: Basic Gradio app ready. Core features (parser, generator, LLM integration) coming next.
