/**
 * Tema Material-UI com tons terra para Ethic Companion
 * Paleta inspirada em elementos naturais e terrosos
 */

import { createTheme } from '@mui/material/styles';

// Paleta de cores terra
const earthyPalette = {
  primary: {
    main: '#8B4513', // Saddle Brown
    light: '#A0522D', // Sienna
    dark: '#654321', // Dark Brown
    contrastText: '#FFFFFF',
  },
  secondary: {
    main: '#D2691E', // Chocolate
    light: '#DEB887', // Burlywood
    dark: '#B8860B', // Dark Goldenrod
    contrastText: '#FFFFFF',
  },
  tertiary: {
    main: '#228B22', // Forest Green
    light: '#90EE90', // Light Green
    dark: '#006400', // Dark Green
  },
  background: {
    default: '#FAF7F2', // Warm White
    paper: '#FFFFFF',
    alt: '#F5F5DC', // Beige
  },
  surface: {
    main: '#DDBEA9', // Light Coffee
    dark: '#CB997E', // Desert Sand
    darker: '#B7B7A4', // Sage
  },
  text: {
    primary: '#3E2723', // Dark Brown
    secondary: '#5D4037', // Medium Brown
    disabled: '#8D6E63', // Light Brown
  },
  neutral: {
    50: '#FAFAFA',
    100: '#F5F5F5',
    200: '#EEEEEE',
    300: '#E0E0E0',
    400: '#BDBDBD',
    500: '#9E9E9E',
    600: '#757575',
    700: '#616161',
    800: '#424242',
    900: '#212121',
  },
  accent: {
    warm: '#FF8C69', // Salmon
    cool: '#20B2AA', // Light Sea Green
    earth: '#CD853F', // Peru
  }
};

// Tema customizado
export const earthyTheme = createTheme({
  palette: {
    mode: 'light',
    primary: earthyPalette.primary,
    secondary: earthyPalette.secondary,
    background: earthyPalette.background,
    text: earthyPalette.text,
    divider: earthyPalette.surface.main,
    grey: earthyPalette.neutral,
    success: {
      main: earthyPalette.tertiary.main,
      light: earthyPalette.tertiary.light,
      dark: earthyPalette.tertiary.dark,
    },
    warning: {
      main: earthyPalette.accent.earth,
    },
    info: {
      main: earthyPalette.accent.cool,
    },
    error: {
      main: '#D32F2F',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
      color: earthyPalette.text.primary,
    },
    h2: {
      fontWeight: 600,
      fontSize: '2rem',
      color: earthyPalette.text.primary,
    },
    h3: {
      fontWeight: 600,
      fontSize: '1.5rem',
      color: earthyPalette.text.primary,
    },
    h4: {
      fontWeight: 500,
      fontSize: '1.25rem',
      color: earthyPalette.text.primary,
    },
    h5: {
      fontWeight: 500,
      fontSize: '1.1rem',
      color: earthyPalette.text.primary,
    },
    h6: {
      fontWeight: 500,
      fontSize: '1rem',
      color: earthyPalette.text.secondary,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
      color: earthyPalette.text.primary,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.5,
      color: earthyPalette.text.secondary,
    },
    button: {
      textTransform: 'none',
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 12,
  },
  spacing: 8,
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 4px 20px rgba(139, 69, 19, 0.1)',
          borderRadius: 16,
          border: `1px solid ${earthyPalette.surface.main}`,
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 24,
          padding: '10px 24px',
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0 4px 12px rgba(139, 69, 19, 0.2)',
          },
        },
        contained: {
          background: `linear-gradient(135deg, ${earthyPalette.primary.main} 0%, ${earthyPalette.primary.dark} 100%)`,
          '&:hover': {
            background: `linear-gradient(135deg, ${earthyPalette.primary.dark} 0%, ${earthyPalette.primary.main} 100%)`,
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 12,
            backgroundColor: earthyPalette.background.paper,
            '&:hover .MuiOutlinedInput-notchedOutline': {
              borderColor: earthyPalette.primary.light,
            },
            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
              borderColor: earthyPalette.primary.main,
              borderWidth: 2,
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          fontWeight: 500,
        },
        colorPrimary: {
          backgroundColor: earthyPalette.surface.main,
          color: earthyPalette.text.primary,
          '&:hover': {
            backgroundColor: earthyPalette.surface.dark,
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
        elevation1: {
          boxShadow: '0 2px 8px rgba(139, 69, 19, 0.08)',
        },
        elevation2: {
          boxShadow: '0 4px 16px rgba(139, 69, 19, 0.12)',
        },
        elevation3: {
          boxShadow: '0 8px 24px rgba(139, 69, 19, 0.16)',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: `linear-gradient(135deg, ${earthyPalette.background.paper} 0%, ${earthyPalette.background.alt} 100%)`,
          color: earthyPalette.text.primary,
          boxShadow: '0 2px 12px rgba(139, 69, 19, 0.1)',
        },
      },
    },
    MuiAvatar: {
      styleOverrides: {
        root: {
          backgroundColor: earthyPalette.primary.main,
          color: earthyPalette.primary.contrastText,
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          '&:hover': {
            backgroundColor: `${earthyPalette.surface.main}40`,
          },
        },
      },
    },
  },
});

// Exportar paleta para uso direto se necessário
export { earthyPalette };
