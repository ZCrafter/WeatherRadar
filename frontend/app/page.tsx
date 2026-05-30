import LocationForm from "../components/LocationForm";
import LocationList from "../components/LocationList";
import ModelSelector from "../components/ModelSelector";
import ComparisonPanel from "../components/ComparisonPanel";
import { getLocations, getModels, getComparison } from "../lib/api";

export default async function Page() {
  const locations = await getLocations();
  const models = await getModels();
  const comparison = locations.length ? await getComparison(locations[0].id) : [];

  return (
    <main>
      <h1>Weather Tracker</h1>
      <p>Track many locations and compare weather models across lead times.</p>
      <ModelSelector models={models} />
      <LocationForm onAdded={() => {}} />
      <LocationList locations={locations} onChanged={() => {}} />
      <ComparisonPanel comparison={comparison} />
    </main>
  );
}
