import { useEffect, useState } from "react";
import { getStatus } from "@/lib/api";

export default function StatusTable() {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    getStatus().then(setData);
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">📊 실시간 상태</h2>
      <table className="w-full text-left border-collapse">
        <thead><tr><th>심볼</th><th>시간대</th><th>RSI</th><th>Trend</th></tr></thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx}>
              <td>{row.symbol}</td>
              <td>{row.timeframe}</td>
              <td>{row.rsi}</td>
              <td>{row.trend}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}