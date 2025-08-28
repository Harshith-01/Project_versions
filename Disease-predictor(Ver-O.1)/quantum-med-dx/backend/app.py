from flask import Flask
from flask_cors import CORS
from ingest import ingest_data
from quantum import QuantumProcessor
from rag import RetrievalAugmentedGenerator
from llm import LargeLanguageModel
from utils import setup_logging
from config import Config

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load configuration
app.config.from_object(Config)

# Initialize logging
setup_logging()

# Initialize components
quantum_processor = QuantumProcessor()
rag_generator = RetrievalAugmentedGenerator()
llm = LargeLanguageModel()

@app.route('/ingest', methods=['POST'])
def ingest():
    data = ingest_data()
    return {"status": "success", "data": data}, 200

@app.route('/quantum', methods=['GET'])
def quantum():
    result = quantum_processor.process()
    return {"result": result}, 200

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json.get('prompt')
    response = llm.generate_text(prompt)
    return {"response": response}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)