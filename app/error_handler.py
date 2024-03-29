from flask import jsonify


class ErrorHandler:
    @staticmethod
    def handle_auth_error(auth_error):
        return jsonify({
            "success": False,
            "error": auth_error.get_status_code(),
            "message": auth_error.get_message(),
        }), auth_error.get_status_code()

    @staticmethod
    def handle_client_error(client_error_exception):
        return jsonify({
            "success": False,
            "message": client_error_exception.get_message(),
        }), client_error_exception.get_status_code()

    @staticmethod
    def handle_internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500
