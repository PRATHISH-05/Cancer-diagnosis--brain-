import { Settings as SettingsIcon, Palette, Type, Moon, Sun, Check } from 'lucide-react';
import { motion } from 'framer-motion';
import { useTheme } from '../context/ThemeContext';

const Settings = () => {
  const { theme, setTheme, accentColor, setAccentColor, fontSize, setFontSize } = useTheme();

  const accentColors = [
    { id: 'purple', name: 'Purple', from: '#667eea', to: '#764ba2' },
    { id: 'blue', name: 'Blue', from: '#3b82f6', to: '#1d4ed8' },
    { id: 'green', name: 'Green', from: '#10b981', to: '#059669' },
    { id: 'pink', name: 'Pink', from: '#ec4899', to: '#be185d' },
  ];

  const fontSizes = [
    { id: 'small', name: 'Small', size: '14px' },
    { id: 'medium', name: 'Medium', size: '16px' },
    { id: 'large', name: 'Large', size: '18px' },
  ];

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <div className="inline-flex items-center justify-center w-16 h-16 mb-4 gradient-bg rounded-full">
          <SettingsIcon className="text-white" size={32} />
        </div>
        <h1 className="text-4xl font-bold mb-3">Settings & Personalization</h1>
        <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Customize your experience with themes, colors, and display preferences
        </p>
      </motion.div>

      {/* Theme Selection */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card mb-6"
      >
        <h2 className="text-2xl font-bold mb-4 flex items-center">
          {theme === 'dark' ? <Moon className="mr-2" size={24} /> : <Sun className="mr-2" size={24} />}
          Theme Mode
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-4">
          Choose between light and dark mode for comfortable viewing
        </p>
        <div className="grid grid-cols-2 gap-4">
          <button
            onClick={() => setTheme('light')}
            className={`p-6 rounded-lg border-2 transition-all duration-200 ${
              theme === 'light'
                ? 'border-primary bg-primary bg-opacity-10'
                : 'border-gray-300 dark:border-gray-600 hover:border-primary'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <Sun size={32} className="text-yellow-500" />
              {theme === 'light' && <Check size={24} className="text-primary" />}
            </div>
            <h3 className="text-lg font-bold">Light Mode</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">Bright and clean interface</p>
          </button>

          <button
            onClick={() => setTheme('dark')}
            className={`p-6 rounded-lg border-2 transition-all duration-200 ${
              theme === 'dark'
                ? 'border-primary bg-primary bg-opacity-10'
                : 'border-gray-300 dark:border-gray-600 hover:border-primary'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <Moon size={32} className="text-purple-500" />
              {theme === 'dark' && <Check size={24} className="text-primary" />}
            </div>
            <h3 className="text-lg font-bold">Dark Mode</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">Easy on the eyes at night</p>
          </button>
        </div>
      </motion.div>

      {/* Accent Color */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="card mb-6"
      >
        <h2 className="text-2xl font-bold mb-4 flex items-center">
          <Palette className="mr-2" size={24} />
          Accent Color
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-4">
          Select your preferred accent color for the interface
        </p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {accentColors.map((color) => (
            <button
              key={color.id}
              onClick={() => setAccentColor(color.id)}
              className={`p-4 rounded-lg border-2 transition-all duration-200 ${
                accentColor === color.id
                  ? 'border-primary scale-105'
                  : 'border-gray-300 dark:border-gray-600 hover:scale-105'
              }`}
            >
              <div
                className="w-full h-16 rounded-lg mb-2"
                style={{
                  background: `linear-gradient(135deg, ${color.from}, ${color.to})`
                }}
              ></div>
              <div className="flex items-center justify-between">
                <span className="font-medium">{color.name}</span>
                {accentColor === color.id && <Check size={20} className="text-primary" />}
              </div>
            </button>
          ))}
        </div>
      </motion.div>

      {/* Font Size */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="card mb-6"
      >
        <h2 className="text-2xl font-bold mb-4 flex items-center">
          <Type className="mr-2" size={24} />
          Font Size
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-4">
          Adjust text size for better readability
        </p>
        <div className="grid grid-cols-3 gap-4">
          {fontSizes.map((size) => (
            <button
              key={size.id}
              onClick={() => setFontSize(size.id)}
              className={`p-6 rounded-lg border-2 transition-all duration-200 ${
                fontSize === size.id
                  ? 'border-primary bg-primary bg-opacity-10'
                  : 'border-gray-300 dark:border-gray-600 hover:border-primary'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span style={{ fontSize: size.size }} className="font-bold">Aa</span>
                {fontSize === size.id && <Check size={20} className="text-primary" />}
              </div>
              <h3 className="text-lg font-bold">{size.name}</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">{size.size}</p>
            </button>
          ))}
        </div>
      </motion.div>

      {/* Preview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="card bg-gray-50 dark:bg-gray-800"
      >
        <h2 className="text-2xl font-bold mb-4">Preview</h2>
        <div className="space-y-4">
          <div className="p-4 bg-white dark:bg-gray-700 rounded-lg">
            <h3 className="text-xl font-bold mb-2 gradient-text">Sample Heading</h3>
            <p className="text-gray-600 dark:text-gray-300">
              This is how regular text will appear with your current settings. 
              The accent colors are applied to buttons and highlights throughout the application.
            </p>
          </div>
          <button className="btn-primary">
            Sample Button
          </button>
        </div>
      </motion.div>

      {/* Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="mt-6 p-4 bg-blue-50 dark:bg-blue-900 dark:bg-opacity-20 rounded-lg text-center"
      >
        <p className="text-sm text-blue-800 dark:text-blue-300">
          💡 Your preferences are saved automatically and will persist across sessions
        </p>
      </motion.div>
    </div>
  );
};

export default Settings;
