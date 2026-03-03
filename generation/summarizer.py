from transformers import pipeline

summarizer_model = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def summarize(text):
    try:
        return summarizer_model(
            text,
            max_length=180,
            min_length=60
        )[0]["summary_text"]
    except Exception:
        return "Summary could not be generated."