import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import BrainDetection from './pages/BrainDetection';
import LungDetection from './pages/LungDetection';
import History from './pages/History';
import About from './pages/About';
import Settings from './pages/Settings';

function App() {
  const [stats, setStats] = useState({
    total_scans: 0,
    brain_scans: 0,
    lung_scans: 0
  });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
        <Navbar stats={stats} />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/brain" element={<BrainDetection onScanComplete={fetchStats} />} />
            <Route path="/lung" element={<LungDetection onScanComplete={fetchStats} />} />
            <Route path="/history" element={<History />} />
            <Route path="/about" element={<About />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
