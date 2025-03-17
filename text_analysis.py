import json
import datetime
from llm_call import llm_call

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

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
# Build Workflow Graph Using LangGraph StateGraph API
# -------------------------------
# We define nodes for grammar, voice, modify, feedback, and metrics.
# The conditional edge from the voice node checks the voice score to decide if we should loop or continue.
# This is our final concrete workflow.
from langgraph.graph import StateGraph  # Using StateGraph from LangGraph

# Define the State schema for our workflow.
# For simplicity, we use a Python dict; in production you might use a TypedDict.
State = dict

def grammar_node(state: State) -> State:
    # Call the grammar agent.
    state["gs_results"] = grammar_and_style_agent_llm(state["current_text"], state.get("prior_context", ""))
    return state

def voice_node(state: State) -> State:
    # Call the voice preservation agent.
    state["vp_results"] = voice_preservation_agent_llm(state["full_text"], state["gs_results"].get("edited_text", state["current_text"]), state.get("prior_context", ""))
    return state

def modify_node(state: State) -> State:
    # Store previous voice score if not already set
    prev_score = state.get("prev_voice_score", 0)
    current_score = state.get("vp_results", {}).get("voice_score", 0)
    
    # Update current text using a more aggressive modification
    state["current_text"] = modify_text_for_voice(state["current_text"], state["vp_results"])
    
    # Log the iteration
    if "iteration_logs" not in state:
        state["iteration_logs"] = []
    state["iteration_logs"].append({
        "input_text": state["current_text"],
        "edited_text": state["gs_results"].get("edited_text", state["current_text"]),
        "voice_score": current_score,
        "grammar_changes": state["gs_results"].get("changes", [])
    })
    
    # Check if improvement is minimal
    improvement = current_score - prev_score
    state["prev_voice_score"] = current_score  # Update for next iteration
    # If improvement is less than 5 and we've iterated at least twice, break out by setting a flag.
    if state.get("iteration_count", 0) >= 2 and improvement < 5:
        state["force_stop"] = True
    return state


def feedback_node(state: State) -> State:
    state["pf_results"] = personalized_feedback_agent_llm(state["metadata"], state["full_text"], state.get("prior_context", ""))
    return state

def metrics_node(state: State) -> State:
    state["wm_results"] = evaluate_writing_metrics(state["full_text"], state.get("prior_context", ""))
    return state

# Define condition function for looping.
def voice_condition(state: State) -> bool:
    # Exit if voice score is at least 80 OR if force_stop is set.
    return state.get("vp_results", {}).get("voice_score", 0) >= 90 or state.get("force_stop", False)

# Build the StateGraph.
graph_builder = StateGraph(State)
graph_builder.add_node("grammar", grammar_node)
graph_builder.add_node("voice", voice_node)
graph_builder.add_node("modify", modify_node)
graph_builder.add_node("feedback", feedback_node)
graph_builder.add_node("metrics", metrics_node)

# Define edges:
graph_builder.add_edge(START, "grammar")
graph_builder.add_edge("grammar", "voice")
# Use conditional edges from voice node:
def route_from_voice(state: State) -> str:
    return "modify" if voice_condition(state) else "feedback"
graph_builder.add_conditional_edges("voice", route_from_voice)
graph_builder.add_edge("modify", "grammar")
graph_builder.add_edge("feedback", "metrics")
graph_builder.add_edge("metrics", END)

# Compile the graph with a checkpointer.
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# -------------------------------
# Orchestrator: Execute Workflow Using LangGraph's invoke API
# -------------------------------
def run_workflow(ocr_json: dict, max_iterations: int = 5, context_dir="context_storage") -> dict:
    metadata = ocr_json.get("metadata", {})
    title = ocr_json.get("Title", "").strip()
    story = ocr_json.get("Story", "").strip()
    full_text = (title + "\n\n" + story).strip()
    prior_context = ""
    
    # Prepare initial state.
    state = {
        "metadata": metadata,
        "full_text": full_text,
        "current_text": full_text,
        "prior_context": prior_context
    }
    
    # Provide a config with required keys and increase recursion_limit.
    config = {
        "recursion_limit": 25,
        "configurable": {
            "thread_id": "1",
            "checkpoint_ns": "",
            "checkpoint_id": "1"
        }
    }
    
    # Invoke the graph with the configuration.
    final_state = graph.invoke(state, config)
    
    overall_score = (final_state["gs_results"].get("grammar_score", 0) * 0.3 +
                     final_state["gs_results"].get("style_score", 0) * 0.3 +
                     final_state["vp_results"].get("voice_score", 0) * 0.2 +
                     final_state["pf_results"].get("personalized_score", 0) * 0.2)
    overall_score = round(overall_score, 2)
    
    report = {
        "StudentID": metadata,
        "Timestamp": datetime.datetime.now().isoformat(),
        "FinalEditedText": final_state["vp_results"].get("final_text", full_text),
        "IterationLogs": final_state.get("iteration_logs", []),
        "ChangeSuggestions": final_state["gs_results"].get("changes", []),
        "Feedback": {
            "VoicePreservation": final_state["vp_results"].get("voice_feedback", ""),
            "Personalized": final_state["pf_results"].get("feedback_message", "")
        },
        "Scores": {
            "Grammar": final_state["gs_results"].get("grammar_score", 0),
            "Style": final_state["gs_results"].get("style_score", 0),
            "VoicePreservation": final_state["vp_results"].get("voice_score", 0),
            "PersonalizedFeedback": final_state["pf_results"].get("personalized_score", 0),
            "Overall": overall_score
        },
        "WritingMetrics": final_state.get("wm_results", {})
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
    
    final_report = run_workflow(ocr_json, max_iterations=5, context_dir="context_storage")
    print(json.dumps(final_report, indent=4))