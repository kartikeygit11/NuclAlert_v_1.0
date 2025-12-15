import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import Intro from './pages/Intro';
import Dashboard from './pages/Dashboard';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Intro />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
