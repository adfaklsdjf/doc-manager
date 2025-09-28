#!/usr/bin/env python3
"""
Simple webhook service for paperless-ngx integration.
Logs all incoming request details for analysis and debugging.
"""

import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
import os

# Setup logging
log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, 'webhook_requests.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def webhook_handler():
    """Handle all webhook requests and log details."""

    # Get current timestamp
    timestamp = datetime.now().isoformat()

    # Collect request details
    request_details = {
        'timestamp': timestamp,
        'method': request.method,
        'url': request.url,
        'path': request.path,
        'query_string': request.query_string.decode('utf-8'),
        'headers': dict(request.headers),
        'remote_addr': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'content_type': request.content_type,
        'content_length': request.content_length,
    }

    # Get request body if present
    try:
        if request.is_json:
            request_details['json_data'] = request.get_json()
        elif request.data:
            request_details['raw_data'] = request.data.decode('utf-8', errors='replace')
        elif request.form:
            request_details['form_data'] = dict(request.form)
    except Exception as e:
        request_details['body_error'] = str(e)

    # Log the request
    logger.info(f"Webhook received: {json.dumps(request_details, indent=2)}")

    # Return success response
    response_data = {
        'status': 'received',
        'timestamp': timestamp,
        'message': 'Webhook processed successfully'
    }

    return jsonify(response_data), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with service info."""
    return jsonify({
        'service': 'paperless-webhook-receiver',
        'status': 'running',
        'endpoints': {
            '/webhook': 'Main webhook endpoint (accepts all HTTP methods)',
            '/health': 'Health check',
            '/': 'This info page'
        },
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    logger.info("Starting webhook service...")
    logger.info(f"Logging requests to: {log_file}")

    # Run on all interfaces to accept local network connections
    app.run(host='0.0.0.0', port=5000, debug=True)