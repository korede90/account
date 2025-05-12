from flask import Flask, request, jsonify
import spacy


app = Flask(__name__)

# Load the trained model
nlp = spacy.load("extract_model")

@app.route('/extract', methods=['POST'])
def extract():
    data = request.get_json()
    text = data.get("text", "")
    
    doc = nlp(text)
    
    results = []
    
    for ent in doc.ents:
        results.append({
            "text": ent.text,
            "label": ent.label_
        })
        
    return jsonify({
        "entities": results
    })
    
if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5050, debug=True)