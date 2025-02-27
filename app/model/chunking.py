def chunk_text(text, method="sentence", chunk_size=3):
    """Chunk text into sentences or paragraphs."""
    if method == "sentence":
        sentences = text.split(". ")
        return [" ".join(sentences[i:i+chunk_size]) for i in range(0, len(sentences), chunk_size)]
    elif method == "paragraph":
        return text.split("\n\n")
    else:
        raise ValueError("Unsupported chunking method")
