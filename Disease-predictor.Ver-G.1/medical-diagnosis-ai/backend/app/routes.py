# /backend/app/routes.py
from flask import current_app, jsonify, request
from .services.diagnosis_service import DiagnosisService
from .models.pydantic_models import DiagnosisRequest, DiagnosisResponse

@current_app.route('/diagnose', methods=['POST'])
def diagnose():
    try:
        # Validate request body
        data = DiagnosisRequest(**request.json)
    except Exception as e:
        return jsonify({"error": "Invalid request format", "details": str(e)}), 400

    # Initialize the service and process the request
    diagnosis_service = DiagnosisService()
    response_data = diagnosis_service.process_request(data)

    # Validate and return the response
    return DiagnosisResponse(**response_data).dict(), 200