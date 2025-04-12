"use client";

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";

// 🔧 직접 타입 선언하여 next-themes 타입 의존성 제거
interface ThemeProviderProps {
  children: React.ReactNode;
  attribute?: string;
  defaultTheme?: string;
  enableSystem?: boolean;
  disableTransitionOnChange?: boolean;
}

export function ThemeProvider({
  children,
  ...props
}: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}