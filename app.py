import os
import subprocess
import re
from flask import Flask, request, jsonify, render_template
import googleapiclient.discovery
from extract_comment import fetch_and_save_comments
from query_data import query_rag
from get_embedding_function import get_embedding_function

app = Flask(__name__)

# YouTube API key (Replace with your actual API key)
API_KEY = 'AIzaSyDj7I12G6kpxEt4esWYXh2XwVAOXu7mbz0'


@app.route('/')
def home():
    return render_template('index1.html')  # Render the chat interface (index.html)

@app.route('/user_message', methods=['POST'])
def user_message():
    user_message = request.json.get('message')
    print(f"User message: {user_message}")


@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')  # Get the user message (YouTube URL or query)
    print(f"User message: {user_message}")
    
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    try:
        # Fetch comments from YouTube and save them to Chroma
        fetch_and_save_comments(user_message, API_KEY)
        print("Comments fetched and saved to Chroma.")
        return jsonify({"response": "Comments fetched and saved to Chroma."}), 200
    except Exception as e:
        print(f"Error fetching comments: {e}")
        return jsonify({"response": "Failed to fetch comments"}), 500

@app.route('/query', methods=['POST'])
def query():
    query_text = request.json.get('query_text')
    print(f"Query text: {query_text}")

    if not query_text:
        return jsonify({"response": "No query text provided"}), 400

    # Run query_rag on the user input query text
    response_text = query_rag(query_text)
    print(f"Query response: {response_text}")

    return jsonify({"response": response_text})


if __name__ == '__main__':
    app.run(debug=True)


