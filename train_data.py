import spacy
import re
import json
import random
from spacy.training import Example

# Abbreviation normalization map
abbreviations = {
    "uba": "united bank of africa",
    "gtbank": "guaranty trust bank",
    "paycom": "paycom",
    "vfd microfinance bank": "vfd microfinance bank",
    "fbn": "first bank of nigeria plc",
    "fcmb": "first city monument bank plc"
}

# Function to normalize abbreviations
def normalize_abbreviations(text):
    for abbr, full_name in abbreviations.items():
        text = re.sub(rf"\b{abbr}\b", full_name, text, flags=re.IGNORECASE)
    return text

# Load data from the JSON file
with open("account_training_data.json", "r", encoding="utf-8") as f:
    TRAIN_DATA = json.load(f)

# Load the spaCy model
nlp = spacy.blank("en")

# Create a new NER component if it doesn't exist
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner", last=True)
else:
    ner = nlp.get_pipe("ner")

# Add the new labels to the NER component
for entry in TRAIN_DATA:
    for ent in entry["entities"]:
        ner.add_label(ent[2])

# Training the model
optimizer = nlp.begin_training()
for epoch in range(80):
    print(f"Epoch {epoch}")
    random.shuffle(TRAIN_DATA)
    losses = {}
    for entry in TRAIN_DATA:
        text = entry["text"]
        clean_text = normalize_abbreviations(text)
        
        # Clean the text: remove brackets and normalize case
        clean_text = re.sub(r"\((.*?)\)", r" \1 ", clean_text)
        clean_text = clean_text.lower()  # Convert to lowercase

        # Create the document object for spaCy
        doc = nlp.make_doc(clean_text)
        example = Example.from_dict(doc, {"entities": entry["entities"]})

        # Update the model with the example
        nlp.update([example], drop=0.5, losses=losses)

    print(f"Losses: {losses}")

# Save the trained model
nlp.to_disk("extract_model")
print("Model built succcessfully and saved to extract_model")
