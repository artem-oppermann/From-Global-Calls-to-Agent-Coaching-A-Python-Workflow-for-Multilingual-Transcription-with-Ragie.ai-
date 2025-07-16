# Multilingual Call Center Transcription with Ragie.ai

A Python Flask application that demonstrates how to build a robust pipeline for transcribing multilingual call center recordings using Ragie.ai's RAG-as-a-Service platform. This workflow automatically processes audio files, transcribes them in multiple languages, and prepares the output for sentiment analysis.

## Features

- **Multilingual Transcription**: Automatic transcription in 100+ languages using Ragie.ai
- **Flask API**: RESTful endpoints for ingesting audio files and retrieving transcripts
- **Sentiment Analysis**: Optional microservice for analyzing transcript sentiment
- **Real-time Processing**: Upload audio files and query transcripts via HTTP API
- **Hybrid Retrieval**: Semantic and keyword-based search through transcribed content

## Architecture

```
Audio Files → Flask API → Ragie.ai → Indexed Transcripts → Sentiment Analysis
```

The solution consists of:
1. **Input Layer**: Audio and text files (MP3, WAV, M4A, etc.)
2. **API Layer**: Python Flask server with ingestion and retrieval endpoints
3. **Processing Layer**: Ragie.ai for transcription, chunking, and indexing
4. **Analysis Layer**: Optional sentiment analysis microservice

## Prerequisites

- Python 3.9+
- pip package manager
- Virtual environment (recommended)
- Ragie.ai account and API key

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd call-center-transcription
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Ragie.ai API key**:
   - Sign up at [Ragie.ai](https://secure.ragie.ai/sign-up)
   - Get your API key from Settings > API Key
   - Export it as an environment variable:
   ```bash
   export RAGIE_API_KEY=your_api_key_here
   ```

## File Structure

```
project/
├── app.py                 # Main Flask application
├── sentiment_service.py   # Optional sentiment analysis service
├── requirements.txt       # Python dependencies
├── sample_call.mp3       # Sample audio file for testing
└── README.md             # This file
```

## Usage

### 1. Start the Main Application

```bash
python app.py
```

The Flask server will start on `http://localhost:5000` with the following endpoints:

- `POST /ingest` - Upload audio files for transcription
- `GET /retrieve?q=query` - Search transcripts with natural language queries
- `GET /status/<document_id>` - Check processing status of uploaded files

### 2. Upload Audio Files

```bash
curl -X POST \
     -F "file=@sample_call.mp3" \
     http://localhost:5000/ingest
```

Response:
```json
[
  {
    "document_id": "7dfdb3b5-4f4c-432c-8f65-d0d879cb1d29",
    "status": "partitioning"
  }
]
```

### 3. Check Processing Status

```bash
curl http://localhost:5000/status/7dfdb3b5-4f4c-432c-8f65-d0d879cb1d29
```

Wait for status to change from "partitioning" to "ready".

### 4. Query Transcripts

```bash
curl "http://localhost:5000/retrieve?q=shipped+wrong+product"
```

Response:
```json
{
  "query": "shipped wrong product",
  "results": [
    {
      "document_id": "7dfdb3b5-4f4c-432c-8f65-d0d879cb1d29",
      "metadata": {
        "language": "auto",
        "source": "call_center"
      },
      "score": 0.19090909090909092,
      "text": "{\"audio_transcript\": \"...transcript content...\"}"
    }
  ]
}
```

### 5. Optional: Sentiment Analysis

Start the sentiment analysis service:

```bash
python sentiment_service.py
```

The service runs on `http://localhost:6000` and provides:
- `POST /sentiment` - Analyze text sentiment

Example combined workflow:
```bash
curl -s "http://localhost:5000/retrieve?q=customer+complaint" \
| jq -r '.results[].text' \
| while IFS= read -r snippet; do
    payload=$(jq -nc --arg t "$snippet" '{text: $t}')
    curl -s -H "Content-Type: application/json" -d "$payload" http://localhost:6000/sentiment
done
```


#### GET /status/<document_id>
Check processing status of uploaded documents.

**Response:**
```json
{
  "document_id": "string",
  "status": "partitioning|ready|error"
}
```

## Supported File Formats

Ragie.ai supports various audio formats:
- MP3
- WAV
- M4A
- OGG
- FLAC
- And more...

## Supported Languages

Ragie.ai supports transcription in 100+ languages including:
- English
- Spanish
- French
- German
- Chinese (Mandarin)
- Japanese
- Korean
- Portuguese
- Italian
- Russian
- Arabic
- Hindi
- And many more...

See the [full list of supported languages](https://docs.ragie.ai/docs/supported-transcription-languages).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Resources

- [Ragie.ai Documentation](https://docs.ragie.ai/docs/overview)
- [Ragie.ai Python SDK](https://docs.ragie.ai/docs/ragie-python)
- [Supported File Types](https://docs.ragie.ai/docs/supported-file-types)
- [Supported Languages](https://docs.ragie.ai/docs/supported-transcription-languages)
- [Sign up for Ragie.ai](https://secure.ragie.ai/sign-up)

