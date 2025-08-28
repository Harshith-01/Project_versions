from flask import Flask
from flask import jsonify
from flask_cors import CORS
from src.routes.diagnose import diagnose_bp
from src.routes.ingest import ingest_bp
from config import settings

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": settings.ALLOWED_ORIGIN}})
    app.register_blueprint(diagnose_bp, url_prefix="/api")
    app.register_blueprint(ingest_bp, url_prefix="/api")
    @app.get("/api/health")
    def health():
        return jsonify({"ok": True})
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=8000, debug=True)
