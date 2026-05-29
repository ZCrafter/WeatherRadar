import LocationForm from "../components/LocationForm";
import LocationList from "../components/LocationList";
import LocationTable from "../components/LocationTable";
import { getLocations } from "../lib/api";

export default async function Page() {
  const locations = await getLocations();

  return (
    <main>
      <h1>Weather Tracker</h1>
      <p>Track multiple locations and compare weather models over time.</p>
      <LocationTable locations={locations} />
      <div style={{ height: 24 }} />
      <LocationForm onAdded={() => {}} />
      <LocationList locations={locations} onChanged={() => {}} />
    </main>
  );
}
