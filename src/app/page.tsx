'use client';

import { useState, useEffect, useRef, FormEvent } from 'react';
import { useAudioRecorder } from '../hooks/useAudioRecorder';
import { useHybridMemoryChat } from '../hooks/useHybridMemoryChat';
import { MemoryStatsPanel, MemoryStatusBadge } from '../components/MemoryStatsPanel';
import { ContextModeSelector, ContextModeBadge } from '../components/ContextModeSelector';
import { MessageList, TypingIndicator } from '../components/EnhancedMessage';

// Função para gerar UUID simples (substitui dependência uuid)
function generateSessionId(): string {
  return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

export default function ChatPage() {
  // Estados do chat híbrido
  const {
    messages,
    isLoading,
    error,
    sessionId,
    memoryStats,
    contextInfo,
    sendMessage,
    clearMessages,
    refreshMemoryStats,
    startNewSession,
    setContextMode,
    contextMode
  } = useHybridMemoryChat({
    sessionId: generateSessionId(),
    contextMode: 'hybrid',
    apiBaseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  });

  // Estados da UI
  const [inputValue, setInputValue] = useState('');
  const [isClient, setIsClient] = useState(false);
  const [activeChat, setActiveChat] = useState('current');
  const [selectedModel, setSelectedModel] = useState('hybrid-memory');
  const [isChatMode, setIsChatMode] = useState(false);
  const [isSpeechActive, setIsSpeechActive] = useState(false);
  const [isTemporaryChat, setIsTemporaryChat] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [showMemoryPanel, setShowMemoryPanel] = useState(false);
  const [showContextDetails, setShowContextDetails] = useState(false);
  
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

  // Função de envio usando o hook de memória híbrida
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const messageText = inputValue;
    setInputValue('');
    setIsChatMode(true); // Activate chat mode when first message is sent

    try {
      await sendMessage(messageText);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleNewChat = () => {
    startNewSession();
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
          // Transcribe audio to text input
          const transcribedText = await transcribeAudio(audioBlob);
          setInputValue(transcribedText);

        } catch (error) {
          console.error('Error processing audio:', error);
          // Handle error through the hook's error system
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
          <div className="flex items-center gap-4">
            {/* Memory Status Badge */}
            <MemoryStatusBadge 
              memoryStats={memoryStats}
              contextInfo={contextInfo}
            />
            
            {/* Context Mode Badge */}
            <ContextModeBadge 
              mode={contextMode || 'hybrid'}
              onClick={() => setShowMemoryPanel(!showMemoryPanel)}
            />
            
            {/* Session ID (for debugging) */}
            <span className="text-xs text-gray-500">
              Sessão: {sessionId.slice(-8)}
            </span>
          </div>

          <div className="flex items-center gap-2">
            {/* Memory Panel Toggle */}
            <button
              onClick={() => setShowMemoryPanel(!showMemoryPanel)}
              className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded"
              title="Mostrar/ocultar painel de memória"
            >
              🧠
            </button>
            
            {/* Context Details Toggle */}
            <button
              onClick={() => setShowContextDetails(!showContextDetails)}
              className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded"
              title="Mostrar/ocultar detalhes de contexto"
            >
              📊
            </button>

            <button className="bg-gradient-to-r from-coral to-pink text-white px-4 py-2 rounded-2xl font-medium hover:shadow-lg transition-all duration-300 border border-white/20">
              ✨ Upgrade
            </button>
          </div>
        </div>

        {/* Memory Panel (when expanded) */}
        {showMemoryPanel && (
          <div className="mb-4">
            <MemoryStatsPanel
              memoryStats={memoryStats}
              contextInfo={contextInfo}
              onRefresh={refreshMemoryStats}
              className="mb-4"
            />
            <ContextModeSelector
              currentMode={contextMode || 'hybrid'}
              onChange={setContextMode}
              disabled={isLoading}
            />
          </div>
        )}

        {!isChatMode && messages.length === 0 ? (
          <div className="welcome-screen">
            <div className="welcome-content">
              <h1 className="welcome-greeting">Olá, Catia</h1>
              <p className="welcome-question">
                Como posso ajudar-te hoje com questões éticas ou reflexões pessoais?
              </p>
              
              {/* Mandala Symbol */}
              <div className="mandala-symbol"></div>
              
              {/* Context Mode Selector (prominent) */}
              <div className="mb-6">
                <ContextModeSelector
                  currentMode={contextMode || 'hybrid'}
                  onChange={setContextMode}
                  disabled={isLoading}
                />
              </div>
              
              {/* Input Section - Centralizado e Prominente */}
              <div className="input-section">
                <form onSubmit={handleSubmit} className="input-container">
                  <textarea
                    ref={textareaRef}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Partilha um dilema ético ou uma reflexão pessoal..."
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
              {/* Error Display */}
              {error && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                  ❌ {error}
                </div>
              )}

              {/* Messages with enhanced context display */}
              <MessageList
                messages={messages}
                lastContextInfo={contextInfo}
                showContextDetails={showContextDetails}
              />

              {/* Typing Indicator */}
              {isLoading && (
                <TypingIndicator contextMode={contextMode} />
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
                    placeholder="Continua a conversa..."
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
              <option value="hybrid-memory">🧠 Memória Híbrida</option>
              <option value="gpt4">GPT-4 Simples</option>
              <option value="gemini">Gemini Pro</option>
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
