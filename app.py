from flask import Flask, request, jsonify
from ragie import Ragie
import os

app = Flask(__name__)
ragie = Ragie(auth="tnt_EL53HDpGqW1_W1PFdKGbFJ8rAIVh2mz7j5dtSFA5B6dTF6wYnwXeDAs")

'''
@app.route('/ingest', methods=['POST'])
def ingest():
    files = request.files.getlist('file')
    results = []

    for f in files:
        filename = f.filename
        content_bytes = f.read()
        f.seek(0)

        response = ragie.documents.create(request={
            "file": {
                "file_name": filename,
                "content": content_bytes
            },
            "metadata": {
                "source": "call_center"
            },
            "mode": {
                "audio": True  
            }
        })

        results.append({
            "document_id": response.id,
            "status": response.status
        })

    return jsonify(results), 202
'''

@app.route('/ingest', methods=['POST'])
def ingest():
    files = request.files.getlist('file')
    results = []
    for f in files:
        filename = f.filename
        # Read the file content as bytes for Ragie
        file_content = f.read()
        
        response = ragie.documents.create(request={
            "file": {
                "file_name": filename,
                "content": file_content  # Use the bytes content directly
            },
            "metadata": {
                "source": "call_center" # custom metadata, not a Ragie param but for our reference 
            },
            "mode": {"audio": True}  # Explicitly enable audio processing mode
        })
        results.append({"document_id": response.id, "status": response.status})
    return jsonify(results), 202


@app.route('/status/<document_id>', methods=['GET'])
def check_status(document_id):
    try:
        doc = ragie.documents.get(document_id=document_id)
        return jsonify({
            "document_id": document_id,
            "status": doc.status
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/retrieve', methods=['GET'])
def retrieve():
    user_query = request.args.get('q')
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    response = ragie.retrievals.retrieve(request={
        "query": user_query
       
    })
    chunks = []
    for chunk in response.scored_chunks:
        chunks.append({
            "text": chunk.text,
            "score": chunk.score,
            "document_id": chunk.document_id,
            "metadata": chunk.document_metadata
        })
    return jsonify({"query": user_query, "results": chunks}), 200


if __name__ == '__main__':
    app.run(debug=True)