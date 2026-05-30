"use client";

import { useEffect, useState } from "react";
import LocationForm from "./LocationForm";
import LocationList from "./LocationList";
import ComparisonDashboard from "./ComparisonDashboard";
import { getLocations, getModels, getComparison } from "../lib/api";

export default function AppShell() {
  const [locations, setLocations] = useState<any[]>([]);
  const [models, setModels] = useState<any[]>([]);
  const [selectedLocationId, setSelectedLocationId] = useState<number | null>(null);
  const [comparison, setComparison] = useState<any[]>([]);

  async function refresh(locationId?: number) {
    const locs = await getLocations();
    const mods = await getModels();
    setLocations(locs);
    setModels(mods);

    const nextId = locationId ?? selectedLocationId ?? locs[0]?.id ?? null;
    setSelectedLocationId(nextId);
    if (nextId) {
      const comp = await getComparison(nextId);
      setComparison(comp);
    } else {
      setComparison([]);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  return (
    <main>
      <h1>Weather Radar</h1>
      <div className="card">
        <LocationForm onAdded={() => refresh()} />
      </div>
      <div className="card">
        <LocationList
          locations={locations}
          selectedLocationId={selectedLocationId}
          onSelect={(id) => refresh(id)}
          onChanged={() => refresh()}
        />
      </div>
      <div className="card">
        <ComparisonDashboard locationId={selectedLocationId} models={models} comparison={comparison} />
      </div>
    </main>
  );
}
