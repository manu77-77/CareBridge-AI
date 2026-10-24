# CareBridge AI
Healthcare Visit & Follow-up Assistant — a Streamlit prototype to organise instructions already provided by a healthcare professional.

## Features
- Paste de-identified healthcare instructions
- Gemini-generated plain-language summary
- Checklist based only on actions supported by the source
- Questions to ask a healthcare professional
- Flags unclear or important points
- Fictional sample for testing

## Safety
Educational prototype only. Not for diagnosis or treatment decisions. Do not enter patient-identifying information. Check all output against the original instructions and ask a qualified professional about unclear points.

## Run locally
1. Install Python 3.10+.
2. Run `pip install -r requirements.txt`.
3. Set your Gemini key as an environment variable (never commit it):
   - Windows PowerShell: `$env:GEMINI_API_KEY="YOUR_KEY"`
   - macOS/Linux: `export GEMINI_API_KEY="YOUR_KEY"`
4. Run `streamlit run app.py`.

For public hosting, configure `GEMINI_API_KEY` in the hosting provider's secrets settings, not in the code.
