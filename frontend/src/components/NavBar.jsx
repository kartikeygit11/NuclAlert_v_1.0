import { Link, NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';

const navItems = [
  { to: '/', label: 'Home' },
  { to: '/why', label: 'Why' },
  { to: '/working', label: 'Working' },
  { to: '/about', label: 'About' },
  { to: '/safety', label: 'Safety' },
];

const NavBar = () => {
  return (
    <motion.nav
      initial={{ opacity: 0, y: -12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="fixed top-0 inset-x-0 z-40"
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between rounded-2xl bg-slate-900/40 border border-slate-800/70 backdrop-blur-xl shadow-lg">
        <Link to="/" className="flex items-center gap-3 text-white font-bold text-lg">
          <span className="text-2xl">☢️</span>
          <div className="leading-5">
            <p>NuclrAlert</p>
            <p className="text-xs text-primary font-semibold uppercase tracking-wide">Safety First</p>
          </div>
        </Link>
        <div className="flex items-center gap-4 text-sm font-semibold">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `px-3 py-2 rounded-lg transition ${
                  isActive ? 'text-primary bg-slate-800/70' : 'text-slate-200 hover:text-white'
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </div>
      </div>
    </motion.nav>
  );
};

export default NavBar;

