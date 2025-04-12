"use client";

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";

// 타입 충돌 방지를 위해 any 사용
export function ThemeProvider({ children, ...props }: any) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}