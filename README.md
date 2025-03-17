# 826 Valencia AI Editing & Translation Tool

This project is an AI-powered tool designed to assist the 826 Valencia writing programs by streamlining the editing and translation process for student writing. The tool performs three key tasks:

1. **Text Extraction:** Extracts text from student writing images.
2. **Text Analysis:** Performs grammar and tone (copyediting) analysis, preserving the student’s unique voice and providing detailed feedback.
3. **Text Translation:** Translates text between English and Spanish, accommodating students who write in Spanish.

## Key Features

### Privacy-First Approach
- **Local LLM Inference:**  
  The project uses a local LLM (Gemma3 4b on Ollama) for all inference tasks. By running the model locally, we ensure that sensitive student writing is never sent to a central API or external server, maintaining strict privacy for student data.

### Multi-Agent Orchestration with LangGraph
- **Orchestrated Workflow:**  
  The editing component is built using LangGraph’s StateGraph API, which creates a multi-agent, conditional workflow. This orchestrated design allows for:
  - **Conditional Routing:** The workflow intelligently routes the text through grammar correction, voice preservation checks, personalized feedback, and overall writing metrics evaluation.
  - **Iterative Processing:** Loops and conditional edges enable iterative improvements, ensuring that the final output meets high standards.
  - **Modularity and Extensibility:** Each component (grammar, voice, feedback, metrics) is implemented as a separate node in the graph, making it easy to modify or extend any part of the workflow.

## Project Structure

- **llm_call.py:**  
  Handles communication with the local LLM via the Ollama CLI.

- **text_extraction.py:**  
  Uses `llm_call` to extract text from an image file containing student writing.

- **text_translate.py:**  
  Provides functions to translate text between English and Spanish.

- **text_analysis.py:**  
  Implements the multi-agent workflow for copyediting and feedback using LangGraph’s StateGraph API.

- **app.py:**  
  A Streamlit app that integrates all modules into a unified, interactive user interface for extracting, analyzing, and translating student writing.

## Setup & Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/dhruv1220/word-weavers.git
   ```

2. **Create and Activate a Python 3.11 Virtual Environment:**

   ```bash
   python3.11 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Configure the Local LLM (Ollama):**  
   Make sure Ollama is installed and that your local model (Gemma3 4b) is accessible.

## Running the App

Start the Streamlit app by running:

```bash
streamlit run app.py
```

This will launch a web interface where you can:

- Upload an image of student writing.
- Extract text from the image.
- If the text is in Spanish, automatically translate it to English for analysis.
- Run a multi-agent analysis workflow (grammar & tone, voice preservation, personalized feedback, writing metrics) powered by LangGraph.
- Translate the corrected text back to Spanish if needed.

## Privacy & Data Handling

- **Local Processing:**  
  All LLM inferences are performed locally on your machine using Ollama. This ensures that sensitive student data is processed privately without leaving your local environment.

- **Data Isolation:**  
  The system is designed to keep student submissions secure, and no sensitive data is transmitted over the network.

## Multi-Agent Orchestration

- **StateGraph Workflow:**  
  The editing and feedback pipeline is implemented using LangGraph’s StateGraph API. The workflow includes:
  - A grammar and style check node.
  - A voice preservation check node.
  - A conditional loop node that updates the text if necessary.
  - Nodes for personalized feedback and overall writing metrics.
- **Modularity:**  
  Each step in the process is a self-contained node, making it easy to adjust or extend the workflow as needed.

