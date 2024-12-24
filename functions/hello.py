import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask!"

def handler(event, context):
    with app.test_request_context():
        response = app.full_dispatch_request()
        return {
            'statusCode': 200,
            'body': response.get_data(as_text=True)
        }