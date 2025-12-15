import { motion } from 'framer-motion';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';

const guidelines = [
  'Stay at least 50km from dangerous plants; evacuate if instructed.',
  'Limit outdoor exposure and seal indoor spaces if advised by authorities.',
  'Carry battery-powered radio/phone for official alerts; follow local guidance.',
  'Avoid consuming locally sourced food or water until safety is confirmed.',
  'If contaminated, remove outer clothing and wash exposed skin promptly.',
  'Know evacuation routes and shelter locations in your area.',
];

const Safety = () => (
  <div className="min-h-screen bg-slate-950 text-slate-100">
    <NavBar />
    <div className="max-w-4xl mx-auto px-6 space-y-8 pt-28 pb-14">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-slate-900/80 border border-slate-800 rounded-2xl p-8 shadow-2xl"
      >
        <p className="text-sm uppercase tracking-[0.18em] text-primary font-semibold mb-2">Safety Guidelines</p>
        <h1 className="text-3xl font-bold text-white mb-3">Protect yourself near nuclear sites</h1>
        <p className="text-slate-200">
          These practical steps help reduce exposure risk when you are near nuclear facilities or during an incident.
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.55 }}
        className="bg-slate-900/70 border border-slate-800 rounded-xl p-6 shadow-lg"
      >
        <ul className="space-y-3 text-slate-200">
          {guidelines.map((g) => (
            <li key={g} className="flex items-start gap-3">
              <span className="w-2 h-2 mt-2 rounded-full bg-primary" />
              <span>{g}</span>
            </li>
          ))}
        </ul>
      </motion.div>
    </div>
    <Footer />
  </div>
);

export default Safety;

