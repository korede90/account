import spacy

nlp = spacy.load("extract_model")

doc = nlp("""
          welcome boss
          """)  # <-- corrected closing quotes

for ent in doc.ents:
    print(ent.text, ent.label_)
