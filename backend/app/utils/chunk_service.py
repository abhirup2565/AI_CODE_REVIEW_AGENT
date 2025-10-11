def chunk_code(content: str, chunk_size: int = 1000): #set default chunk size
    """
    Split large code into manageable chunks.
    """
    return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]