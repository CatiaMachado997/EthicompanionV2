'use client';

import { useState, useEffect, useRef, FormEvent } from 'react';
import { useAudioRecorder } from '../hooks/useAudioRecorder';
import { useHybridMemoryChat, Message } from '../hooks/useHybridMemoryChat';
import { MemoryStatsPanel, MemoryStatusBadge } from '../components/MemoryStatsPanel';
import { ContextModeSelector, ContextModeBadge } from '../components/ContextModeSelector';

// Importações Material-UI
import { 
  Box, 
  TextField, 
  Switch, 
  FormControlLabel, 
  Grid, 
  Paper,
  Typography,
  Divider,
  Stack,
} from '@mui/material';
import { EarthyThemeProvider } from '../theme/earthyTheme';
import {
  EthicHeader,
  MainContainer,
  ChatCard,
  MessagesContainer,
  UserMessage,
  AssistantMessage,
  ThinkingIndicator as MaterialThinkingIndicator,
  InputArea,
  SendButton,
  AudioButton,
  ConnectionStatus,
} from '../components/MaterialUIComponents';

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
    sendMessageWithStreaming,  // Nova função de streaming
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
  const [useStreaming, setUseStreaming] = useState(true);  // Nova opção para streaming
  
  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Audio recording with error handling
  const {
    isRecording,
    audioBlob,
    startRecording,
    stopRecording,
    isSupported: isAudioSupported,
    error: recordingError
  } = useAudioRecorder();

  useEffect(() => {
    setIsClient(true);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (recordingError) {
      console.error('Recording error:', recordingError);
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
      // Usar streaming ou método tradicional baseado na preferência
      if (useStreaming) {
        await sendMessageWithStreaming(messageText);
      } else {
        await sendMessage(messageText);
      }
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
      console.error('Transcription error:', error);
      throw error;
    }
  };

  const toggleSpeech = () => {
    if (!isAudioSupported) {
      console.warn('Audio recording not supported in this browser');
      return;
    }

    if (isRecording) {
      stopRecording();
      setIsSpeechActive(false);
    } else {
      startRecording();
      setIsSpeechActive(true);
    }
  };

  // Audio blob processing
  useEffect(() => {
    if (audioBlob && !isRecording) {
      const processAudio = async () => {
        try {
          setIsTranscribing(true);
          const transcription = await transcribeAudio(audioBlob);
          if (transcription.trim()) {
            setInputValue(prev => prev + transcription);
          }
        } catch (error) {
          console.error('Error processing audio:', error);
        } finally {
          setIsTranscribing(false);
          setIsSpeechActive(false);
        }
      };

      processAudio();
    }
  }, [audioBlob, isRecording, isSpeechActive]);

  // Renderizar mensagens com componentes Material-UI
  const renderMessages = () => {
    return messages.map((msg: Message, index: number) => {
      const timestamp = new Date(msg.timestamp || Date.now()).toLocaleTimeString('pt-PT', {
        hour: '2-digit',
        minute: '2-digit'
      });

      if (msg.sender === 'user') {
        return (
          <UserMessage 
            key={index}
            message={msg.text}
            timestamp={timestamp}
          />
        );
      } else {
        return (
          <AssistantMessage
            key={index}
            message={msg.text}
            timestamp={timestamp}
            isStreaming={msg.isStreaming}
          />
        );
      }
    });
  };

  if (!isClient) {
    return null; // Avoid hydration mismatch
  }

  return (
    <EarthyThemeProvider>
      <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
        {/* Header */}
        <EthicHeader />

        {/* Container Principal */}
        <MainContainer maxWidth="lg">
          <Box sx={{ display: 'flex', gap: 3, flexDirection: { xs: 'column', md: 'row' } }}>
            {/* Painel Lateral de Memória */}
            <Box sx={{ flex: '0 0 300px', width: { xs: '100%', md: '300px' } }}>
              <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Memória do Sistema
                </Typography>
                <MemoryStatusBadge 
                  memoryStats={memoryStats}
                  contextInfo={contextInfo}
                />
                <Divider sx={{ my: 2 }} />
                <ContextModeSelector
                  currentMode={contextMode || 'hybrid'}
                  onChange={setContextMode}
                />
              </Paper>

              {/* Configurações de Chat */}
              <Paper elevation={2} sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Configurações
                </Typography>
                <Stack spacing={2}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={useStreaming}
                        onChange={(e) => setUseStreaming(e.target.checked)}
                        color="primary"
                      />
                    }
                    label="Respostas em Tempo Real"
                  />
                  <FormControlLabel
                    control={
                      <Switch
                        checked={isTemporaryChat}
                        onChange={(e) => setIsTemporaryChat(e.target.checked)}
                        color="secondary"
                      />
                    }
                    label="Chat Temporário"
                  />
                </Stack>
              </Paper>
            </Box>

            {/* Área Principal de Chat */}
            <Box sx={{ flex: 1 }}>
              <ChatCard elevation={3}>
                {/* Área de Mensagens */}
                <MessagesContainer>
                  {messages.length === 0 ? (
                    <Box sx={{ 
                      display: 'flex', 
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      height: '100%',
                      textAlign: 'center',
                      color: 'text.secondary'
                    }}>
                      <Typography variant="h4" gutterBottom>
                        🤖 Ethic Companion
                      </Typography>
                      <Typography variant="body1" sx={{ maxWidth: 400 }}>
                        Partilha um dilema ético ou uma reflexão pessoal. 
                        Estou aqui para te ajudar a pensar através de questões morais complexas.
                      </Typography>
                    </Box>
                  ) : (
                    <>
                      {renderMessages()}
                      {isLoading && !useStreaming && <MaterialThinkingIndicator />}
                      <div ref={messagesEndRef} />
                    </>
                  )}
                </MessagesContainer>

                {/* Área de Input */}
                <InputArea>
                  <form onSubmit={handleSubmit}>
                    <Box sx={{ display: 'flex', alignItems: 'flex-end', gap: 1 }}>
                      {/* Botão de Áudio */}
                      <AudioButton
                        onClick={toggleSpeech}
                        isRecording={isRecording}
                      />

                      {/* Campo de Texto */}
                      <TextField
                        fullWidth
                        multiline
                        maxRows={4}
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        placeholder="Partilha um dilema ético ou uma reflexão pessoal..."
                        variant="outlined"
                        size="medium"
                        disabled={isLoading}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            handleSubmit(e);
                          }
                        }}
                        sx={{ 
                          '& .MuiOutlinedInput-root': {
                            bgcolor: 'background.paper',
                          }
                        }}
                      />

                      {/* Botão de Envio */}
                      <SendButton
                        onClick={() => handleSubmit({ preventDefault: () => {} } as FormEvent)}
                        disabled={isLoading || !inputValue.trim()}
                      />
                    </Box>
                  </form>
                </InputArea>
              </ChatCard>
            </Box>
          </Box>
        </MainContainer>

        {/* Status de Conexão */}
        <ConnectionStatus isConnected={!error} />
      </Box>
    </EarthyThemeProvider>
  );
}
