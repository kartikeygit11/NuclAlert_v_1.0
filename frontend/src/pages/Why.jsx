import { motion } from 'framer-motion';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';

const incidents = [
  {
    title: 'Chernobyl (1986)',
    detail: 'Unaware responders and residents were exposed to radioactive fallout, leading to acute radiation sickness and long-term health impacts.',
  },
  {
    title: 'Fukushima Daiichi (2011)',
    detail: 'Evacuation delays and limited awareness of plume spread increased exposure risks for nearby populations.',
  },
  {
    title: 'Goiania Incident (1987)',
    detail: 'Scrap workers unknowingly handled a radiotherapy source, spreading contamination and causing radiation sickness.',
  },
];

const Why = () => (
  <div className="min-h-screen bg-slate-950 text-slate-100">
    <NavBar />
    <div className="max-w-5xl mx-auto px-6 space-y-10 pt-28 pb-14">
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-slate-900/80 border border-slate-800 rounded-2xl p-8 shadow-2xl"
      >
        <p className="text-sm uppercase tracking-[0.18em] text-primary font-semibold mb-2">Why NuclrAlert</p>
        <h1 className="text-3xl font-bold text-white mb-3">Proactive safety for nuclear proximity</h1>
        <p className="text-slate-200">
          People often don’t realize when they are close to nuclear sources or legacy contamination sites. NuclrAlert provides instant proximity alerts, risk classification, and clear guidance to reduce accidental exposure.
        </p>
      </motion.div>

      <div className="grid md:grid-cols-3 gap-5">
        {incidents.map((item, idx) => (
          <motion.div
            key={item.title}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.1 * idx }}
            className="bg-slate-900/70 border border-slate-800 rounded-xl p-5 shadow-lg"
          >
            <h3 className="text-xl font-semibold text-white mb-2">{item.title}</h3>
            <p className="text-slate-300 text-sm">{item.detail}</p>
          </motion.div>
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-slate-900/70 border border-slate-800 rounded-xl p-6 shadow-lg"
      >
        <h2 className="text-2xl font-semibold text-white mb-2">How NuclrAlert helps</h2>
        <ul className="text-slate-200 space-y-2 list-disc list-inside">
          <li>Detects when you are near nuclear plants or mapped sources.</li>
          <li>Classifies risk by plant age and distance, issuing clear alerts.</li>
          <li>Shows interactive maps and safety guidance to minimize exposure.</li>
        </ul>
      </motion.div>
    </div>
    <Footer />
  </div>
);

export default Why;

