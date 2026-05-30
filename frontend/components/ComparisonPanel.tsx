"use client";

export default function ComparisonPanel({ comparison }: { comparison: any[] }) {
  return (
    <div style={{ marginTop: 24 }}>
      <h2>Comparison</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th align="left">Model</th>
            <th align="left">Temp MAE</th>
            <th align="left">Temp Bias</th>
            <th align="left">Pairs</th>
          </tr>
        </thead>
        <tbody>
          {comparison.map((row) => (
            <tr key={row.model}>
              <td>{row.model}</td>
              <td>{row.temp_mae ?? "-"}</td>
              <td>{row.temp_bias ?? "-"}</td>
              <td>{row.pairs}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
