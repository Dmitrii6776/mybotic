import requests
import logging
import os
from flask import Flask, jsonify, request
from requests.auth import HTTPBasicAuth

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# --- Freqtrade API Configuration ---
FREQTRADE_URL = "http://freqtrade:8080/api/v1"  # Adjust if needed
FT_USERNAME = os.environ.get("FT_API_USER", "freqtrader")  # Default matches config
FT_PASSWORD = os.environ.get("FT_API_PASS", "YOUR_SECURE_PASSWORD")  # Get from env


def call_ft_api(endpoint, method='GET', params=None, json_data=None):
    """
    Helper function to call the Freqtrade API.

    Args:
        endpoint (str): The API endpoint to call (e.g., '/status').
        method (str, optional): The HTTP method to use ('GET' or 'POST'). Defaults to 'GET'.
        params (dict, optional): Query parameters for the request. Defaults to None.
        json_data (dict, optional): JSON data for the request body (for POST). Defaults to None.

    Returns:
        tuple: A tuple containing the JSON response data and the HTTP status code.
               Returns an error message and status code on failure.
    """
    url = f"{FREQTRADE_URL}/{endpoint.lstrip('/')}"
    auth = HTTPBasicAuth(FT_USERNAME, FT_PASSWORD)
    try:
        if method.upper() == 'GET':
            response = requests.get(url, auth=auth, params=params, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, auth=auth, params=params, json=json_data, timeout=10)
        else:
            return {"error": "Unsupported HTTP method"}, 500

        response.raise_for_status()
        return response.json(), response.status_code

    except requests.exceptions.Timeout:
        logging.error(f"Timeout calling Freqtrade API endpoint: {endpoint}")
        return {"error": "Freqtrade API request timed out"}, 504
    except requests.exceptions.ConnectionError:
        logging.error(f"Connection error calling Freqtrade API endpoint: {endpoint}. Is Freqtrade running?")
        return {"error": "Could not connect to Freqtrade API"}, 503
    except requests.exceptions.HTTPError as e:
        logging.error(
            f"HTTP error calling Freqtrade API endpoint: {endpoint}. Status: {e.response.status_code}, Response: {e.response.text[:200]}")
        try:
            err_data = e.response.json()
        except ValueError:
            err_data = {"error": f"HTTP error {e.response.status_code}", "details": e.response.text[:200]}
        return err_data, e.response.status_code
    except Exception as e:
        logging.error(f"Unexpected error calling Freqtrade API: {e}", exc_info=True)
        return {"error": "An unexpected error occurred"}, 500


@app.route('/')
def index():
    """
    Index route for the Flask application.

    Returns:
        str: A message indicating the server is running.
    """
    return "Freqtrade API Interaction Server Running. Use endpoints like /ft/status."


@app.route('/ft/status')
def get_ft_status():
    """
    Get the status from the running Freqtrade bot.

    Returns:
        tuple: A tuple containing the JSON response data and the HTTP status code.
    """
    data, status_code = call_ft_api('/status')
    return jsonify(data), status_code


@app.route('/ft/profit')
def get_ft_profit():
    """
    Get profit summary from the running Freqtrade bot.

    Returns:
        tuple: A tuple containing the JSON response data and the HTTP status code.
    """
    data, status_code = call_ft_api('/profit')
    return jsonify(data), status_code


@app.route('/ft/balance')
def get_ft_balance():
    """
    Get balance information from the running Freqtrade bot.

    Returns:
        tuple: A tuple containing the JSON response data and the HTTP status code.
    """
    data, status_code = call_ft_api('/balance')
    return jsonify(data), status_code


@app.route('/ft/forcebuy', methods=['POST'])
def force_buy():
    """
    Force buy a pair (use carefully!).

    Expects a JSON request body with a 'pair' field.
    An optional 'price' field can also be provided.

    Returns:
        tuple: A tuple containing the JSON response data and the HTTP status code.
    """
    req_data = request.get_json()
    if not req_data or 'pair' not in req_data:
        return jsonify({"error": "Missing 'pair' in request body"}), 400

    pair = req_data['pair']
    price = req_data.get('price')
    params = {'pair': pair}
    if price:
        params['price'] = price

    data, status_code = call_ft_api('/forceentry', method='POST', params=params)
    return jsonify(data), status_code


if __name__ == '__main__':
    logging.info("Starting Flask server for Freqtrade API interaction...")
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)