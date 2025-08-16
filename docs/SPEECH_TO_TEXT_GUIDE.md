# 🎤 Speech-to-Text Integration

This document describes the speech-to-text functionality added to the Ethic Companion V2 project using OpenAI's Whisper API.

## 🚀 Features Added

### 1. Core Function: `speech_to_text()`

An asynchronous function that converts audio files to text using OpenAI's Whisper API.

**Features:**
- ✅ Asynchronous processing
- ✅ Multiple audio format support (WAV, MP3, WEBM, OGG, FLAC, M4A)
- ✅ Comprehensive error handling
- ✅ Portuguese language optimization
- ✅ Proper API key management
- ✅ Detailed logging

### 2. API Endpoints

#### `/speech-to-text` (POST)
- **Purpose**: Transcribe audio file to text
- **Input**: Audio file via multipart/form-data
- **Output**: JSON with transcribed text and metadata

#### `/voice-chat` (POST)  
- **Purpose**: Complete voice interaction (transcribe + chat response)
- **Input**: Audio file via multipart/form-data
- **Output**: Chat response based on transcribed audio

## 🔧 Setup Instructions

### 1. Install Dependencies
```bash
pip install openai>=1.0.0
```

### 2. Configure API Key

#### Local Development (.env file):
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

#### Production (Google Secret Manager):
Create a secret named `ethic-companion-openai-api-key` in your Google Cloud project.

### 3. Get OpenAI API Key
1. Visit: https://platform.openai.com/api-keys
2. Create a new API key
3. Add it to your environment configuration

## 📝 Usage Examples

### Python (Backend)
```python
# Direct function usage
import io
from backend_app.api.chat import speech_to_text

async def transcribe_example():
    with open("audio.wav", "rb") as f:
        text = await speech_to_text(f)
        print(f"Transcribed: {text}")
```

### cURL Commands
```bash
# Transcribe audio only
curl -X POST "http://localhost:8000/speech-to-text" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@recording.wav"

# Voice chat (transcribe + response)
curl -X POST "http://localhost:8000/voice-chat" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@recording.wav"
```

### JavaScript (Frontend)
```javascript
// Record and transcribe audio
async function recordAndTranscribe() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const mediaRecorder = new MediaRecorder(stream);
  const audioChunks = [];
  
  mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
  
  mediaRecorder.onstop = async () => {
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
    const formData = new FormData();
    formData.append('audio_file', audioBlob, 'recording.webm');
    
    const response = await fetch('/api/speech-to-text', {
      method: 'POST',
      body: formData
    });
    
    const result = await response.json();
    console.log('Transcription:', result.text);
  };
  
  mediaRecorder.start();
  // ... stop recording logic
}
```

## 🛡️ Error Handling

The function handles various error scenarios:

- **Authentication Error**: Invalid API key
- **Rate Limit Error**: API quota exceeded  
- **API Error**: OpenAI service issues
- **File Format Error**: Unsupported audio format
- **Network Error**: Connection issues

All errors are logged and return appropriate HTTP status codes.

## 🎵 Supported Audio Formats

- **WAV** (audio/wav)
- **MP3** (audio/mp3, audio/mpeg)  
- **MP4** (audio/mp4)
- **WEBM** (audio/webm)
- **OGG** (audio/ogg)
- **FLAC** (audio/flac)
- **M4A** (audio/m4a)

## 📊 Response Format

### `/speech-to-text` Response:
```json
{
  "text": "Transcribed text here",
  "filename": "recording.wav",
  "content_type": "audio/wav",
  "size_bytes": 12345
}
```

### `/voice-chat` Response:
```json
{
  "reply": "Assistant response based on transcribed audio"
}
```

## 🔒 Security Considerations

- API keys are managed through environment variables
- File uploads are validated for type and size
- Comprehensive error logging without exposing sensitive data
- Proper cleanup of temporary audio streams

## 🧪 Testing

Run the test file to verify functionality:
```bash
python tests/test_speech_to_text.py
```

## 🚀 Integration with Existing Features

The speech-to-text functionality integrates seamlessly with:
- **Memory System**: Voice interactions are stored in Weaviate
- **Web Search**: Voice queries trigger intelligent routing
- **LLM Processing**: Transcribed text flows through existing chat logic
- **Error Logging**: Voice interactions are logged for debugging

## 📈 Performance Notes

- Whisper API typically processes audio in 2-10 seconds
- Supports files up to 25MB
- Portuguese language optimization for better accuracy
- Async processing prevents blocking other requests

## 🔄 Future Enhancements

Potential improvements:
- Real-time streaming transcription
- Speaker identification
- Custom vocabulary/domain optimization
- Audio preprocessing for better quality
- Multiple language support selection
