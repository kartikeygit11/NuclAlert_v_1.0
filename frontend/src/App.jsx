import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import Intro from './pages/Intro';
import Dashboard from './pages/Dashboard';
import Why from './pages/Why';
import Working from './pages/Working';
import About from './pages/About';
import Safety from './pages/Safety';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Intro />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/why" element={<Why />} />
        <Route path="/working" element={<Working />} />
        <Route path="/about" element={<About />} />
        <Route path="/safety" element={<Safety />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
