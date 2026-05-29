const base = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export async function getLocations() {
  const res = await fetch(`${base}/api/locations`, { cache: "no-store" });
  return res.json();
}

export async function addLocation(payload: {
  name: string;
  latitude: number;
  longitude: number;
  timezone?: string;
  notes?: string;
}) {
  const res = await fetch(`${base}/api/locations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function deleteLocation(id: number) {
  const res = await fetch(`${base}/api/locations/${id}`, {
    method: "DELETE",
  });
  return res.json();
}
