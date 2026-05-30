"use client";

import { useEffect, useState } from "react";
import LocationForm from "../components/LocationForm";
import LocationList from "../components/LocationList";
import ModelSelector from "../components/ModelSelector";
import ComparisonPanel from "../components/ComparisonPanel";
import { getLocations, getModels, getComparison } from "../lib/api";

export default function Page() {
  const [locations, setLocations] = useState<any[]>([]);
  const [models, setModels] = useState<any[]>([]);
  const [comparison, setComparison] = useState<any[]>([]);
  const [selectedLocationId, setSelectedLocationId] = useState<number | null>(null);

  async function refresh() {
    const locs = await getLocations();
    const mods = await getModels();
    setLocations(locs);
    setModels(mods);

    const firstId = selectedLocationId ?? locs[0]?.id ?? null;
    setSelectedLocationId(firstId);

    if (firstId) {
      const comp = await getComparison(firstId);
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
      <h1>Weather Tracker</h1>
      <p>Track many locations and compare weather models across lead times.</p>
      <ModelSelector models={models} />
      <LocationForm onAdded={refresh} />
      <LocationList locations={locations} onChanged={refresh} />
      <ComparisonPanel comparison={comparison} />
    </main>
  );
}
