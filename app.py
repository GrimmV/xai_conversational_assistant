from flask import Flask, request, make_response, jsonify
from InteractiveBot import InteractiveBot

# Prepare environment variables
from dotenv import load_dotenv
import os
import logging
logging.basicConfig(filename='logging.log', level=logging.DEBUG)

load_dotenv()

CURRENT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# CURRENT_OPENAI_BASE = os.getenv("OPENAI_API_BASE")

# os.environ["OPENAI_DEPLOYMENT_NAME"] = "GPT4Turbo"
os.environ["OPENAI_MODEL_NAME"] = "gpt-4-turbo-preview"

# init GPT Objects
def create_app(config=None):
    app = Flask(__name__)

    standard_bot = InteractiveBot()

    @app.route("/api/test", methods=["GET", "OPTIONS"])
    def test_api():

        print("test")
        
        if request.method == "OPTIONS":
            return _build_cors_preflight_response()
        elif request.method == "GET": 
            gpt_response = standard_bot.handle_request()
            response = make_response(gpt_response)
            print(response)
            return _corsify_actual_response(response)
        else:
            raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))

    def _build_cors_preflight_response():
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

    def _corsify_actual_response(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)