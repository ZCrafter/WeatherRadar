export default function ModelSelector({ models }: { models: any[] }) {
  return (
    <div style={{ marginBottom: 24 }}>
      <h2>Models</h2>
      <ul>
        {models.map((m) => (
          <li key={m.name}>
            {m.name} {m.enabled ? "enabled" : "disabled"}
          </li>
        ))}
      </ul>
    </div>
  );
}
