"use client";

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";

// ✅ 직접 타입을 정의하여 next-themes에 의존하지 않도록 처리
type Attribute = "class" | "style" | (string & {}); // 공식 타입 참고

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