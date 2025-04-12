"use client";

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";

// ✅ next-themes 내부 정의에 맞춘 정확한 타입 지정
type ThemeProviderProps = {
  children: React.ReactNode;
  attribute?: "class";
  defaultTheme?: string;
  enableSystem?: boolean;
  disableTransitionOnChange?: boolean;
};

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}