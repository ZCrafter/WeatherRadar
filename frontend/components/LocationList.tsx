"use client";

import { deleteLocation, runSnapshot } from "../lib/api";

export default function LocationList({
  locations,
  selectedLocationId,
  onSelect,
  onChanged,
}: {
  locations: any[];
  selectedLocationId: number | null;
  onSelect: (id: number) => void;
  onChanged: () => void;
}) {
  return (
    <div>
      <h2>Saved locations</h2>
      <ul style={{ listStyle: "none", padding: 0, display: "grid", gap: 12 }}>
        {locations.map((l) => (
          <li
            key={l.id}
            style={{
              padding: 12,
              borderRadius: 12,
              background: selectedLocationId === l.id ? "#1b2850" : "#111a33",
              border: "1px solid #27345d",
            }}
          >
            <strong>{l.name}</strong>
            <div>{l.latitude}, {l.longitude}</div>
            <div>{l.timezone}</div>
            <div style={{ display: "flex", gap: 8, marginTop: 8, flexWrap: "wrap" }}>
              <button onClick={() => onSelect(l.id)}>View</button>
              <button
                onClick={async () => {
                  await runSnapshot(l.id);
                  onChanged();
                }}
              >
                Snapshot now
              </button>
              <button
                onClick={async () => {
                  await deleteLocation(l.id);
                  onChanged();
                }}
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
