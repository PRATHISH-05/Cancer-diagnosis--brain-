import { Link } from 'react-router-dom';
import { Brain, Waves, ArrowRight, Shield, Zap, Target } from 'lucide-react';
import { motion } from 'framer-motion';

const Home = () => {
  const features = [
    {
      icon: Shield,
      title: 'High Accuracy',
      description: 'Brain: 93.29% | Lung: 99.36% recall'
    },
    {
      icon: Zap,
      title: 'Fast Analysis',
      description: 'Get results in seconds with AI processing'
    },
    {
      icon: Target,
      title: 'Precise Detection',
      description: 'Advanced CNN models for accurate diagnosis'
    }
  ];

  const fadeIn = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Hero Section */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={fadeIn}
        transition={{ duration: 0.6 }}
        className="text-center py-16 px-4"
      >
        <div className="inline-block mb-4 px-4 py-2 bg-purple-100 dark:bg-purple-900 text-primary dark:text-purple-300 rounded-full text-sm font-semibold">
          AI-Powered Medical Imaging
        </div>
        <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary via-purple-500 to-secondary bg-clip-text text-transparent">
          Cancer Detection Platform
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
          Advanced deep learning models for accurate detection and analysis of brain tumors and lung cancer from medical imaging
        </p>
        <div className="flex justify-center gap-4 flex-wrap">
          <Link to="/brain" className="btn-primary">
            Start Brain Scan
          </Link>
          <Link to="/lung" className="btn-secondary">
            Start Lung Scan
          </Link>
        </div>
      </motion.div>

      {/* Features */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={fadeIn}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="grid md:grid-cols-3 gap-6 mb-16"
      >
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <div key={index} className="card text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 mb-4 gradient-bg rounded-full">
                <Icon className="text-white" size={32} />
              </div>
              <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
              <p className="text-gray-600 dark:text-gray-300">{feature.description}</p>
            </div>
          );
        })}
      </motion.div>

      {/* Detection Systems */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={fadeIn}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="grid md:grid-cols-2 gap-8 mb-16"
      >
        {/* Brain Detection Card */}
        <Link to="/brain" className="group">
          <div className="card hover:scale-105 transition-transform duration-300 cursor-pointer border-2 border-transparent hover:border-primary dark:hover:border-primary-dark">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Brain className="text-blue-600" size={28} />
                </div>
                <div>
                  <h3 className="text-2xl font-bold">Brain Tumor Detection</h3>
                  <p className="text-sm text-gray-500">MRI Scan Analysis</p>
                </div>
              </div>
              <ArrowRight className="text-primary group-hover:translate-x-2 transition-transform" size={24} />
            </div>
            <div className="space-y-2 mb-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Model Accuracy</span>
                <span className="font-bold text-primary">93.29%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-gradient-to-r from-blue-400 to-blue-600 h-2 rounded-full" style={{ width: '93%' }}></div>
              </div>
            </div>
            <p className="text-gray-600 dark:text-gray-300">
              Detect Glioma, Meningioma, Pituitary tumors from MRI scans with advanced CNN architecture
            </p>
            <div className="mt-4 flex flex-wrap gap-2">
              <span className="px-3 py-1 bg-blue-100 text-blue-600 rounded-full text-sm">Glioma</span>
              <span className="px-3 py-1 bg-purple-100 text-purple-600 rounded-full text-sm">Meningioma</span>
              <span className="px-3 py-1 bg-green-100 text-green-600 rounded-full text-sm">Pituitary</span>
            </div>
          </div>
        </Link>

        {/* Lung Detection Card */}
        <Link to="/lung" className="group">
          <div className="card hover:scale-105 transition-transform duration-300 cursor-pointer border-2 border-transparent hover:border-secondary">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Waves className="text-purple-600" size={28} />
                </div>
                <div>
                  <h3 className="text-2xl font-bold">Lung Cancer Detection</h3>
                  <p className="text-sm text-gray-500">CT Scan Analysis</p>
                </div>
              </div>
              <ArrowRight className="text-secondary group-hover:translate-x-2 transition-transform" size={24} />
            </div>
            <div className="space-y-2 mb-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Cancer Detection Recall</span>
                <span className="font-bold text-secondary">99.36%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-gradient-to-r from-purple-400 to-purple-600 h-2 rounded-full" style={{ width: '99%' }}></div>
              </div>
            </div>
            <p className="text-gray-600 dark:text-gray-300">
              Analyze CT scans to classify Normal, Benign, and Malignant cases using ResNet50 transfer learning
            </p>
            <div className="mt-4 flex flex-wrap gap-2">
              <span className="px-3 py-1 bg-green-100 text-green-600 rounded-full text-sm">Normal</span>
              <span className="px-3 py-1 bg-yellow-100 text-yellow-600 rounded-full text-sm">Benign</span>
              <span className="px-3 py-1 bg-red-100 text-red-600 rounded-full text-sm">Malignant</span>
            </div>
          </div>
        </Link>
      </motion.div>

      {/* Disclaimer */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={fadeIn}
        transition={{ duration: 0.6, delay: 0.6 }}
        className="bg-yellow-50 dark:bg-yellow-900 dark:bg-opacity-20 border-l-4 border-yellow-400 p-6 rounded-lg mb-8"
      >
        <h3 className="text-lg font-bold text-yellow-800 dark:text-yellow-300 mb-2">⚠️ Medical Disclaimer</h3>
        <p className="text-yellow-700 dark:text-yellow-400">
          This tool is for <strong>educational and research purposes only</strong>. It is NOT intended for clinical diagnosis or treatment decisions. 
          Always consult qualified healthcare professionals for medical advice and diagnosis. The AI models provide predictions based on training data 
          and should be used as a supplementary tool alongside professional medical evaluation.
        </p>
      </motion.div>
    </div>
  );
};

export default Home;
