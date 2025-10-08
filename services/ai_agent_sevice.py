import os,getpass,time,json
from typing import List
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from services.chunk_service import chunk_code
from dotenv import load_dotenv
load_dotenv()
# --- Defining individual tools ---
@tool
def analyze_code_chunk(code_chunk: str) -> str:
    """
    Analyze a code chunk and identify potential issues, improvements, and suggestions.
    """
    return f"Analyzing code chunk of length {len(code_chunk)} — possible improvements will be listed here."

@tool
def suggest_fixes(issue_description: str) -> str:
    """
    Suggest fixes for a given issue description.
    """
    return f"Suggested fix for: {issue_description}"

#list all the tools for LLM
tools=[analyze_code_chunk,suggest_fixes]

# Initialize LangGraph model
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

def get_agent():
    model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    agent = create_react_agent(model, tools)
    return agent

#-----------------------
def extract_response_content(response):
    """
    Safely extract text from agent.invoke() output.
    Handles dict, list, or AIMessage objects.
    """
    # If it's a dict with messages
    if isinstance(response, dict):
        messages = response.get("messages", [])
        if messages:
            msg = messages[-1]
            if hasattr(msg, "content"):
                return msg.content
            elif isinstance(msg, dict):
                return msg.get("content", "")
        return str(response)

    # If it's a single AIMessage object
    elif isinstance(response, AIMessage):
        return response.content

    # Fallback to string
    return str(response)
# --- Main analysis workflow ---
def analyze_pr_files(pr_files: List[dict]) -> List[dict]:
    """
    Accepts PR file data {filename: {"extension": ..., "content": ...}}
    Splits large PRs into manageable chunks and sends to the agent.
    """
    agent = get_agent()
    results = []

    for f in pr_files:
        filename = f["filename"]
        content = f["content"]
        status = f["status"]
        ext = f["extension"]

        if not content:
            continue


        chunks = chunk_code(content) #default chunk size is set
        file_analysis = []
        MAX_RETRIES = 5

        for chunk in chunks:
                attempt = 0
                user_prompt = (
                    f"Analyze the following {ext} file `{filename}` (status: {status}). "
                    f"Find issues and return a JSON list of objects like this:\n"
                    f"[{{'type': 'bug'|'style', 'line': int, 'description': str, 'suggestion': str}}]\n\n"
                    f"Code:\n{chunk}"
                )
                while attempt < MAX_RETRIES:
                    try:
                        response = agent.invoke({"messages": [{"role": "user", "content": user_prompt}]})
                        content = extract_response_content(response)
                        # --- Parse AI output safely ---
                        try:
                            ai_issues = json.loads(content)
                            if isinstance(ai_issues, list):
                                for issue in ai_issues:
                                    if isinstance(issue, dict):
                                        file_analysis.append(issue)
                                    else:
                                        file_analysis.append({
                                            "type": "info",
                                            "line": 0,
                                            "description": str(issue),
                                            "suggestion": "Check manually"
                                        })
                            else:
                                file_analysis.append({
                                    "type": "info",
                                    "line": 0,
                                    "description": str(ai_issues),
                                    "suggestion": "Check manually"
                                })
                        except json.JSONDecodeError:
                            # fallback dummy
                            file_analysis.append({
                            "type": "error",
                            "line": 0,
                            "description": f"Unparsable AI output: {content[:120]}",
                            "suggestion": "Review manually"
                            })
                        break
                    except Exception as e:
                        if "429" in str(e):
                            wait = max(2 ** attempt, 60)  # exponential backoff, max 60s
                            time.sleep(wait)
                            attempt += 1
                        else:
                            file_analysis.append({
                            "type": "error",
                            "line": 0,
                            "description": f"Error analyzing chunk: {e}",
                            "suggestion": "Retry manually"
                        })
                        break

        results.append({
            "file": filename,
            "status": status,
            "extension": ext,
            "analysis": file_analysis
        })

    return results
