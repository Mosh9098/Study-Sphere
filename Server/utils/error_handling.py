from flask import jsonify

def handle_not_found(message):
    response = {
        "error": "Not Found",
        "message": message
    }
    return jsonify(response), 404

def handle_validation_error(errors):
    response = {
        "error": "Validation Error",
        "messages": errors
    }
    return jsonify(response), 400
