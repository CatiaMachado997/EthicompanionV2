'use client';

import { useState, useEffect, useRef, FormEvent } from 'react';
import { useAudioRecorder } from '../hooks/useAudioRecorder';

type Message = {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
};

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isClient, setIsClient] = useState(false);
  const [activeChat, setActiveChat] = useState('current');
  const [selectedModel, setSelectedModel] = useState('gpt5');
  const [isChatMode, setIsChatMode] = useState(false);
  const [isSpeechActive, setIsSpeechActive] = useState(false);
  const [isTemporaryChat, setIsTemporaryChat] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Audio recording hook
  const {
    isRecording,
    audioBlob,
    startRecording,
    stopRecording,
    error: recordingError,
    isSupported: isAudioSupported
  } = useAudioRecorder();

  useEffect(() => { setIsClient(true); }, []);
  useEffect(() => { scrollToBottom(); }, [messages]);

  // Display recording errors
  useEffect(() => {
    if (recordingError) {
      console.error('Recording error:', recordingError);
      // You could show a toast notification here
    }
  }, [recordingError]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setIsChatMode(true); // Activate chat mode when first message is sent

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: inputValue, // Changed from message to text
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: data.response,
          sender: 'assistant',
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        throw new Error('Failed to get response');
      }
    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Desculpe, ocorreu um erro. Tente novamente.',
        sender: 'assistant',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setActiveChat('current');
    setIsChatMode(false);
  };

  // Handle speech-to-text transcription
  const transcribeAudio = async (audioBlob: Blob): Promise<string> => {
    const formData = new FormData();
    formData.append('audio_file', audioBlob, 'recording.webm');

    try {
      const response = await fetch('/api/speech-to-text', {
        method: 'POST',
        body: formData,
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
  };

  // Handle voice chat (transcribe + get response)
  const handleVoiceChat = async (audioBlob: Blob) => {
    const formData = new FormData();
    formData.append('audio_file', audioBlob, 'recording.webm');

    try {
      const response = await fetch('/api/voice-chat', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result.response;
    } catch (error) {
      console.error('Error in voice chat:', error);
      throw error;
    }
  };

  // Handle speech button toggle
  const toggleSpeech = async () => {
    if (!isAudioSupported) {
      alert('Audio recording is not supported in your browser');
      return;
    }

    if (isRecording) {
      // Stop recording and process
      stopRecording();
    } else {
      // Start recording
      try {
        await startRecording();
        setIsSpeechActive(true);
      } catch (error) {
        console.error('Error starting recording:', error);
        alert('Could not start recording. Please check microphone permissions.');
      }
    }
  };

  // Process audio when recording stops
  useEffect(() => {
    if (audioBlob && !isRecording && isSpeechActive) {
      const processAudio = async () => {
        setIsTranscribing(true);
        setIsSpeechActive(false);

        try {
          // Option 1: Just transcribe to text input
          const transcribedText = await transcribeAudio(audioBlob);
          setInputValue(transcribedText);

          // Option 2: Direct voice chat (uncomment to use)
          // const response = await handleVoiceChat(audioBlob);
          // const userMessage: Message = {
          //   id: Date.now().toString(),
          //   text: transcribedText,
          //   sender: 'user',
          //   timestamp: new Date(),
          // };
          // const assistantMessage: Message = {
          //   id: (Date.now() + 1).toString(),
          //   text: response,
          //   sender: 'assistant',
          //   timestamp: new Date(),
          // };
          // setMessages(prev => [...prev, userMessage, assistantMessage]);
          // setIsChatMode(true);

        } catch (error) {
          console.error('Error processing audio:', error);
          const errorMessage: Message = {
            id: Date.now().toString(),
            text: 'Desculpe, ocorreu um erro ao processar o áudio. Tente novamente.',
            sender: 'assistant',
            timestamp: new Date(),
          };
          setMessages(prev => [...prev, errorMessage]);
        } finally {
          setIsTranscribing(false);
        }
      };

      processAudio();
    }
  }, [audioBlob, isRecording, isSpeechActive]);

  if (!isClient) {
    return (
      <div className="main-layout">
        <div className="loading-indicator">
          <div className="loading-bubble">
            <div className="typing-dots">
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`main-layout ${isChatMode ? 'chat-mode' : ''}`}>
      {/* Sidebar */}
      <div className="sidebar">
        <div className="user-settings">
          <div className="user-info">
            <div className="user-avatar">CM</div>
            <div className="user-details">
              <div className="user-name">Catia Machado</div>
              <div className="user-status">Premium</div>
            </div>
          </div>
          <button className="settings-btn">⚙️</button>
        </div>

        <button className="new-chat-btn" onClick={handleNewChat}>
          <span className="new-chat-icon">✏️</span>
          <span className="new-chat-text">Nova Conversa</span>
        </button>

        <div className="chat-history">
          <div className="section-title">Conversas Recentes</div>
          <div className="chat-item">
            <span className="chat-icon">💬</span>
            <span className="chat-text">Alinhar face e ombros</span>
          </div>
          <div className="chat-item">
            <span className="chat-icon">💬</span>
            <span className="chat-text">L5 vs SE III</span>
          </div>
          <div className="chat-item">
            <span className="chat-icon">💬</span>
            <span className="chat-text">Esquema de tricô explicado</span>
          </div>
        </div>

        <div className="my-gpts">
          <div className="section-title">Meus GPTs</div>
          <div className="chat-item">
            <span className="chat-icon ethic-companion">🤖</span>
            <span className="chat-text">Ethic Companion</span>
          </div>
          <div className="chat-item">
            <span className="chat-icon personal-assistant">👤</span>
            <span className="chat-text">Assistente Pessoal</span>
          </div>
          <div className="chat-item">
            <span className="chat-icon study-helper">📚</span>
            <span className="chat-text">Ajudante de Estudo</span>
          </div>
        </div>

        <div className="other-functionalities">
          <div className="section-title">Outras Funcionalidades</div>
          <div className="chat-item">
            <span className="functionality-icon">🔍</span>
            <span className="functionality-text">Pesquisa na Web</span>
          </div>
          <div className="chat-item">
            <span className="functionality-icon">📊</span>
            <span className="functionality-text">Análise de Dados</span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <div className="top-bar">
          <button className="bg-gradient-to-r from-coral to-pink text-white px-4 py-2 rounded-2xl font-medium hover:shadow-lg transition-all duration-300 border border-white/20">
            ✨ Upgrade
          </button>
        </div>

        {!isChatMode && messages.length === 0 ? (
          <div className="welcome-screen">
            <div className="welcome-content">
              <h1 className="welcome-greeting">Hello, Catia</h1>
              <p className="welcome-question">
                How can I help you today? How are you feeling and doing?
              </p>
              
              {/* Mandala Symbol */}
              <div className="mandala-symbol"></div>
              
              {/* Input Section - Centralizado e Prominente */}
              <div className="input-section">
                <form onSubmit={handleSubmit} className="input-container">
                  <textarea
                    ref={textareaRef}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Mensagem para Ethic Companion..."
                    className="input-textarea"
                    rows={1}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSubmit(e);
                      }
                    }}
                  />
                  <div className="input-actions">
                    <button
                      type="button"
                      onClick={toggleSpeech}
                      disabled={isTranscribing || !isAudioSupported}
                      className={`speech-btn ${isRecording ? 'recording' : isSpeechActive ? 'active' : ''} ${!isAudioSupported ? 'disabled' : ''}`}
                      title={
                        !isAudioSupported 
                          ? 'Audio recording not supported' 
                          : isRecording 
                            ? 'Click to stop recording' 
                            : isTranscribing 
                              ? 'Transcribing audio...' 
                              : 'Click to start voice input'
                      }
                    >
                      {isTranscribing ? '⏳' : isRecording ? '⏹️' : '🎤'}
                    </button>
                    <button
                      type="submit"
                      disabled={isLoading || !inputValue.trim()}
                      className="submit-btn"
                    >
                      ➤
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        ) : (
          <>
            <div className="messages-area">
              {messages.map((message) => (
                <div key={message.id} className={`message ${message.sender}`}>
                  <div className="message-container">
                    <div className="message-bubble">
                      <div className="message-text">{message.text}</div>
                      <div className="message-meta">
                        <span className="message-time">
                          {message.timestamp.toLocaleTimeString()}
                        </span>
                        <div className="message-actions">
                          <button className="action-btn">📋</button>
                          <button className="action-btn">🔄</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="loading-indicator">
                  <div className="loading-bubble">
                    <div className="typing-dots">
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <div className="input-area">
              <form onSubmit={handleSubmit} className="input-section">
                <div className="input-container">
                  <textarea
                    ref={textareaRef}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Mensagem para Ethic Companion..."
                    className="input-textarea"
                    rows={1}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSubmit(e);
                      }
                    }}
                  />
                  <div className="input-actions">
                    <button
                      type="button"
                      onClick={toggleSpeech}
                      disabled={isTranscribing || !isAudioSupported}
                      className={`speech-btn ${isRecording ? 'recording' : isSpeechActive ? 'active' : ''} ${!isAudioSupported ? 'disabled' : ''}`}
                      title={
                        !isAudioSupported 
                          ? 'Audio recording not supported' 
                          : isRecording 
                            ? 'Click to stop recording' 
                            : isTranscribing 
                              ? 'Transcribing audio...' 
                              : 'Click to start voice input'
                      }
                    >
                      {isTranscribing ? '⏳' : isRecording ? '⏹️' : '🎤'}
                    </button>
                    <button
                      type="submit"
                      disabled={isLoading || !inputValue.trim()}
                      className="submit-btn"
                    >
                      ➤
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </>
        )}

        <div className="bottom-bar">
          <div className="model-selector">
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="model-dropdown"
            >
              <option value="gpt5">GPT-5</option>
              <option value="gpt4">GPT-4</option>
              <option value="gpt3">GPT-3.5</option>
            </select>
          </div>
          <div className="temporary-chat">
            <span className="text-xs mr-2">Chat Temporário</span>
            <button
              onClick={() => setIsTemporaryChat(!isTemporaryChat)}
              className={`temp-chat-toggle ${isTemporaryChat ? 'active' : ''}`}
            ></button>
          </div>
        </div>
      </div>
    </div>
  );
}
