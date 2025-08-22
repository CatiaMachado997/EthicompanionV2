/**
 * Componentes Material-UI customizados para Ethic Companion
 * Mantém a funcionalidade existente com novo design terra
 */

import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Paper,
  Card,
  CardContent,
  Box,
  Fab,
  Avatar,
  Chip,
  CircularProgress,
  styled,
  useTheme,
} from '@mui/material';
import {
  Psychology as PsychologyIcon,
  Send as SendIcon,
  VolumeUp as VolumeUpIcon,
  Memory as MemoryIcon,
} from '@mui/icons-material';

// Header customizado
export const EthicHeader = () => {
  const theme = useTheme();
  
  return (
    <AppBar position="static" elevation={0}>
      <Toolbar>
        <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
          <PsychologyIcon />
        </Avatar>
        <Typography variant="h5" component="h1" sx={{ flexGrow: 1, fontWeight: 600 }}>
          Ethic Companion
        </Typography>
        <Chip 
          icon={<MemoryIcon />}
          label="Memória Híbrida Ativa"
          color="primary"
          variant="outlined"
          size="small"
        />
      </Toolbar>
    </AppBar>
  );
};

// Container principal
export const MainContainer = styled(Container)(({ theme }) => ({
  minHeight: '100vh',
  backgroundColor: theme.palette.background.default,
  paddingTop: theme.spacing(3),
  paddingBottom: theme.spacing(3),
}));

// Card de chat customizado
interface ChatCardProps {
  children: React.ReactNode;
  elevation?: number;
}

export const ChatCard = ({ children, elevation = 2 }: ChatCardProps) => {
  return (
    <Card 
      elevation={elevation}
      sx={{ 
        height: '70vh',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        background: 'linear-gradient(145deg, #FFFFFF 0%, #FAF7F2 100%)',
      }}
    >
      <CardContent sx={{ p: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
        {children}
      </CardContent>
    </Card>
  );
};

// Área de mensagens
export const MessagesContainer = styled(Box)(({ theme }) => ({
  flexGrow: 1,
  overflowY: 'auto',
  padding: theme.spacing(2),
  display: 'flex',
  flexDirection: 'column',
  gap: theme.spacing(1.5),
  '&::-webkit-scrollbar': {
    width: '6px',
  },
  '&::-webkit-scrollbar-track': {
    backgroundColor: theme.palette.background.alt,
    borderRadius: '3px',
  },
  '&::-webkit-scrollbar-thumb': {
    backgroundColor: theme.palette.primary.main,
    borderRadius: '3px',
    '&:hover': {
      backgroundColor: theme.palette.primary.dark,
    },
  },
}));

// Mensagem do usuário
interface UserMessageProps {
  message: string;
  timestamp?: string;
}

export const UserMessage = ({ message, timestamp }: UserMessageProps) => {
  const theme = useTheme();
  
  return (
    <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 1 }}>
      <Paper
        elevation={1}
        sx={{
          maxWidth: '70%',
          p: 2,
          borderRadius: '18px 18px 6px 18px',
          background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
          color: theme.palette.primary.contrastText,
        }}
      >
        <Typography variant="body1">{message}</Typography>
        {timestamp && (
          <Typography variant="caption" sx={{ opacity: 0.8, display: 'block', mt: 0.5 }}>
            {timestamp}
          </Typography>
        )}
      </Paper>
    </Box>
  );
};

// Mensagem do assistente
interface AssistantMessageProps {
  message: string;
  timestamp?: string;
  isStreaming?: boolean;
}

export const AssistantMessage = ({ message, timestamp, isStreaming }: AssistantMessageProps) => {
  const theme = useTheme();
  
  return (
    <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 1 }}>
      <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1, maxWidth: '70%' }}>
        <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
          <PsychologyIcon fontSize="small" />
        </Avatar>
        <Paper
          elevation={1}
          sx={{
            p: 2,
            borderRadius: '18px 18px 18px 6px',
            backgroundColor: theme.palette.background.paper,
            border: `1px solid ${theme.palette.divider}`,
          }}
        >
          <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
            {message}
            {isStreaming && (
              <Box component="span" sx={{ 
                display: 'inline-block',
                width: '2px',
                height: '1.2em',
                backgroundColor: 'primary.main',
                ml: 0.5,
                animation: 'blink 1s infinite',
                '@keyframes blink': {
                  '0%, 50%': { opacity: 1 },
                  '51%, 100%': { opacity: 0 },
                },
              }} />
            )}
          </Typography>
          {timestamp && (
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 0.5 }}>
              {timestamp}
            </Typography>
          )}
        </Paper>
      </Box>
    </Box>
  );
};

// Indicador de pensamento
export const ThinkingIndicator = () => {
  const theme = useTheme();
  
  return (
    <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 1 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
          <PsychologyIcon fontSize="small" />
        </Avatar>
        <Paper
          elevation={1}
          sx={{
            p: 2,
            borderRadius: '18px 18px 18px 6px',
            backgroundColor: theme.palette.background.paper,
            border: `1px solid ${theme.palette.divider}`,
            display: 'flex',
            alignItems: 'center',
            gap: 1,
          }}
        >
          <CircularProgress size={16} thickness={4} />
          <Typography variant="body2" color="text.secondary">
            Pensando...
          </Typography>
        </Paper>
      </Box>
    </Box>
  );
};

// Área de input customizada
export const InputArea = styled(Box)(({ theme }) => ({
  padding: theme.spacing(2),
  borderTop: `1px solid ${theme.palette.divider}`,
  backgroundColor: theme.palette.background.alt,
}));

// Botão de envio customizado
interface SendButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

export const SendButton = ({ onClick, disabled }: SendButtonProps) => {
  return (
    <Fab
      color="primary"
      aria-label="enviar mensagem"
      onClick={onClick}
      disabled={disabled}
      size="medium"
      sx={{
        ml: 1,
        boxShadow: '0 4px 12px rgba(139, 69, 19, 0.3)',
        '&:hover': {
          boxShadow: '0 6px 16px rgba(139, 69, 19, 0.4)',
        },
      }}
    >
      <SendIcon />
    </Fab>
  );
};

// Botão de áudio
interface AudioButtonProps {
  onClick: () => void;
  isRecording?: boolean;
}

export const AudioButton = ({ onClick, isRecording }: AudioButtonProps) => {
  return (
    <Fab
      color="secondary"
      aria-label="comando de voz"
      onClick={onClick}
      size="small"
      sx={{
        mr: 1,
        opacity: isRecording ? 0.7 : 1,
        animation: isRecording ? 'pulse 1.5s infinite' : 'none',
        '@keyframes pulse': {
          '0%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.1)' },
          '100%': { transform: 'scale(1)' },
        },
      }}
    >
      <VolumeUpIcon fontSize="small" />
    </Fab>
  );
};

// Status de conexão
interface ConnectionStatusProps {
  isConnected: boolean;
}

export const ConnectionStatus = ({ isConnected }: ConnectionStatusProps) => {
  return (
    <Chip
      label={isConnected ? "Conectado" : "Desconectado"}
      color={isConnected ? "success" : "error"}
      size="small"
      sx={{ 
        position: 'fixed',
        bottom: 16,
        right: 16,
        zIndex: 1000,
      }}
    />
  );
};
