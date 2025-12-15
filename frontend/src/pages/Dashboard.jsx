import { useEffect, useState } from 'react';
import { API_BASE, getData, loadData, mapUrl } from '../lib/api';

const MetricCard = ({ label, value, color }) => (
  <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/80 shadow-lg text-center">
    <p className="text-sm text-slate-400 font-semibold">{label}</p>
    <p className="text-3xl font-bold" style={{ color }}>{value}</p>
  </div>
);

const AlertBanner = ({ data }) => {
  if (!data) return null;
  const { on_site_plants, dangerous_zones, moderate_zones, safe_zones } = data;

  if (on_site_plants?.length) {
    return (
      <div className="border-l-4 border-rose-500 bg-rose-500/10 p-4 rounded-lg">
        <h3 className="text-lg font-bold text-rose-300">🚨 ON-SITE ALERT</h3>
        <p className="text-slate-100">You are currently at: {on_site_plants.join(', ')}</p>
        <p className="text-slate-200 text-sm">Follow site safety protocols immediately.</p>
      </div>
    );
  }
  if (dangerous_zones?.length) {
    return (
      <div className="border-l-4 border-rose-500 bg-rose-500/10 p-4 rounded-lg">
        <h3 className="text-lg font-bold text-rose-300">🚨 HIGH RADIATION ALERT</h3>
        <p className="text-slate-100">Within 50km of {dangerous_zones.length} dangerous plants: {dangerous_zones.join(', ')}</p>
      </div>
    );
  }
  if (moderate_zones?.length) {
    return (
      <div className="border-l-4 border-amber-400 bg-amber-500/10 p-4 rounded-lg">
        <h3 className="text-lg font-bold text-amber-200">⚠️ Moderate Radiation Warning</h3>
        <p className="text-slate-100">Within 75km of {moderate_zones.length} aging plants: {moderate_zones.join(', ')}</p>
      </div>
    );
  }
  if (safe_zones?.length) {
    return (
      <div className="border-l-4 border-emerald-500 bg-emerald-500/10 p-4 rounded-lg">
        <h3 className="text-lg font-bold text-emerald-200">✅ Safe Zone</h3>
        <p className="text-slate-100">Near {safe_zones.length} newer plants: {safe_zones.join(', ')}</p>
      </div>
    );
  }
  return (
    <div className="border-l-4 border-slate-500 bg-slate-700/20 p-4 rounded-lg">
      <h3 className="text-lg font-bold text-slate-200">🌿 Clear Area</h3>
      <p className="text-slate-100">No immediate proximity of any known nuclear plants.</p>
    </div>
  );
};

const MapFrame = ({ filename }) => {
  if (!filename) {
    return <p className="text-slate-400 text-sm">Map will appear once data is loaded.</p>;
  }
  return (
    <div className="rounded-xl overflow-hidden border border-slate-800 shadow-xl">
      <iframe
        title="Radiation Map"
        src={mapUrl(filename)}
        className="w-full h-[520px] border-0"
        loading="lazy"
      />
    </div>
  );
};

const PlantsTable = ({ plants }) => {
  if (!plants?.length) return <p className="text-slate-400 text-sm">No plants available.</p>;
  return (
    <div className="overflow-x-auto border border-slate-800 rounded-xl shadow-lg">
      <table className="min-w-full text-sm">
        <thead className="bg-slate-900 text-slate-200">
          <tr>
            <th className="px-4 py-3 text-left">Name</th>
            <th className="px-4 py-3 text-left">Latitude</th>
            <th className="px-4 py-3 text-left">Longitude</th>
            <th className="px-4 py-3 text-left">Age</th>
            <th className="px-4 py-3 text-left">Safety</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800 bg-slate-900/60">
          {plants.map((p) => (
            <tr key={`${p.Name}-${p.Latitude}`}>
              <td className="px-4 py-3 text-slate-100">{p.Name}</td>
              <td className="px-4 py-3 text-slate-300">{p.Latitude}</td>
              <td className="px-4 py-3 text-slate-300">{p.Longitude}</td>
              <td className="px-4 py-3 text-slate-100">{p.Age}</td>
              <td className="px-4 py-3 font-semibold">
                <span
                  className={
                    p.Safety === 'Dangerous'
                      ? 'text-rose-400'
                      : p.Safety === 'Moderate'
                        ? 'text-amber-400'
                        : 'text-emerald-400'
                  }
                >
                  {p.Safety}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const NearbyList = ({ distances = [] }) => {
  if (!distances.length) return <p className="text-slate-400 text-sm">No nearby plants detected within range.</p>;
  const sorted = [...distances].sort((a, b) => a.Distance - b.Distance).slice(0, 5);
  return (
    <div className="space-y-3">
      {sorted.map((plant) => (
        <div
          key={plant.Name}
          className="p-4 rounded-lg border border-slate-800 bg-slate-900/70 flex items-center justify-between"
        >
          <div>
            <p className="font-semibold text-slate-100">{plant.Name}</p>
            <p className="text-slate-400 text-sm">
              Age: {plant.Age} yrs • Status: <span className="font-semibold">{plant.Safety}</span>
            </p>
          </div>
          <p className="text-emerald-300 font-bold">{plant.Distance.toFixed(2)} km</p>
        </div>
      ))}
    </div>
  );
};

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('alerts');

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      let result = await getData();
      if (!result?.plants || result.plants.length === 0) {
        await loadData();
        result = await getData();
      }
      setData(result);
    } catch (err) {
      setError(err.message || 'Unable to load data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const totals = {
    total: data?.plants?.length || 0,
    safe: data?.plants?.filter((p) => p.Safety === 'Safe').length || 0,
    moderate: data?.plants?.filter((p) => p.Safety === 'Moderate').length || 0,
    dangerous: data?.plants?.filter((p) => p.Safety === 'Dangerous').length || 0,
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-7xl mx-auto px-6 py-10 space-y-6">
        <header className="bg-slate-900/80 border border-slate-800 rounded-3xl p-6 shadow-2xl backdrop-blur flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-primary font-semibold">Nuclear Safety Dashboard</p>
            <h1 className="text-3xl font-bold text-white mt-1">Real-time Nuclear Hazard Tracking</h1>
            <p className="text-slate-300 text-sm mt-2">Data sourced from backend /data/data2.csv and processed on demand.</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={fetchData}
              className="px-4 py-3 rounded-xl bg-primary text-slate-950 font-semibold shadow-lg hover:scale-[1.01] transition"
            >
              🔄 Reload Data
            </button>
          </div>
        </header>

        {error && (
          <div className="border border-rose-500/40 bg-rose-500/10 text-rose-100 px-4 py-3 rounded-xl">
            {error}
          </div>
        )}

        {loading ? (
          <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-10 text-center shadow-xl">
            <p className="text-lg font-semibold">⏳ Loading data...</p>
            <p className="text-slate-400 text-sm mt-2">Processing nuclear plant dataset</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <MetricCard label="Total Plants" value={totals.total} color="#e5e7eb" />
              <MetricCard label="Safe Plants" value={totals.safe} color="#22c55e" />
              <MetricCard label="Moderate Plants" value={totals.moderate} color="#f59e0b" />
              <MetricCard label="Dangerous Plants" value={totals.dangerous} color="#ef4444" />
            </div>

            <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
              <div className="flex flex-wrap gap-3 border-b border-slate-800 pb-3">
                {['alerts', 'map', 'data'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`px-4 py-2 rounded-lg text-sm font-semibold ${
                      activeTab === tab ? 'bg-primary text-slate-950' : 'bg-slate-800 text-slate-200'
                    }`}
                  >
                    {tab === 'alerts' && '🚨 Alerts'}
                    {tab === 'map' && '🌍 Map'}
                    {tab === 'data' && '📊 Data'}
                  </button>
                ))}
              </div>

              {activeTab === 'alerts' && (
                <div className="space-y-4">
                  <h3 className="text-xl font-semibold text-white">Current Radiation Status</h3>
                  <AlertBanner data={data} />
                  <div>
                    <h4 className="text-lg font-semibold mb-3">Nearby Nuclear Plants</h4>
                    <NearbyList distances={data?.distances} />
                  </div>
                </div>
              )}

              {activeTab === 'map' && (
                <div className="space-y-3">
                  <h3 className="text-xl font-semibold text-white">Interactive Radiation Map</h3>
                  <p className="text-slate-400 text-sm">🟢 Safe | 🟠 Moderate | 🔴 Dangerous</p>
                  <MapFrame filename={data?.map_filename} />
                </div>
              )}

              {activeTab === 'data' && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xl font-semibold text-white">Nuclear Plant Database</h3>
                    <a
                      className="px-4 py-2 rounded-lg bg-primary text-slate-950 font-semibold shadow hover:scale-[1.01] transition"
                      href={`${API_BASE}/download_processed`}
                      target="_blank"
                    >
                      📥 Download Processed Data
                    </a>
                  </div>
                  <PlantsTable plants={data?.plants} />
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Dashboard;

