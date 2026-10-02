import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)


# ============================================================
# MODEL CONFIGURATION
# ============================================================

MODEL_NAME = "facebook/bart-large-cnn"

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ============================================================
# GLOBAL MODEL VARIABLES
# ============================================================

_tokenizer = None
_model = None


# ============================================================
# LOAD BART MODEL ONLY WHEN NEEDED
# ============================================================

def load_summarization_model():

    global _tokenizer
    global _model

    if _tokenizer is None or _model is None:

        print("Loading BART tokenizer...")
        _tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

        print("Loading BART model...")
        _model = AutoModelForSeq2SeqLM.from_pretrained(
            MODEL_NAME
        )

        _model = _model.to(DEVICE)
        _model.eval()

        print("BART model loaded successfully!")

    return _tokenizer, _model


# ============================================================
# GENERATE SUMMARY
# ============================================================

def generate_summary(text):

    if not text or not text.strip():
        return "No information available for summarization."

    tokenizer, model = load_summarization_model()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=1024,
        truncation=True
    )

    inputs = {
        key: value.to(DEVICE)
        for key, value in inputs.items()
    }

    with torch.no_grad():

        summary_ids = model.generate(
            **inputs,
            max_length=130,
            min_length=30,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=3
        )

    summary = tokenizer.decode(
        summary_ids[0],
        skip_special_tokens=True
    )

    return summary


# ============================================================
# TEST ONLY WHEN RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    sample_text = """
    Severe flooding has affected several houses in Coimbatore.
    Five people are trapped and residents urgently need food
    and medical assistance. Rescue teams are requested immediately.

    Heavy rainfall has caused water levels to rise rapidly in
    several areas. Roads have been flooded and transportation
    has been disrupted.

    Local residents have requested emergency rescue operations.
    Medical teams and food supplies are also required.

    Authorities are monitoring the situation and evacuation
    operations are being considered for severely affected areas.
    """

    print("\n====================================")
    print("DISASTER SITUATION SUMMARIZATION")
    print("====================================")

    print("\nGenerated Summary:\n")

    result = generate_summary(sample_text)

    print(result)
