import { useState, useEffect } from 'react';
import { History as HistoryIcon, Brain, Waves, Clock, TrendingUp } from 'lucide-react';
import { motion } from 'framer-motion';
import axios from 'axios';

const History = () => {
  const [brainHistory, setBrainHistory] = useState([]);
  const [lungHistory, setLungHistory] = useState([]);
  const [activeTab, setActiveTab] = useState('brain');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const [brainRes, lungRes] = await Promise.all([
        axios.get('http://localhost:5000/api/history/brain'),
        axios.get('http://localhost:5000/api/history/lung')
      ]);
      
      setBrainHistory(brainRes.data.history || []);
      setLungHistory(lungRes.data.history || []);
    } catch (error) {
      console.error('Error fetching history:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getTumorColor = (tumorType) => {
    const colors = {
      'Glioma': 'bg-red-100 text-red-700',
      'Meningioma': 'bg-orange-100 text-orange-700',
      'No Tumor': 'bg-green-100 text-green-700',
      'Pituitary': 'bg-purple-100 text-purple-700'
    };
    return colors[tumorType] || 'bg-gray-100 text-gray-700';
  };

  const getDiagnosisColor = (diagnosis) => {
    const colors = {
      'Normal': 'bg-green-100 text-green-700',
      'Benign': 'bg-yellow-100 text-yellow-700',
      'Malignant': 'bg-red-100 text-red-700'
    };
    return colors[diagnosis] || 'bg-gray-100 text-gray-700';
  };

  const getStats = (history) => {
    if (history.length === 0) return null;

    const avgConfidence = history.reduce((sum, item) => sum + item.confidence, 0) / history.length;
    const classifications = {};
    
    history.forEach(item => {
      const key = item.tumor_type || item.diagnosis;
      classifications[key] = (classifications[key] || 0) + 1;
    });

    return { avgConfidence, classifications };
  };

  const currentHistory = activeTab === 'brain' ? brainHistory : lungHistory;
  const stats = getStats(currentHistory);

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 mb-4 gradient-bg rounded-full">
          <HistoryIcon className="text-white" size={32} />
        </div>
        <h1 className="text-4xl font-bold mb-3">Detection History</h1>
        <p className="text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
          View your past scan results and track analysis patterns
        </p>
      </div>

      {/* Stats Overview */}
      {stats && (
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="card text-center">
            <TrendingUp className="mx-auto mb-2 text-primary" size={32} />
            <div className="text-3xl font-bold text-primary">{currentHistory.length}</div>
            <div className="text-gray-600 dark:text-gray-400">Total Scans</div>
          </div>
          <div className="card text-center">
            <Brain className="mx-auto mb-2 text-secondary" size={32} />
            <div className="text-3xl font-bold text-secondary">{stats.avgConfidence.toFixed(1)}%</div>
            <div className="text-gray-600">Avg Confidence</div>
          </div>
          <div className="card text-center">
            <Clock className="mx-auto mb-2 text-green-600" size={32} />
            <div className="text-3xl font-bold text-green-600">
              {Object.keys(stats.classifications).length}
            </div>
            <div className="text-gray-600">Classifications</div>
          </div>
        </div>
      )}

      {/* Tab Selector */}
      <div className="flex space-x-2 mb-6">
        <button
          onClick={() => setActiveTab('brain')}
          className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all flex items-center justify-center space-x-2 ${
            activeTab === 'brain'
              ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg'
              : 'bg-white text-gray-700 hover:bg-gray-100'
          }`}
        >
          <Brain size={20} />
          <span>Brain Scans ({brainHistory.length})</span>
        </button>
        <button
          onClick={() => setActiveTab('lung')}
          className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all flex items-center justify-center space-x-2 ${
            activeTab === 'lung'
              ? 'bg-gradient-to-r from-purple-500 to-purple-600 text-white shadow-lg'
              : 'bg-white text-gray-700 hover:bg-gray-100'
          }`}
        >
          <Waves size={20} />
          <span>Lung Scans ({lungHistory.length})</span>
        </button>
      </div>

      {/* History List */}
      {loading ? (
        <div className="card text-center py-12">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Loading history...</p>
        </div>
      ) : currentHistory.length === 0 ? (
        <div className="card text-center py-12">
          <HistoryIcon className="mx-auto mb-4 text-gray-400" size={64} />
          <h3 className="text-xl font-bold text-gray-700 mb-2">No History Found</h3>
          <p className="text-gray-600 mb-4">
            Start scanning to see your detection history here
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {currentHistory.slice().reverse().map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              className="card hover:shadow-lg transition-all"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4 flex-1">
                  {/* Icon */}
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                    activeTab === 'brain' ? 'bg-blue-100' : 'bg-purple-100'
                  }`}>
                    {activeTab === 'brain' ? (
                      <Brain className={activeTab === 'brain' ? 'text-blue-600' : 'text-purple-600'} size={24} />
                    ) : (
                      <Waves className="text-purple-600" size={24} />
                    )}
                  </div>

                  {/* Info */}
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-1">
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                        activeTab === 'brain' 
                          ? getTumorColor(item.tumor_type)
                          : getDiagnosisColor(item.diagnosis)
                      }`}>
                        {item.tumor_type || item.diagnosis}
                      </span>
                      <span className="text-sm text-gray-500 flex items-center">
                        <Clock size={14} className="mr-1" />
                        {formatDate(item.timestamp)}
                      </span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-600">Confidence:</span>
                      <div className="flex-1 max-w-xs bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            activeTab === 'brain'
                              ? 'bg-gradient-to-r from-blue-400 to-blue-600'
                              : 'bg-gradient-to-r from-purple-400 to-purple-600'
                          }`}
                          style={{ width: `${item.confidence}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-semibold text-gray-700">
                        {item.confidence.toFixed(2)}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Classification Distribution */}
      {stats && stats.classifications && (
        <div className="card mt-8">
          <h3 className="text-lg font-bold mb-4">Classification Distribution</h3>
          <div className="space-y-3">
            {Object.entries(stats.classifications).map(([classification, count]) => {
              const percentage = (count / currentHistory.length) * 100;
              return (
                <div key={classification}>
                  <div className="flex justify-between mb-1">
                    <span className="font-medium">{classification}</span>
                    <span className="text-gray-600">{count} ({percentage.toFixed(1)}%)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${
                        activeTab === 'brain'
                          ? 'bg-gradient-to-r from-blue-400 to-blue-600'
                          : 'bg-gradient-to-r from-purple-400 to-purple-600'
                      }`}
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default History;
