// dashboard-ui/src/app/Page.tsx
"use client";

import React, { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import {
  Table,
  TableHeader,
  TableRow,
  TableCell,
  TableBody,
} from "@/components/ui/table";

interface StatusData {
  [key: string]: {
    price: number;
    rsi: Record<string, number>;
    trend: Record<string, string>;
    updated_at: string;
  };
}

export default function Page() {
  const [data, setData] = useState<StatusData>({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/status");
        const json = await res.json();
        setData(json);
      } catch (error) {
        console.error("데이터 가져오기 실패:", error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000); // 5초마다 새로고침
    return () => clearInterval(interval);
  }, []);

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4">📊 실시간 시세 대시보드</h1>
      <Card>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableCell>종목</TableCell>
                <TableCell>가격</TableCell>
                <TableCell>RSI (H1)</TableCell>
                <TableCell>RSI (H4)</TableCell>
                <TableCell>RSI (D)</TableCell>
                <TableCell>추세 (H1)</TableCell>
                <TableCell>추세 (H4)</TableCell>
                <TableCell>추세 (D)</TableCell>
                <TableCell>업데이트 시각</TableCell>
              </TableRow>
            </TableHeader>
            <TableBody>
              {Object.entries(data).map(([symbol, status]) => (
                <TableRow key={symbol}>
                  <TableCell>{symbol}</TableCell>
                  <TableCell>{status.price?.toFixed(2) ?? "-"}</TableCell>
                  <TableCell>{status.rsi?.["H1"]?.toFixed(2) ?? "-"}</TableCell>
                  <TableCell>{status.rsi?.["H4"]?.toFixed(2) ?? "-"}</TableCell>
                  <TableCell>{status.rsi?.["D"]?.toFixed(2) ?? "-"}</TableCell>
                  <TableCell>{status.trend?.["H1"] ?? "-"}</TableCell>
                  <TableCell>{status.trend?.["H4"] ?? "-"}</TableCell>
                  <TableCell>{status.trend?.["D"] ?? "-"}</TableCell>
                  <TableCell>{new Date(status.updated_at).toLocaleString()}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </main>
  );
}
