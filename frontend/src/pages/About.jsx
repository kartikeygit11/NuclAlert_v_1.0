import { motion } from 'framer-motion';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';

const About = () => (
  <div className="min-h-screen bg-slate-950 text-slate-100">
    <NavBar />
    <div className="max-w-4xl mx-auto px-6 space-y-8 pt-28 pb-14">
      <motion.div
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-slate-900/80 border border-slate-800 rounded-2xl p-8 shadow-2xl"
      >
        <p className="text-sm uppercase tracking-[0.18em] text-primary font-semibold mb-2">About</p>
        <h1 className="text-3xl font-bold text-white mb-3">Built for situational awareness</h1>
        <p className="text-slate-200">
          NuclrAlert is an awareness tool designed to surface proximity risks around nuclear plants. It is not a replacement for official alerts, but a companion that helps you see risk zones, understand distances, and act promptly.
        </p>
      </motion.div>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.55 }}
        className="bg-slate-900/70 border border-slate-800 rounded-xl p-6 shadow-lg space-y-3"
      >
        <h2 className="text-xl font-semibold text-white">What we value</h2>
        <ul className="text-slate-200 space-y-2 list-disc list-inside">
          <li>Clarity: simple alerts, clear maps, and concise guidance.</li>
          <li>Safety-first: highlight danger, moderate, and safe zones with urgency.</li>
          <li>Transparency: show data sources and thresholds openly.</li>
        </ul>
      </motion.div>
    </div>
    <Footer />
  </div>
);

export default About;

