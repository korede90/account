import spacy
import json
import random
from spacy.training import Example

# Load your data from the JSON file
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
        annotations = entry["entities"]

        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, {"entities": annotations})

        nlp.update([example], drop=0.5, losses=losses)

    print(f"Losses: {losses}")

# Save the trained model
nlp.to_disk("extract_model")