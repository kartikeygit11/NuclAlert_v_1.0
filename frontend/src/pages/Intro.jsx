import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loadData, heroImageUrl } from '../lib/api';

const Intro = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleStart = async () => {
    setLoading(true);
    setError('');
    try {
      await loadData();
      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen bg-hero text-slate-100 flex items-center justify-center px-6 py-10"
      style={{
        backgroundImage: `linear-gradient(rgba(11, 18, 32, 0.78), rgba(11, 18, 32, 0.9)), url(${heroImageUrl})`,
      }}
    >
      <div className="max-w-5xl w-full space-y-8">
        <div className="bg-slate-900/80 border border-slate-800 shadow-2xl rounded-3xl p-10 backdrop-blur">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-8">
            <div className="space-y-4">
              <p className="text-sm uppercase tracking-[0.2em] text-primary font-semibold">NuclrAlert</p>
              <h1 className="text-3xl md:text-4xl font-bold text-white">
                Real-time Nuclear Radiation Detection &amp; Safety
              </h1>
              <p className="text-slate-200 max-w-3xl">
                Monitor risk zones, understand your proximity to nuclear plants, and receive instant alerts when you are on-site or near hazardous locations.
              </p>
              <div className="flex flex-wrap gap-3">
                <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-200 text-sm border border-emerald-500/30">
                  Live Location
                </span>
                <span className="px-3 py-1 rounded-full bg-blue-500/10 text-blue-200 text-sm border border-blue-500/30">
                  Interactive Maps
                </span>
                <span className="px-3 py-1 rounded-full bg-amber-500/10 text-amber-200 text-sm border border-amber-500/30">
                  Instant Alerts
                </span>
              </div>
              {error && <p className="text-rose-400 text-sm">{error}</p>}
              <div className="flex gap-4">
                <button
                  onClick={handleStart}
                  disabled={loading}
                  className="px-5 py-3 rounded-xl bg-primary text-slate-950 font-semibold shadow-lg shadow-emerald-500/30 hover:scale-[1.01] transition disabled:opacity-60"
                >
                  {loading ? 'Loading...' : '🚀 Proceed to Dashboard'}
                </button>
                <button
                  onClick={() => navigate('/dashboard')}
                  className="px-4 py-3 rounded-xl bg-slate-800 text-slate-100 border border-slate-700 hover:border-primary transition"
                >
                  View Dashboard
                </button>
              </div>
            </div>
            <div className="shrink-0">
              <div className="flex items-center justify-center w-28 h-28 rounded-2xl bg-slate-800 border border-slate-700 shadow-lg">
                <span className="text-5xl">☢️</span>
              </div>
            </div>
          </div>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-2 space-y-6">
            <section className="bg-slate-900/75 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-lg bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-300 text-xl">🔍</div>
                <h2 className="text-xl font-semibold text-white">Project Overview</h2>
              </div>
              <p className="text-slate-200 mb-4">
                NuclrAlert empowers you with situational awareness around nuclear sites. Stay ahead with precise proximity alerts and clear safety guidance.
              </p>
              <ul className="space-y-2 text-slate-200">
                <li className="flex items-start gap-2"><span className="text-emerald-400 mt-0.5">•</span> Real-time location tracking with IP geolocation fallback.</li>
                <li className="flex items-start gap-2"><span className="text-emerald-400 mt-0.5">•</span> Automatic classification of plants by safety and age.</li>
                <li className="flex items-start gap-2"><span className="text-emerald-400 mt-0.5">•</span> On-site detection and instant alerting.</li>
                <li className="flex items-start gap-2"><span className="text-emerald-400 mt-0.5">•</span> Interactive Folium maps with safety overlays.</li>
              </ul>
            </section>
          </div>
          <aside className="space-y-6">
            <section className="bg-slate-900/75 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-amber-500/15 border border-amber-500/30 flex items-center justify-center text-amber-300 text-xl">🧰</div>
                <h2 className="text-lg font-semibold text-white">Tech Stack</h2>
              </div>
              <div className="grid grid-cols-2 gap-3 text-slate-200 text-sm">
                <span className="px-3 py-2 rounded-xl bg-slate-800/70 border border-slate-700">Flask</span>
                <span className="px-3 py-2 rounded-xl bg-slate-800/70 border border-slate-700">React</span>
                <span className="px-3 py-2 rounded-xl bg-slate-800/70 border border-slate-700">Tailwind</span>
                <span className="px-3 py-2 rounded-xl bg-slate-800/70 border border-slate-700">Pandas</span>
                <span className="px-3 py-2 rounded-xl bg-slate-800/70 border border-slate-700">Geopy</span>
                <span className="px-3 py-2 rounded-xl bg-slate-800/70 border border-slate-700">Folium</span>
              </div>
            </section>
          </aside>
        </div>
      </div>
    </div>
  );
};

export default Intro;

