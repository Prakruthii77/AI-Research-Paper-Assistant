from transformers import pipeline

explainer = pipeline(
    "text-generation",
    model="gpt2"
)

def explain_methodology(text):
    prompt = f"Explain the methodology in simple words:\n{text}"
    
    try:
        return explainer(
            prompt,
            max_length=180
        )[0]["generated_text"]
    except Exception:
        return "Methodology explanation failed."