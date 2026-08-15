# Agentic SDLC Control Tower

Interview PoC: Requirement -> Context -> Requirement Agent -> HITL -> Design -> Architecture Review -> Build/Test -> Evaluation.

## Run
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

The app runs in deterministic demo mode without an API key. This is intentional: no fake LLM claims.
If OPENAI_API_KEY is later added, live model integration can be layered in.

## Demo
Use the preloaded requirement, click Run Agentic SDLC, approve the clarification, approve the architecture review, then inspect the evaluation and trace.
