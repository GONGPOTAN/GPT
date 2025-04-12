"use client";

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";

// ✅ 정확한 Attribute 타입 정의
type Attribute = "class" | "style";

interface CustomThemeProviderProps {
  children: React.ReactNode;
  attribute?: Attribute;
  defaultTheme?: string;
  enableSystem?: boolean;
  disableTransitionOnChange?: boolean;
}

export function ThemeProvider({
  children,
  ...props
}: CustomThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}