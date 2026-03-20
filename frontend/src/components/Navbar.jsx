import { Link, useLocation } from 'react-router-dom';
import { Activity, Brain, History as HistoryIcon, Info, Moon, Sun, Settings } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const Navbar = ({ stats }) => {
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();

  const isActive = (path) => location.pathname === path;

  const navItems = [
    { path: '/', label: 'Home', icon: Activity },
    { path: '/brain', label: 'Brain', icon: Brain },
    { path: '/lung', label: 'Lung', icon: Activity },
    { path: '/history', label: 'History', icon: HistoryIcon },
    { path: '/about', label: 'About', icon: Info },
  ];

  return (
    <nav className="bg-white dark:bg-gray-800 shadow-lg sticky top-0 z-50 transition-colors duration-300">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 gradient-bg rounded-lg flex items-center justify-center">
              <Activity className="text-white" size={24} />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
              Cancer Detection AI
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                    isActive(item.path)
                      ? 'bg-gradient-to-r from-primary to-secondary text-white'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                  }`}
                >
                  <Icon size={18} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>

          {/* Right Side Controls */}
          <div className="flex items-center space-x-4">
            {/* Stats Badge */}
            <div className="hidden lg:flex items-center space-x-4 bg-gray-100 dark:bg-gray-700 px-4 py-2 rounded-lg">
              <div className="text-center">
                <div className="text-sm text-gray-600 dark:text-gray-400">Total Scans</div>
                <div className="text-xl font-bold text-primary">{stats.total_scans}</div>
              </div>
              <div className="h-8 w-px bg-gray-300 dark:bg-gray-600"></div>
              <div className="text-center">
                <div className="text-sm text-gray-600 dark:text-gray-400">Brain</div>
                <div className="text-lg font-semibold text-blue-600">{stats.brain_scans}</div>
              </div>
              <div className="text-center">
                <div className="text-sm text-gray-600 dark:text-gray-400">Lung</div>
                <div className="text-lg font-semibold text-purple-600">{stats.lung_scans}</div>
              </div>
            </div>

            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            >
              {theme === 'dark' ? (
                <Sun className="text-yellow-500" size={20} />
              ) : (
                <Moon className="text-gray-700" size={20} />
              )}
            </button>

            {/* Settings Button */}
            <Link
              to="/settings"
              className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              title="Settings"
            >
              <Settings className="text-gray-700 dark:text-gray-300" size={20} />
            </Link>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden flex justify-around pb-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex flex-col items-center p-2 rounded-lg ${
                  isActive(item.path)
                    ? 'text-primary'
                    : 'text-gray-600 dark:text-gray-400'
                }`}
              >
                <Icon size={20} />
                <span className="text-xs mt-1">{item.label}</span>
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
