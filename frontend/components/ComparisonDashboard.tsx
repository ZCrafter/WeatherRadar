"use client";

import { useMemo } from "react";

function num(v: any, digits = 2) {
  if (v === null || v === undefined || Number.isNaN(v)) return "-";
  return Number(v).toFixed(digits);
}

export default function ComparisonDashboard({
  locationId,
  models,
  comparison,
}: {
  locationId: number | null;
  models: any[];
  comparison: any[];
}) {
  const modelsList = models.map((m) => m.name).join(", ");

  const chartData = useMemo(() => {
    return comparison.flatMap((m) =>
      (m.series || []).map((p: any) => ({
        model: m.model,
        time: p.target_time,
        temp_error: p.temp_error,
        precip_error: p.precip_error,
        lead_minutes: p.lead_minutes,
      }))
    );
  }, [comparison]);

  if (!locationId) {
    return <div>Select a location to see comparisons.</div>;
  }

  return (
    <div>
      <h2>Comparison</h2>
      <div style={{ marginBottom: 8, opacity: 0.8 }}>Models loaded: {modelsList}</div>

      {comparison.map((m) => (
        <div key={m.model} style={{ marginBottom: 24 }}>
          <h3>{m.model}</h3>
          <div>Temp MAE: {num(m.overall?.temp_mae, 2)}</div>
          <div>Temp Bias: {num(m.overall?.temp_bias, 2)}</div>
          <div>Precip Brier: {num(m.overall?.precip_brier, 4)}</div>
          <div>Precip Hit Rate: {num(m.overall?.precip_hit_rate, 3)}</div>
          <div>Pairs: {m.overall?.pairs ?? 0}</div>

          <table style={{ width: "100%", marginTop: 12, borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th align="left">Lead</th>
                <th align="left">Temp MAE</th>
                <th align="left">Temp Bias</th>
                <th align="left">Precip Brier</th>
                <th align="left">Precip Hit</th>
                <th align="left">Pairs</th>
              </tr>
            </thead>
            <tbody>
              {(m.buckets || []).map((b: any) => (
                <tr key={b.lead_minutes}>
                  <td>{b.lead_minutes}m</td>
                  <td>{num(b.temp_mae, 2)}</td>
                  <td>{num(b.temp_bias, 2)}</td>
                  <td>{num(b.precip_brier, 4)}</td>
                  <td>{num(b.precip_hit_rate, 3)}</td>
                  <td>{b.pairs}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}

      <div style={{ marginTop: 24 }}>
        <h3>Time series data points</h3>
        <div style={{ maxHeight: 240, overflow: "auto", fontFamily: "monospace", whiteSpace: "pre-wrap" }}>
          {JSON.stringify(chartData.slice(0, 40), null, 2)}
        </div>
      </div>
    </div>
  );
}
