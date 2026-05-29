export default function LocationTable({ locations }: { locations: any[] }) {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th align="left">Name</th>
          <th align="left">Lat</th>
          <th align="left">Lon</th>
          <th align="left">Timezone</th>
        </tr>
      </thead>
      <tbody>
        {locations.map((l) => (
          <tr key={l.id}>
            <td>{l.name}</td>
            <td>{l.latitude}</td>
            <td>{l.longitude}</td>
            <td>{l.timezone}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
