import { useState } from 'react';
import { ZoomIn, ZoomOut, Maximize2 } from 'lucide-react';
import { motion } from 'framer-motion';

const ResultsVisualization = ({ result, type }) => {
  const [selectedView, setSelectedView] = useState('original');
  const [isFullscreen, setIsFullscreen] = useState(false);

  const views = [
    { id: 'original', label: 'Original', image: result.original_image },
    { id: 'heatmap', label: 'Heatmap', image: result.heatmap },
  ];

  const currentImage = views.find(v => v.id === selectedView)?.image;

  return (
    <div className="card">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-bold">Image Analysis</h3>
        <button
          onClick={() => setIsFullscreen(!isFullscreen)}
          className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          title="Toggle fullscreen"
        >
          <Maximize2 size={20} />
        </button>
      </div>

      {/* View Selector */}
      <div className="flex space-x-2 mb-4">
        {views.map((view) => (
          <button
            key={view.id}
            onClick={() => setSelectedView(view.id)}
            className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
              selectedView === view.id
                ? 'bg-gradient-to-r from-primary to-secondary text-white shadow-md'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
            }`}
          >
            {view.label}
          </button>
        ))}
      </div>

      {/* Image Display */}
      <motion.div
        key={selectedView}
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
        className={`relative bg-gray-900 rounded-lg overflow-hidden ${
          isFullscreen ? 'fixed inset-0 z-50 m-4' : 'h-96'
        }`}
      >
        <img
          src={currentImage}
          alt={selectedView}
          className="w-full h-full object-contain"
        />
        
        {/* View Label Overlay */}
        <div className="absolute top-4 left-4 bg-black bg-opacity-60 text-white px-3 py-1 rounded-lg text-sm font-medium">
          {views.find(v => v.id === selectedView)?.label}
        </div>

        {/* Close fullscreen button */}
        {isFullscreen && (
          <button
            onClick={() => setIsFullscreen(false)}
            className="absolute top-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors"
          >
            Close
          </button>
        )}
      </motion.div>

      {/* Legend */}
      {selectedView === 'heatmap' && (
        <div className="mt-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Heatmap Legend:</p>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-blue-500 rounded"></div>
              <span className="text-xs text-gray-600 dark:text-gray-400">Low Activity</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-yellow-500 rounded"></div>
              <span className="text-xs text-gray-600 dark:text-gray-400">Medium</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-red-500 rounded"></div>
              <span className="text-xs text-gray-600 dark:text-gray-400">High Activity</span>
            </div>
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
            Areas of interest are highlighted based on edge detection and feature analysis
          </p>
        </div>
      )}

      {/* Image Comparison Grid */}
      <div className="mt-4 grid grid-cols-2 gap-2">
        {views.map((view) => (
          <button
            key={view.id}
            onClick={() => setSelectedView(view.id)}
            className={`relative overflow-hidden rounded-lg border-2 transition-all ${
              selectedView === view.id
                ? 'border-primary ring-2 ring-primary ring-opacity-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <img
              src={view.image}
              alt={view.label}
              className="w-full h-24 object-cover"
            />
            <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-60 text-white text-xs py-1 text-center">
              {view.label}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default ResultsVisualization;
