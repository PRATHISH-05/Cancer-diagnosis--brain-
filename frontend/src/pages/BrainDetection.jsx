import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Brain, AlertCircle, CheckCircle, Loader, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import ResultsVisualization from '../components/ResultsVisualization';

const BrainDetection = ({ onScanComplete }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.bmp', '.dicom']
    },
    multiple: false
  });

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post('http://localhost:5000/api/brain/detect', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
      if (onScanComplete) onScanComplete();
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred during analysis');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
  };

  const getTumorColor = (tumorType) => {
    const colors = {
      'Glioma': 'text-red-600 bg-red-50 border-red-300',
      'Meningioma': 'text-orange-600 bg-orange-50 border-orange-300',
      'No Tumor': 'text-green-600 bg-green-50 border-green-300',
      'Pituitary': 'text-purple-600 bg-purple-50 border-purple-300'
    };
    return colors[tumorType] || 'text-gray-600 bg-gray-50 border-gray-300';
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 mb-4 gradient-bg rounded-full">
          <Brain className="text-white" size={32} />
        </div>
        <h1 className="text-4xl font-bold mb-3 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          Brain Tumor Detection
        </h1>
        <p className="text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
          Upload an MRI scan to detect and classify brain tumors using our advanced AI model
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Upload Section */}
        <div className="space-y-6">
          {/* File Upload */}
          {!preview ? (
            <div
              {...getRootProps()}
              className={`card cursor-pointer border-2 border-dashed transition-all duration-300 ${
                isDragActive
                  ? 'border-primary bg-purple-50 scale-105'
                  : 'border-gray-300 hover:border-primary'
              }`}
            >
              <input {...getInputProps()} />
              <div className="text-center py-12">
                <Upload
                  className={`mx-auto mb-4 transition-colors ${
                    isDragActive ? 'text-primary' : 'text-gray-400 dark:text-gray-500'
                  }`}
                  size={64}
                />
                <h3 className="text-xl font-bold mb-2">
                  {isDragActive ? 'Drop the image here' : 'Upload MRI Scan'}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 mb-4">
                  Drag & drop your MRI image, or click to browse
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Supports: PNG, JPG, JPEG, BMP, DICOM
                </p>
              </div>
            </div>
          ) : (
            <div className="card relative">
              <button
                onClick={handleReset}
                className="absolute top-4 right-4 p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
              >
                <X size={20} />
              </button>
              <h3 className="text-lg font-bold mb-4">Uploaded Image</h3>
              <img
                src={preview}
                alt="Preview"
                className="w-full h-64 object-contain bg-gray-100 dark:bg-gray-700 rounded-lg mb-4"
              />
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="btn-primary w-full flex items-center justify-center space-x-2"
              >
                {loading ? (
                  <>
                    <Loader className="animate-spin" size={20} />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Brain size={20} />
                    <span>Analyze MRI Scan</span>
                  </>
                )}
              </button>
            </div>
          )}

          {/* Info Card */}
          <div className="card bg-blue-50 border-2 border-blue-200">
            <h3 className="font-bold text-blue-900 mb-3 flex items-center">
              <AlertCircle className="mr-2" size={20} />
              Detection Capabilities
            </h3>
            <div className="space-y-2 text-sm text-blue-800">
              <div className="flex items-center">
                <CheckCircle size={16} className="mr-2 text-green-600" />
                <span><strong>Glioma:</strong> Most common malignant brain tumor</span>
              </div>
              <div className="flex items-center">
                <CheckCircle size={16} className="mr-2 text-green-600" />
                <span><strong>Meningioma:</strong> Usually benign tumor</span>
              </div>
              <div className="flex items-center">
                <CheckCircle size={16} className="mr-2 text-green-600" />
                <span><strong>Pituitary:</strong> Tumor of pituitary gland</span>
              </div>
              <div className="flex items-center">
                <CheckCircle size={16} className="mr-2 text-green-600" />
                <span><strong>No Tumor:</strong> Healthy brain scan</span>
              </div>
            </div>
            <div className="mt-4 pt-4 border-t border-blue-300">
              <p className="text-sm font-semibold text-blue-900">
                Model Accuracy: <span className="text-blue-600">93.29%</span>
              </p>
            </div>
          </div>
        </div>

        {/* Results Section */}
        <div className="space-y-6">
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg"
              >
                <div className="flex items-center">
                  <AlertCircle className="text-red-500 mr-3" size={24} />
                  <div>
                    <h3 className="font-bold text-red-900">Analysis Error</h3>
                    <p className="text-red-700">{error}</p>
                  </div>
                </div>
              </motion.div>
            )}

            {result && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-6"
              >
                {/* Prediction Result */}
                <div className={`result-card ${getTumorColor(result.tumor_type)}`}>
                  <h3 className="text-lg font-bold mb-2">Diagnosis Result</h3>
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <p className="text-3xl font-bold">{result.tumor_type}</p>
                      <p className="text-sm mt-1">
                        Confidence: <span className="font-bold">{result.confidence.toFixed(2)}%</span>
                      </p>
                    </div>
                    <Brain size={48} />
                  </div>
                  <div className="w-full bg-white bg-opacity-50 rounded-full h-3 overflow-hidden">
                    <div
                      className="h-full bg-current opacity-70 transition-all duration-1000"
                      style={{ width: `${result.confidence}%` }}
                    ></div>
                  </div>
                </div>

                {/* Visualization */}
                <ResultsVisualization result={result} type="brain" />

                {/* All Predictions */}
                <div className="card">
                  <h3 className="text-lg font-bold mb-4">All Class Probabilities</h3>
                  <div className="space-y-3">
                    {Object.entries(result.all_predictions).map(([className, probability]) => (
                      <div key={className}>
                        <div className="flex justify-between mb-1">
                          <span className="font-medium">{className}</span>
                          <span className="text-gray-600">{probability.toFixed(2)}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="h-2 rounded-full bg-gradient-to-r from-primary to-secondary transition-all duration-1000"
                            style={{ width: `${probability}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Action Buttons */}
                <button
                  onClick={handleReset}
                  className="btn-secondary w-full"
                >
                  Analyze Another Image
                </button>
              </motion.div>
            )}

            {!result && !error && !loading && preview && (
              <div className="card text-center py-12">
                <Brain className="mx-auto mb-4 text-gray-400" size={64} />
                <p className="text-gray-600">Click "Analyze MRI Scan" to start detection</p>
              </div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

export default BrainDetection;
