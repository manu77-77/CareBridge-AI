import os, json, re
import streamlit as st
from google import genai

st.set_page_config(page_title="CareBridge AI", page_icon="🩺", layout="centered")
st.title("🩺 CareBridge AI")
st.subheader("Healthcare Visit & Follow-up Assistant")
st.write("Organise instructions you have already received from a qualified healthcare professional into a clearer summary, checklist, and questions for your next visit.")
st.warning("Educational prototype only — not a medical device or a substitute for a clinician. It does not diagnose, prescribe, or change medication instructions. Use fictional or de-identified text only; do not enter names or other identifying details.")

with st.expander("How to use"):
    st.write("Remove personal details, paste instructions from your clinician, then select Organise instructions. Ask your healthcare professional about anything unclear.")

sample = """Example only — fictional instructions:
Schedule a follow-up appointment with the clinic in one week.
Keep the wound clean and dry as explained by the nurse.
Contact the clinic if you are unsure how to care for the wound.
Seek urgent medical help if you experience severe bleeding or difficulty breathing.
Bring your current medication list to the follow-up visit."""

if "instructions" not in st.session_state:
    st.session_state.instructions = ""
if st.button("Load fictional sample"):
    st.session_state.instructions = sample

text = st.text_area("Healthcare instructions", key="instructions", height=220, placeholder="Paste de-identified instructions here...")
go = st.button("Organise instructions", type="primary")


def prompt_for(source):
    return f"""
You organise healthcare instructions already provided by a
qualified healthcare professional. You are not a clinician.

Return ONLY valid JSON with exactly these keys:
- "plain_language_summary": a string
- "checklist": an array of strings
- "questions_for_clinician": an array of strings
- "unclear_or_important_points": an array of strings

Rules:
1. Use simple, respectful language.
2. Preserve the source meaning and every safety warning.
3. Do not diagnose, prescribe, recommend new treatment, infer
   medication doses, invent details, or change medication
   instructions.
4. Put each clear, actionable task explicitly supported by the
   source into a separate checklist item.
5. For example, if the source says to attend a follow-up visit
   and bring a medication list, include both as checklist items.
6. Do not leave the checklist empty if the source contains clear,
   actionable tasks. If no actionable tasks are provided, return
   an empty array.
7. Do not put checklist items inside the summary.
8. Flag missing dates, unclear instructions, and other ambiguity.
9. Ask questions that help the user clarify missing information
   with their healthcare professional.
10. If the source is not healthcare instructions, explain this
    in the summary and do not invent healthcare tasks.
11. Return all four keys even if some arrays are empty.

SOURCE TEXT:
---
{source}
---
"""


def parse_json(raw):
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    a, b = raw.find("{"), raw.rfind("}")
    if a < 0 or b <= a:
        raise ValueError("No JSON object in model response")
    return json.loads(raw[a:b+1])

if go:
    if not text.strip():
        st.error("Paste instructions or load the fictional sample first.")
    elif len(text) > 12000:
        st.error("Please shorten the text to 12,000 characters or fewer.")
    else:
        key = os.getenv("GEMINI_API_KEY", "").strip()
        if not key:
            st.error("GEMINI_API_KEY is not configured. Set it as an environment variable; never put the key in this code or GitHub.")
        else:
            try:
                with st.spinner("Organising instructions..."):
                    client = genai.Client(api_key=key)
                    response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt_for(text))
                    st.session_state.result = parse_json(response.text or "")
            except Exception as e:
                st.error("The AI request failed. Check internet access, API key, and model availability.")
                st.caption(type(e).__name__)


result = st.session_state.get("result")

if isinstance(result, dict):
    st.divider()
    st.header("Organised instructions")

    st.subheader("Plain-language summary")
    st.write(
        result.get(
            "plain_language_summary",
            "No summary returned."
        )
    )

    st.subheader("Follow-up checklist")
    checklist = result.get("checklist", [])

    if isinstance(checklist, list) and checklist:
        for i, item in enumerate(checklist):
            st.checkbox(str(item), key=f"followup_{i}")
    else:
        st.info(
            "No checklist items were returned. "
            "Please review the summary and original instructions."
        )

    st.subheader("Questions for your healthcare professional")
    questions = result.get("questions_for_clinician", [])

    if isinstance(questions, list) and questions:
        for item in questions:
            st.markdown(f"- {item}")
    else:
        st.info("No questions were returned.")

    st.subheader("Unclear or important points")
    important_points = result.get("unclear_or_important_points", [])

    if isinstance(important_points, list) and important_points:
        for item in important_points:
            st.markdown(f"- {item}")
    else:
        st.info("No additional points were returned.")

    st.info(
        "Compare this output with the original instructions. "
        "If anything is missing, contradictory, or unclear, "
        "contact the healthcare professional who provided them."
    )

elif result is not None:
    st.warning(
        "The AI response was not valid. Please organise the "
        "instructions again."
    )

st.divider()
st.caption(
    "CareBridge AI • Project prototype • "
    "Not for diagnosis or treatment decisions"
)
