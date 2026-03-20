import { Brain, Waves, Shield, Target, Zap, Heart, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';

const About = () => {
  const technologies = [
    { name: 'TensorFlow', description: 'Deep learning framework' },
    { name: 'React', description: 'Modern UI framework' },
    { name: 'Flask', description: 'Python backend API' },
    { name: 'CNN/ResNet50', description: 'Neural network architectures' }
  ];

  const features = [
    {
      icon: Brain,
      title: 'Brain Tumor Detection',
      description: 'CNN model trained on 3,000+ MRI scans',
      accuracy: '93.29%',
      classes: ['Glioma', 'Meningioma', 'Pituitary', 'No Tumor']
    },
    {
      icon: Waves,
      title: 'Lung Cancer Detection',
      description: 'ResNet50 transfer learning on 1,933 CT scans',
      accuracy: '99.36% Recall',
      classes: ['Normal', 'Benign', 'Malignant']
    }
  ];

  const principles = [
    {
      icon: Shield,
      title: 'Privacy First',
      description: 'Images processed locally, not stored permanently'
    },
    {
      icon: Target,
      title: 'High Accuracy',
      description: 'State-of-the-art models with clinical-grade performance'
    },
    {
      icon: Zap,
      title: 'Fast Analysis',
      description: 'Real-time predictions in seconds'
    },
    {
      icon: Heart,
      title: 'Patient-Centric',
      description: 'Designed to assist healthcare professionals'
    }
  ];

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
          About This Platform
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Advanced AI-powered medical imaging analysis for cancer detection
        </p>
      </motion.div>

      {/* Mission Statement */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card mb-12 gradient-bg text-white"
      >
        <h2 className="text-2xl font-bold mb-4">Our Mission</h2>
        <p className="text-lg opacity-95 leading-relaxed">
          To democratize access to advanced medical imaging analysis through artificial intelligence, 
          supporting healthcare professionals in early cancer detection and improving patient outcomes 
          worldwide. This platform combines cutting-edge deep learning with intuitive user experience 
          to make AI-assisted diagnosis accessible and reliable.
        </p>
      </motion.div>

      {/* Detection Models */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="mb-12"
      >
        <h2 className="text-3xl font-bold mb-6 text-center">Detection Capabilities</h2>
        <div className="grid md:grid-cols-2 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div key={index} className="card border-2 border-gray-200">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-12 h-12 gradient-bg rounded-lg flex items-center justify-center">
                    <Icon className="text-white" size={24} />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold">{feature.title}</h3>
                    <p className="text-sm text-primary font-semibold">{feature.accuracy} Accuracy</p>
                  </div>
                </div>
                <p className="text-gray-600 mb-4">{feature.description}</p>
                <div className="flex flex-wrap gap-2">
                  {feature.classes.map((cls, i) => (
                    <span key={i} className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                      {cls}
                    </span>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </motion.div>

      {/* Core Principles */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="mb-12"
      >
        <h2 className="text-3xl font-bold mb-6 text-center">Core Principles</h2>
        <div className="grid md:grid-cols-4 gap-6">
          {principles.map((principle, index) => {
            const Icon = principle.icon;
            return (
              <div key={index} className="card text-center">
                <div className="w-12 h-12 mx-auto mb-3 gradient-bg rounded-full flex items-center justify-center">
                  <Icon className="text-white" size={24} />
                </div>
                <h3 className="font-bold mb-2">{principle.title}</h3>
                <p className="text-sm text-gray-600">{principle.description}</p>
              </div>
            );
          })}
        </div>
      </motion.div>

      {/* Technology Stack */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="card mb-12"
      >
        <h2 className="text-2xl font-bold mb-6">Technology Stack</h2>
        <div className="grid md:grid-cols-4 gap-4">
          {technologies.map((tech, index) => (
            <div key={index} className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="font-bold text-primary mb-1">{tech.name}</div>
              <div className="text-sm text-gray-600">{tech.description}</div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* How It Works */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="card mb-12"
      >
        <h2 className="text-2xl font-bold mb-6">How It Works</h2>
        <div className="space-y-4">
          <div className="flex items-start space-x-4">
            <div className="w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center font-bold flex-shrink-0">
              1
            </div>
            <div>
              <h3 className="font-bold mb-1">Upload Medical Image</h3>
              <p className="text-gray-600">Upload MRI (brain) or CT (lung) scan in standard image formats</p>
            </div>
          </div>
          <div className="flex items-start space-x-4">
            <div className="w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center font-bold flex-shrink-0">
              2
            </div>
            <div>
              <h3 className="font-bold mb-1">AI Processing</h3>
              <p className="text-gray-600">Image is preprocessed and analyzed by trained neural networks</p>
            </div>
          </div>
          <div className="flex items-start space-x-4">
            <div className="w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center font-bold flex-shrink-0">
              3
            </div>
            <div>
              <h3 className="font-bold mb-1">Results & Visualization</h3>
              <p className="text-gray-600">Get instant classification with confidence scores and heatmap visualization</p>
            </div>
          </div>
          <div className="flex items-start space-x-4">
            <div className="w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center font-bold flex-shrink-0">
              4
            </div>
            <div>
              <h3 className="font-bold mb-1">Clinical Review</h3>
              <p className="text-gray-600">Healthcare professional reviews AI suggestion alongside clinical evaluation</p>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Disclaimer */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="card bg-yellow-50 border-2 border-yellow-300"
      >
        <div className="flex items-start space-x-3">
          <AlertCircle className="text-yellow-600 flex-shrink-0 mt-1" size={24} />
          <div>
            <h3 className="text-lg font-bold text-yellow-900 mb-2">Important Medical Disclaimer</h3>
            <div className="text-yellow-800 space-y-2">
              <p>
                This platform is designed for <strong>educational and research purposes only</strong>. 
                It is NOT a substitute for professional medical advice, diagnosis, or treatment.
              </p>
              <ul className="list-disc list-inside space-y-1 ml-4">
                <li>Always consult qualified healthcare professionals for medical decisions</li>
                <li>AI predictions should be validated by trained radiologists</li>
                <li>This tool has not received regulatory approval for clinical use</li>
                <li>Results should be interpreted within full clinical context</li>
                <li>Do not use for emergency medical situations</li>
              </ul>
              <p className="font-semibold mt-3">
                If you have medical concerns, seek immediate professional medical attention.
              </p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default About;
