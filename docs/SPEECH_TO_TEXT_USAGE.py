"""
Example of how to integrate speech-to-text with your frontend
This shows the curl commands and JavaScript fetch examples
"""

# Example 1: Direct speech-to-text endpoint
curl_example_1 = """
# Upload audio file for transcription only
curl -X POST "http://localhost:8000/speech-to-text" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@path/to/your/audio.wav"

# Response:
{
  "text": "Transcrição do áudio aqui",
  "filename": "audio.wav",
  "content_type": "audio/wav",
  "size_bytes": 12345
}
"""

# Example 2: Voice chat endpoint (transcribe + chat response)
curl_example_2 = """
# Upload audio file and get chat response
curl -X POST "http://localhost:8000/voice-chat" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@path/to/your/audio.wav"

# Response:
{
  "reply": "Resposta do assistente baseada no áudio transcrito"
}
"""

# JavaScript frontend integration example
js_example = """
// JavaScript example for frontend integration

// Function to record audio and send to speech-to-text
async function transcribeAudio(audioBlob) {
  const formData = new FormData();
  formData.append('audio_file', audioBlob, 'recording.webm');
  
  try {
    const response = await fetch('/api/speech-to-text', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result.text;
  } catch (error) {
    console.error('Error transcribing audio:', error);
    throw error;
  }
}

// Function for voice chat (transcribe + get response)
async function voiceChat(audioBlob) {
  const formData = new FormData();
  formData.append('audio_file', audioBlob, 'recording.webm');
  
  try {
    const response = await fetch('/api/voice-chat', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result.reply;
  } catch (error) {
    console.error('Error in voice chat:', error);
    throw error;
  }
}

// Example usage with Web Audio API
let mediaRecorder;
let audioChunks = [];

// Start recording
async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    
    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };
    
    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
      audioChunks = [];
      
      // Option 1: Just transcribe
      const transcription = await transcribeAudio(audioBlob);
      console.log('Transcription:', transcription);
      
      // Option 2: Voice chat (transcribe + response)
      // const response = await voiceChat(audioBlob);
      // console.log('Chat response:', response);
    };
    
    mediaRecorder.start();
    console.log('Recording started');
  } catch (error) {
    console.error('Error starting recording:', error);
  }
}

// Stop recording
function stopRecording() {
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop();
    console.log('Recording stopped');
  }
}
"""

if __name__ == "__main__":
    print("📚 Exemplos de integração Speech-to-Text")
    print("\n" + "="*50)
    print("CURL - Transcrição simples:")
    print(curl_example_1)
    print("\n" + "="*50)
    print("CURL - Voice Chat:")
    print(curl_example_2)
    print("\n" + "="*50)
    print("JavaScript - Integração Frontend:")
    print(js_example)
