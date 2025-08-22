/**
 * Provider de tema Material-UI com tons terra
 */

import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { earthyTheme } from './earthyTheme';

interface EarthyThemeProviderProps {
  children: React.ReactNode;
}

export function EarthyThemeProvider({ children }: EarthyThemeProviderProps) {
  return (
    <ThemeProvider theme={earthyTheme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}
