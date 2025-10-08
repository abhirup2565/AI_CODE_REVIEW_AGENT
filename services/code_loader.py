def load_file_content(file_dict, github_token=None):
    """
    Load patch.
    """
    content = file_dict.get("patch", "")
    ext = file_dict["extension"]
    # Add file type header for AI context
    if ext in ["py"]:
        return f"# Python file: {file_dict['filename']}\n{content}"
    elif ext in ["js", "ts"]:
        return f"// JavaScript file: {file_dict['filename']}\n{content}"
    elif ext in ["java"]:
        return f"// Java file: {file_dict['filename']}\n{content}"
    else:
        return f"// File: {file_dict['filename']}\n{content}"


def chunk_text(text, max_tokens=2000):
    """
    Split large text into chunks suitable for LLM input.
    """
    lines = text.splitlines()
    chunks = []
    current_chunk = ""
    current_tokens = 0

    for line in lines:
        current_chunk += line + "\n"
        current_tokens += len(line.split())  # rough token estimate

        if current_tokens >= max_tokens:
            chunks.append(current_chunk)
            current_chunk = ""
            current_tokens = 0

    if current_chunk:
        chunks.append(current_chunk)
    return chunks
