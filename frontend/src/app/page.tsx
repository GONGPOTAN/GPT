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
    price: number | null;
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
        const res = await fetch("https://gpt-trading-bot.fly.dev/api/status");
        const json = await res.json();
        setData(json);
      } catch (error) {
        console.error("❌ 데이터 로딩 실패:", error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const formatKST = (utcString: string) => {
    const date = new Date(utcString);
    const kst = new Date(date.getTime() + 9 * 60 * 60 * 1000);
    return kst.toLocaleString("ko-KR", {
      year: "numeric",
      month: "numeric",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  return (
    <main className="pt-6 px-4 md:px-10">
      <h1 className="text-3xl font-extrabold mb-2">
        💣 GPT Trading Bot Dashboard
      </h1>

      <h2 className="text-xl font-semibold mb-4">📊 실시간 시세 & 지표 상태</h2>

      <Card>
        <CardContent className="overflow-x-auto p-4">
          <Table>
            <TableHeader>
              <TableRow>
                <TableCell>🪙 종목</TableCell>
                <TableCell>💰 가격</TableCell>
                <TableCell>📐 RSI (H1)</TableCell>
                <TableCell>RSI (H4)</TableCell>
                <TableCell>RSI (D)</TableCell>
                <TableCell>📈 추세 (H1)</TableCell>
                <TableCell>추세 (H4)</TableCell>
                <TableCell>추세 (D)</TableCell>
                <TableCell>🕒 업데이트</TableCell>
              </TableRow>
            </TableHeader>
            <TableBody>
              {Object.entries(data).map(([symbol, status]) => (
                <TableRow key={symbol}>
                  <TableCell>{symbol}</TableCell>
                  <TableCell>
                    {status.price != null
                      ? status.price.toLocaleString("ko-KR", {
                          maximumFractionDigits: 10,
                        })
                      : "-"}
                  </TableCell>
                  <TableCell>
                    {status.rsi?.H1 !== undefined
                      ? status.rsi.H1.toFixed(2)
                      : "-"}
                  </TableCell>
                  <TableCell>
                    {status.rsi?.H4 !== undefined
                      ? status.rsi.H4.toFixed(2)
                      : "-"}
                  </TableCell>
                  <TableCell>
                    {status.rsi?.D !== undefined
                      ? status.rsi.D.toFixed(2)
                      : "-"}
                  </TableCell>
                  <TableCell>{status.trend?.H1 ?? "-"}</TableCell>
                  <TableCell>{status.trend?.H4 ?? "-"}</TableCell>
                  <TableCell>{status.trend?.D ?? "-"}</TableCell>
                  <TableCell>{formatKST(status.updated_at)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </main>
  );
}