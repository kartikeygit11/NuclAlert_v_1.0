const Footer = () => (
  <footer className="mt-10 border-t border-slate-800/80 bg-slate-950/80">
    <div className="max-w-7xl mx-auto px-6 py-4 flex flex-col md:flex-row items-center justify-between gap-2 text-xs text-slate-500">
      <p>© {new Date().getFullYear()} NuclrAlert – Educational nuclear safety awareness tool.</p>
      <p>Always follow official guidance from your local authorities.</p>
    </div>
  </footer>
);

export default Footer;

