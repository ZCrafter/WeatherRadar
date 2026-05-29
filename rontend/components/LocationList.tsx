"use client";

import { deleteLocation } from "../lib/api";

export default function LocationList({
  locations,
  onChanged,
}: {
  locations: any[];
  onChanged: () => void;
}) {
  return (
    <div>
      <h2>Saved locations</h2>
      <ul style={{ listStyle: "none", padding: 0, display: "grid", gap: 12 }}>
        {locations.map((l) => (
          <li key={l.id} style={{ padding: 12, background: "#111a33", borderRadius: 12 }}>
            <strong>{l.name}</strong>
            <div>{l.latitude}, {l.longitude}</div>
            <div>{l.timezone}</div>
            <button
              onClick={async () => {
                await deleteLocation(l.id);
                onChanged();
              }}
              style={{ marginTop: 8 }}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
