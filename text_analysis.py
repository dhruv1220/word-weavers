import json
import datetime
from llm_call import llm_call


# -------------------------------
# Core Agent Functions with Expanded Prompts
# -------------------------------

def grammar_and_style_agent_llm(text: str, context: str = "") -> dict:
    prompt = (
        "You are a professional writing editor using the 826 Valencia Publishing Style Guide "
        "and the NWP Analytic Writing Continuum. Analyze the following student writing for grammar, punctuation, "
        "and style errors. Provide a corrected version of the text, list each change made (with original text, suggestion, "
        "error category, and rationale), and assign a Grammar Score and a Style Score (each between 0 and 100). "
        "Return your output as a JSON object with keys 'edited_text', 'changes', 'grammar_score', and 'style_score'."
        "Do not have any initial or trailing text. \n\n"
        "Student Writing:\n" + text
    )
    output_text = llm_call(prompt)
    # Strip markdown code block delimiters if present
    if output_text.startswith("```json"):
        output_text = output_text[len("```json"):].strip()
    if output_text.endswith("```"):
        output_text = output_text[:-3].strip()
    return json.loads(output_text)

def voice_preservation_agent_llm(original_text: str, edited_text: str, context: str = "") -> dict:
    prompt = (
        "You are a specialist in maintaining the writer's unique voice. Compare the original student writing and the "
        "edited version below. Evaluate whether the student's informal tone and creative expressions are preserved. If necessary, "
        "adjust the edited text to better preserve the original voice. Provide a Voice Preservation Score (0-100) and a brief "
        "explanation. Return your output as JSON with keys 'final_text', 'voice_score', and 'voice_feedback'."
        "Do not have any initial or trailing text. \n\n"
        "Original Text:\n" + original_text + "\n\n"
        "Edited Text:\n" + edited_text
    )
    output_text = llm_call(prompt)
    # Strip markdown code block delimiters if present
    if output_text.startswith("```json"):
        output_text = output_text[len("```json"):].strip()
    if output_text.endswith("```"):
        output_text = output_text[:-3].strip()
    return json.loads(output_text)

def personalized_feedback_agent_llm(metadata: dict, text: str, context: str = "") -> dict:
    prompt = (
        "You are an experienced writing mentor. Given the following student metadata and writing sample, provide "
        "personalized, constructive feedback to help the student improve while preserving their unique voice. Use the NWP "
        "Analytic Writing Continuum as your reference. Return your output as JSON with keys 'feedback_message' and "
        "'personalized_score' (0-100).\n\n"
        "Student Metadata:\n" + json.dumps(metadata, indent=2) + "\n\n"
        "Writing Sample:\n" + text
    )
    output_text = llm_call(prompt)
    # Strip markdown code block delimiters if present
    if output_text.startswith("```json"):
        output_text = output_text[len("```json"):].strip()
    if output_text.endswith("```"):
        output_text = output_text[:-3].strip()
    return json.loads(output_text)

# -------------------------------
# Dynamic Helper Agents for Writing Metrics
# Each helper is provided the full detailed criteria for its category.
# In production, these long prompts would incorporate the complete rubric text.
# -------------------------------

def content_metrics_agent_llm(text: str, context: str = "") -> dict:
    rubric = (
        "Rubric for Content (Including Quality and Clarity of Ideas and Meaning):\n"
        "1. The writing may announce the topic, but no central focus is present; ideas are minimal or undeveloped.\n"
        "2. The writing presents several ideas without a clear focus; ideas are confusing or incidental.\n"
        "3. The writing has a discernible focus; ideas somewhat support the central theme, but details are poorly developed.\n"
        "4. The writing is generally clear and focused; ideas satisfactorily support the theme, though predictable.\n"
        "5. The writing is clear and focused; ideas enhance the theme with developed details and creativity.\n"
        "6. The writing is clear, consistently focused, and exceptionally well developed; ideas fully support the theme with creativity.\n"
    )
    prompt = (
        "You are an expert evaluator for the 'Content' dimension using the following rubric:\n"
        f"{rubric}\n"
        "Evaluate the following student writing on Content. Return a JSON object with keys 'score' (1-6) and 'comment'.\n\n"
        "Student Writing:\n" + text
    )
    output_text = llm_call(prompt)
    # Strip markdown code block delimiters if present
    if output_text.startswith("```json"):
        output_text = output_text[len("```json"):].strip()
    if output_text.endswith("```"):
        output_text = output_text[:-3].strip()
    return json.loads(output_text)

def structure_metrics_agent_llm(text: str, context: str = "") -> dict:
    rubric = (
        "Rubric for Structure:\n"
        "1. Lacks direction; structure is absent or chaotic.\n"
        "2. Organization is inadequate; loosely connected events or details, weak openings/closures.\n"
        "3. Minimally adequate; formulaic or inconsistent structure with mechanical openings/closures.\n"
        "4. Satisfactorily developed; clear opening and closure, though predictable.\n"
        "5. Well shaped; strong organization with consistent flow and effective transitions.\n"
        "6. Exceptionally well structured; compelling, seamless organization with outstanding resolution.\n"
    )
    prompt = (
        "You are an expert evaluator for the 'Structure' dimension using the following rubric:\n"
        f"{rubric}\n"
        "Evaluate the following student writing on Structure. Return a JSON object with keys 'score' (1-6) and 'comment'.\n\n"
        "Student Writing:\n" + text
    )
    output_text = llm_call(prompt)
    # Strip markdown code block delimiters if present
    if output_text.startswith("```json"):
        output_text = output_text[len("```json"):].strip()
    if output_text.endswith("```"):
        output_text = output_text[:-3].strip()
    return json.loads(output_text)

def stance_metrics_agent_llm(text: str, context: str = "") -> dict:
    rubric = (
        "Rubric for Stance (Tone and Style):\n"
        "1. Demonstrates no clear perspective; tone is flat and inappropriate.\n"
        "2. Weak perspective; tone and style are not clearly defined.\n"
        "3. Sporadic demonstration of a clear perspective; uneven tone.\n"
        "4. Adequate perspective; tone is acceptable for purpose.\n"
        "5. Convincing perspective; tone adds interest and is appropriate.\n"
        "6. Consistently powerful perspective; distinctive and sophisticated tone.\n"
    )
    prompt = (
        "You are an expert evaluator for the 'Stance' dimension using the following rubric:\n"
        f"{rubric}\n"
        "Evaluate the following student writing on Stance. Return a JSON object with keys 'score' (1-6) and 'comment'.\n\n"
        "Student Writing:\n" + text
    )
    output_text = llm_call(prompt)
    # Strip markdown code block delimiters if present
    if output_text.startswith("```json"):
        output_text = output_text[len("```json"):].strip()
    if output_text.endswith("```"):
        output_text = output_text[:-3].strip()
    return json.loads(output_text)

def sentence_fluency_agent_llm(text: str, context: str = "") -> dict:
    rubric = (
        "Rubric for Sentence Fluency:\n"
        "1. Sentences are choppy or awkward; little flow.\n"
        "2. Some structural issues causing confusion or unnatural phrasing.\n"
        "3. Minimal flow; rigid or mechanical phrasing with little variation.\n"
        "4. Some flow and rhythm; transitions are sometimes forced.\n"
        "5. Generally rhythmic with effective variation; most sentences are clear.\n"
        "6. Exceptionally fluid and varied; each sentence flows smoothly into the next.\n"
    )
    prompt = (
        "You are an expert evaluator for the 'Sentence Fluency' dimension using the following rubric:\n"
        f"{rubric}\n"
        "Evaluate the following student writing on Sentence Fluency. Return a JSON object with keys 'score' (1-6) and 'comment'.\n\n"
        "Student Writing:\n" + text
    )
    output_text = llm_call(prompt)
    # Strip markdown code block delimiters if present
    if output_text.startswith("```json"):
        output_text = output_text[len("```json"):].strip()
    if output_text.endswith("```"):
        output_text = output_text[:-3].strip()
    return json.loads(output_text)

def diction_metrics_agent_llm(text: str, context: str = "") -> dict:
    rubric = (
        "Rubric for Diction (Language):\n"
        "1. Vocabulary is limited; redundant or incorrectly used words; no imagery.\n"
        "2. Occasional clarity, but with vague or incorrect expressions; little imagery.\n"
        "3. Sometimes clear and precise; mostly simple language with occasional imagery.\n"
        "4. Generally clear and appropriate; some variety but predictable imagery.\n"
        "5. Vivid and precise language; creative and effective imagery.\n"
        "6. Consistently powerful and varied language; imagery is consistently effective.\n"
    )
    prompt = (
        "You are an expert evaluator for the 'Diction' dimension using the following rubric:\n"
        f"{rubric}\n"
        "Evaluate the following student writing on Diction. Return a JSON object with keys 'score' (1-6) and 'comment'.\n\n"
        "Student Writing:\n" + text
    )
    output_text = llm_call(prompt)
    # Strip markdown code block delimiters if present
    if output_text.startswith("```json"):
        output_text = output_text[len("```json"):].strip()
    if output_text.endswith("```"):
        output_text = output_text[:-3].strip()
    return json.loads(output_text)

def conventions_metrics_agent_llm(text: str, context: str = "") -> dict:
    rubric = (
        "Rubric for Conventions:\n"
        "1. Many errors; spelling, usage, punctuation, capitalization, and formatting are poor.\n"
        "2. Several errors that show struggle with basic conventions; extensive editing needed.\n"
        "3. Limited control over conventions; moderate editing required.\n"
        "4. Reasonable control with minor errors; basic conventions mostly followed.\n"
        "5. Few errors; effective control over conventions with some stylistic use.\n"
        "6. Almost error-free; outstanding control of conventions used intentionally for style.\n"
    )
    prompt = (
        "You are an expert evaluator for the 'Conventions' dimension using the following rubric:\n"
        f"{rubric}\n"
        "Evaluate the following student writing on Conventions. Return a JSON object with keys 'score' (1-6) and 'comment'.\n\n"
        "Student Writing:\n" + text
    )
    output_text = llm_call(prompt)
    # Strip markdown code block delimiters if present
    if output_text.startswith("```json"):
        output_text = output_text[len("```json"):].strip()
    if output_text.endswith("```"):
        output_text = output_text[:-3].strip()
    return json.loads(output_text)

def evaluate_writing_metrics(text: str, context: str = "") -> dict:
    """
    Calls all the helper agents to evaluate writing metrics.
    Aggregates the scores and comments from:
      - Content
      - Structure
      - Stance
      - Sentence Fluency
      - Diction
      - Conventions
    Returns a dictionary with individual results and an overall average score.
    """
    content = content_metrics_agent_llm(text, context)
    structure = structure_metrics_agent_llm(text, context)
    stance = stance_metrics_agent_llm(text, context)
    fluency = sentence_fluency_agent_llm(text, context)
    diction = diction_metrics_agent_llm(text, context)
    conventions = conventions_metrics_agent_llm(text, context)
    
    # Aggregate scores (average)
    scores = []
    for res in [content, structure, stance, fluency, diction, conventions]:
        try:
            scores.append(float(res.get("score", 0)))
        except Exception:
            scores.append(0)
    overall = round(sum(scores) / len(scores), 2) if scores else 0
    
    return {
        "Content": content,
        "Structure": structure,
        "Stance": stance,
        "Sentence Fluency": fluency,
        "Diction": diction,
        "Conventions": conventions,
        "Overall": {"score": overall, "comment": "Average score across all dimensions."}
    }

# -------------------------------
# Helper: Dynamic Text Modification
# -------------------------------
def modify_text_for_voice(text: str, vp_results: dict) -> str:
    note = " [Ensure that informal and creative expressions are preserved in your revisions.]"
    return text + note

# -------------------------------
# Orchestrator: Iterative Multi-Agent System
# -------------------------------
def multi_agent_system_iterative(ocr_json: dict, voice_threshold: int = 90, max_iterations: int = 5) -> dict:
    """
    Orchestrates the multi-agent iterative process:
      1. Combine OCR JSON (metadata, Title, Story) into full text.
      2. Iteratively invoke the Grammar & Style Agent and Voice Preservation Agent.
         If the voice score is below the threshold, modify text and iterate.
      3. When voice preservation is acceptable (or max iterations reached), call the Personalized Feedback Agent 
         and evaluate writing metrics using helper agents.
      4. Aggregate all results into a teacher-friendly report.
    """
    metadata = ocr_json.get("metadata", {})
    title = ocr_json.get("Title", "").strip()
    story = ocr_json.get("Story", "").strip()
    full_text = (title + "\n\n" + story).strip()
    
    current_text = full_text
    iteration_logs = []
    iteration = 0
    best_gs_results = None
    best_vp_results = None
    prior_context = ""  # This can be populated from shared memory or logs in a full system.
    
    while iteration < max_iterations:
        iteration += 1
        gs_results = grammar_and_style_agent_llm(current_text, context=prior_context)
        edited_text = gs_results.get("edited_text", current_text)
        vp_results = voice_preservation_agent_llm(full_text, edited_text, context=prior_context)
        voice_score = vp_results.get("voice_score", 0)
        iteration_logs.append({
            "iteration": iteration,
            "input_text": current_text,
            "edited_text": edited_text,
            "voice_score": voice_score,
            "grammar_changes": gs_results.get("changes", [])
        })
        if voice_score >= voice_threshold:
            best_gs_results = gs_results
            best_vp_results = vp_results
            break
        else:
            current_text = modify_text_for_voice(current_text, vp_results)
            best_gs_results = gs_results
            best_vp_results = vp_results

    pf_results = personalized_feedback_agent_llm(metadata, full_text, context=prior_context)
    wm_results = evaluate_writing_metrics(full_text, context=prior_context)
    
    def calculate_overall_score(gs, vp, pf):
        gs["grammar_score"] = int(gs["grammar_score"])
        gs["style_score"] = int(gs["style_score"])
        vp["voice_score"] = int(vp["voice_score"])
        pf["personalized_score"] = int(pf["personalized_score"])
        return round(gs["grammar_score"] * 0.3 + gs["style_score"] * 0.3 + vp["voice_score"] * 0.2 + pf["personalized_score"] * 0.2, 2)
    
    overall_score = calculate_overall_score(best_gs_results, best_vp_results, pf_results)
    
    report = {
        "StudentID": {
            "Name": metadata.get("name", "Unknown"),
            "School": metadata.get("school", "Unknown"),
            "DOB": metadata.get("DOB", "Unknown"),
            "Age": metadata.get("Age", "Unknown")
        },
        "Timestamp": datetime.datetime.now().isoformat(),
        "FinalEditedText": best_vp_results.get("final_text", edited_text),
        "IterationCount": iteration,
        "IterationLogs": iteration_logs,
        "ChangeSuggestions": best_gs_results.get("changes", []),
        "Feedback": {
            "VoicePreservation": best_vp_results.get("voice_feedback", ""),
            "Personalized": pf_results.get("feedback_message", "")
        },
        "Scores": {
            "Grammar": best_gs_results.get("grammar_score", 0),
            "Style": best_gs_results.get("style_score", 0),
            "VoicePreservation": best_vp_results.get("voice_score", 0),
            "PersonalizedFeedback": pf_results.get("personalized_score", 0),
            "Overall": overall_score
        },
        "WritingMetrics": wm_results
    }
    return report

# -------------------------------
# Example Usage
# -------------------------------
if __name__ == "__main__":
    ocr_json = {
        "metadata": {
            "name": "Jane Smith",
            "school": "826 Valencia",
            "DOB": "2008-09-12",
            "Age": 15
        },
        "Title": "A Day at the Park",
        "Story": (
            "Today I went to teh park and saw many interesting things. "
            "I loved the bright colors and the funny sounds. My heart felt light and free."
        )
    }
    
    final_report = multi_agent_system_iterative(ocr_json)
    print(json.dumps(final_report, indent=4))
