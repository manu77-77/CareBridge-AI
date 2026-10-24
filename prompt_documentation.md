# CareBridge AI — Prompt Documentation

## 1. Project Goal

CareBridge AI is an educational prototype that organises de-identified healthcare instructions already provided by a qualified healthcare professional into:

- A plain-language summary
- A follow-up checklist
- Questions to ask the healthcare professional
- Unclear or important points

The application does not diagnose conditions, prescribe treatment, or change medication instructions.

## 2. AI Tool and Model

- AI provider: Google Gemini API
- Python SDK: `google-genai`
- Model configured in the application: `gemini-3.8-flash`
- Interface framework: Streamlit
- Programming language: Python

The API key is read from the `GEMINI_API_KEY` environment variable and must not be committed to the repository.

## 3. In-App Prompt

The following prompt is used by the `prompt_for()` function in `app.py`.

```text
You organise healthcare instructions already provided by a qualified professional. You are not a clinician.
Return ONLY valid JSON with keys:
"plain_language_summary" (string),
"checklist" (array of strings),
"questions_for_clinician" (array of strings),
"unclear_or_important_points" (array of strings).
Use simple respectful language. Preserve the source meaning and all warnings. Do not diagnose, prescribe, recommend treatment, infer doses, invent details, or tell the user to start/stop/change medication. Checklist items must be explicitly supported by the source. Flag ambiguity and suggest asking the clinician. If the text is not healthcare instructions, say so in the JSON.
SOURCE TEXT:
---
[The user's supplied instructions are inserted here]
---
```

The actual application inserts the supplied text in place of the placeholder.

## 4. Development and Improvement History

The development process involved:

1. Creating a Streamlit interface for entering healthcare instructions.
2. Connecting the application to the Gemini API.
3. Requesting structured JSON output for the four result sections.
4. Testing fictional examples involving clear instructions, ambiguous instructions, and emergency warnings.
5. Updating the result-display code after an indentation and result-handling issue caused headings and output sections to appear incorrectly.
6. Applying a soft sage-green theme using `.streamlit/config.toml`.

Note: This section summarises the development process. The original development prompts were not all preserved verbatim, so these summaries are not presented as exact historical prompts.

## 5. Fictional Test Log

### Test 1 — Clear follow-up instructions

**Input**

```text
Attend a follow-up appointment in seven days. Keep the wound clean and dry as instructed by your nurse. Bring your current medication list. Contact the clinic if you have questions.
```

**Observed result**

The AI summarised the follow-up appointment, wound-care instruction, medication list, and contacting the clinic. It also identified that the exact appointment date and time were not provided.

**Issue identified**

The checklist was empty in the observed output, despite several actionable instructions in the input.

**Status: Needs further testing.** The result-display code was corrected, but the empty checklist must be retested to establish whether the issue is resolved.

### Test 2 — Ambiguous medication and appointment instructions

**Input**

```text
Take the medicine as previously discussed. Attend the next appointment soon. If you are unsure about the instructions, contact the clinic.
```

**Observed result**

The AI identified that the medicine name, dose, and schedule were missing. It also flagged that the appointment date and time were unspecified and suggested asking the clinic for clarification.

**Assessment**

The output handled the ambiguity appropriately in the observed test. It did not invent a medication dose or appointment date.

### Test 3 — Urgent warning

**Input**

```text
Follow the wound-care instructions provided by the nurse. Seek emergency medical attention immediately if severe bleeding or difficulty breathing occurs. Contact the clinic if you have questions about routine wound care.
```

**Observed result**

The AI retained the warning about severe bleeding and difficulty breathing, explained that the wound-care details were not included, and suggested contacting the clinic about routine care questions.

**Assessment**

The observed output preserved the urgent warning clearly. Further testing is still needed to assess consistency.

## 6. Technical Issue and Fix

An `AttributeError` occurred when the application attempted to call `.get()` on a `None` result.

The result-rendering section was updated to:

- Display results only when the result is a dictionary.
- Keep the summary, checklist, questions, and important points within the correct conditional block.
- Show a fallback message if no checklist items are returned.
- Avoid attempting to render missing or invalid results as a dictionary.

The interface was also updated to use a soft sage-green theme.

**Verification status:** The corrected layout has displayed the result sections, but the empty-checklist behaviour still requires a fresh test. The fix should not be described as fully verified until that test passes.

## 7. Safety and Limitations

- Use fictional or de-identified text only.
- Do not enter names or other identifying information.
- The output may omit details or produce an incomplete checklist.
- The AI must not replace the healthcare professional's original instructions.
- Important warnings should be compared against the original text.
- Users should contact their healthcare professional about unclear or contradictory instructions.
- The prototype is not a medical device and is not intended for diagnosis or treatment decisions.

## 8. Reflection and Next Improvements

The structured JSON prompt helps organise information into predictable sections. Explicit instructions to preserve warnings, avoid inventing details, and flag ambiguity support safer output.

The main issue identified during testing is that the checklist may be empty even when the input contains actionable instructions. The next improvement is to investigate and retest checklist generation before treating the application as submission-ready.

Further testing should include unrelated text, empty input, malformed model output, API errors, and repeated runs of the same fictional examples.

## 9. Final Project Checklist

- [x] Gemini API connection tested successfully
- [x] Three fictional examples tested
- [x] Soft sage-green theme applied
- [x] Result-rendering code updated
- [ ] Empty-checklist issue retested and resolved
- [ ] Prompt documentation reviewed and saved
- [ ] API key excluded from source control
- [ ] GitHub repository published
- [ ] Live deployment tested
- [ ] Assessment demonstration video recorded
