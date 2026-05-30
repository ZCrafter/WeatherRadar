"use client";

import { useState } from "react";
import { addLocation } from "../lib/api";

export default function LocationForm({ onAdded }: { onAdded: () => void }) {
  const [name, setName] = useState("");
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [timezone, setTimezone] = useState("auto");
  const [notes, setNotes] = useState("");

  async function submit() {
    await addLocation({
      name,
      latitude: Number(latitude),
      longitude: Number(longitude),
      timezone,
      notes,
    });
    setName("");
    setLatitude("");
    setLongitude("");
    setTimezone("auto");
    setNotes("");
    onAdded();
  }

  return (
    <div style={{ display: "grid", gap: 8 }}>
      <h2>Add location</h2>
      <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
      <input placeholder="Latitude" value={latitude} onChange={(e) => setLatitude(e.target.value)} />
      <input placeholder="Longitude" value={longitude} onChange={(e) => setLongitude(e.target.value)} />
      <input placeholder="Timezone" value={timezone} onChange={(e) => setTimezone(e.target.value)} />
      <input placeholder="Notes" value={notes} onChange={(e) => setNotes(e.target.value)} />
      <button onClick={submit}>Save</button>
    </div>
  );
}
