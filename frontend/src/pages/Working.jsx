import { motion } from 'framer-motion';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';

const steps = [
  { title: 'Load dataset', detail: 'We ingest curated nuclear plant data (name, latitude, longitude, age).' },
  { title: 'Locate user', detail: 'We resolve your position with geolocation and fallback to IP-based estimation.' },
  { title: 'Compute distances', detail: 'Geodesic calculations determine exact distance to every plant.' },
  { title: 'Classify risk', detail: 'Age thresholds and distance bands mark plants as Safe / Moderate / Dangerous.' },
  { title: 'Render map', detail: 'Folium/Leaflet map shows you and nearby plants with safety colors.' },
  { title: 'Notify & guide', detail: 'If you are on-site or in risk zones, we raise alerts and show guidance.' },
];

const Working = () => (
  <div className="min-h-screen bg-slate-950 text-slate-100">
    <NavBar />
    <div className="max-w-6xl mx-auto px-6 space-y-8 pt-28 pb-14">
      <motion.div
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-slate-900/80 border border-slate-800 rounded-2xl p-8 shadow-2xl"
      >
        <p className="text-sm uppercase tracking-[0.18em] text-primary font-semibold mb-2">Working</p>
        <h1 className="text-3xl font-bold text-white mb-3">How the system works</h1>
        <p className="text-slate-200">
          NuclrAlert combines geolocation, distance computation, and safety classification to give you clear, actionable insight about nuclear proximity.
        </p>
      </motion.div>

      <div className="grid md:grid-cols-2 gap-5">
        {steps.map((step, idx) => (
          <motion.div
            key={step.title}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.45, delay: idx * 0.05 }}
            className="bg-slate-900/70 border border-slate-800 rounded-xl p-5 shadow-lg"
          >
            <div className="flex items-center gap-3 mb-2">
              <span className="w-9 h-9 rounded-full bg-primary/15 border border-primary/40 text-primary font-bold flex items-center justify-center">
                {idx + 1}
              </span>
              <h3 className="text-lg font-semibold text-white">{step.title}</h3>
            </div>
            <p className="text-slate-300 text-sm">{step.detail}</p>
          </motion.div>
        ))}
      </div>
    </div>
    <Footer />
  </div>
);

export default Working;

