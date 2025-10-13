import os, getpass, time, json
from typing import List
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain.schema import AIMessage
from backend.app.utils import chunk_code
from backend.app.models import(
    Issue,
    FileAnalysis,
    Summary,
    AnalysisResult,
    PRResponse
)
from dotenv import load_dotenv
load_dotenv()

#   Initialize Model + Agent
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")


def get_agent():
    """Initialize Gemini model and tool schema using the Pydantic model."""
    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_analysis_result",
                "description": "Return code analysis results in a structured format.",
                "parameters": AnalysisResult.model_json_schema(),
            },
        }
    ]
    model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    return create_react_agent(model, tools)

#Main Workflow
def analyze_pr_files(task_id:int ,pr_files: List[dict]) -> PRResponse:
    """
    Accepts PR file data [{filename: ..., extension: ..., content: ..., status: ...}]
    Splits large PRs into chunks and sends them to Gemini to produce structured results.
    Returns a PRResponse object validated via Pydantic.
    """
    agent = get_agent()
    all_file_results = []

    for f in pr_files:
        filename = f["filename"]
        content = f["content"]
        status = f["status"]
        ext = f["extension"]

        if content is None:
            continue

        chunks = chunk_code(content)
        file_issues = []

        for chunk in chunks:
            attempt = 0
            MAX_RETRIES = 5
            prompt = (
                f"You are an expert code reviewer. Analyze the following {ext} file `{filename}` (status: {status}). "
                "Return *only* valid JSON by calling the tool `generate_analysis_result`. "
                "Do not include markdown, explanations, or extra text.\n\n"
                f"Code:\n{chunk}"
            )

            while attempt < MAX_RETRIES:
                try:
                    response = agent.invoke({
                        "messages": [{"role": "user", "content": prompt}]
                    })
                    print("TYPE OF RESPONSE:", type(response))
                    print("RESPONSE CONTENT:", response)
                    # structured_output = response.choices[0].message.tool_calls[0].function.arguments
                    structured_output = None
                    # Find the AIMessage that contains the tool call
                    for msg in response["messages"]:
                        if isinstance(msg, AIMessage):
                            func_call = msg.additional_kwargs.get("function_call")
                            if func_call and "arguments" in func_call:
                                # arguments is a JSON string
                                structured_output = json.loads(func_call["arguments"])
                                break


                    #  validate using Pydantic
                    try:
                        parsed = AnalysisResult.model_validate(structured_output)
                        # Add validated issues
                        for file in parsed.files:
                            file_issues.extend(file.issues)
                        break  # success, stop retrying
                    except Exception as parse_err:
                        file_issues.append(Issue(
                            type="error",
                            line=0,
                            description=f"Parsing error: {parse_err}",
                            suggestion="Verify JSON structure."
                        ))
                        break

                except Exception as e:
                    if "429" in str(e):  # rate limit
                        wait = min(2 ** attempt, 60)
                        time.sleep(wait)
                        attempt += 1
                    else:
                        file_issues.append(Issue(
                            type="error",
                            line=0,
                            description=f"Error analyzing chunk: {e}",
                            suggestion="Check manually"
                        ))
                        break

        all_file_results.append(FileAnalysis(name=filename, issues=file_issues))

    # Prepare summary 
    total_files = len(all_file_results)
    total_issues = sum(len(f.issues) for f in all_file_results)
    critical_issues = sum(
        1 for f in all_file_results for i in f.issues if i.type == "bug"
    )

    summary = Summary(
        total_files=total_files,
        total_issues=total_issues,
        critical_issues=critical_issues
    )

    #Prepare Response
    result = AnalysisResult(files=all_file_results, summary=summary)
    response = PRResponse(task_id=task_id, status="completed", results=result)
    return response.model_dump()

