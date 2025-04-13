"use client";

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";

// ✅ 허용되는 attribute 값만 명시적으로 타입 지정
type AttributeType = "class" | "data-theme";

interface CustomThemeProviderProps {
  children: React.ReactNode;
  attribute?: AttributeType;
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