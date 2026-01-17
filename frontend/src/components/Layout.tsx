import { ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { Search, TrendingUp, BarChart3 } from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center space-x-3 group">
              <div className="bg-gradient-to-br from-blue-600 to-blue-700 p-2 rounded-lg group-hover:scale-105 transition-transform">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
                PriceCompare
              </span>
            </Link>

            <nav className="flex items-center space-x-1">
              <Link
                to="/"
                className="flex items-center space-x-2 px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 hover:text-blue-600 transition-colors font-medium"
              >
                <Search className="w-5 h-5" />
                <span>Search</span>
              </Link>
              <Link
                to="/compare"
                className="flex items-center space-x-2 px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 hover:text-blue-600 transition-colors font-medium"
              >
                <BarChart3 className="w-5 h-5" />
                <span>Compare</span>
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white mt-auto">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="bg-blue-600 p-2 rounded-lg">
                  <TrendingUp className="w-5 h-5" />
                </div>
                <h3 className="text-xl font-bold">PriceCompare</h3>
              </div>
              <p className="text-gray-400 leading-relaxed">
                Compare prices across Jumia, Kilimall, Alibaba, Amazon, and eBay to find the best deals.
              </p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Features</h3>
              <ul className="space-y-2 text-gray-400">
                <li className="hover:text-white transition-colors cursor-pointer">• Text-based product search</li>
                <li className="hover:text-white transition-colors cursor-pointer">• Image recognition search</li>
                <li className="hover:text-white transition-colors cursor-pointer">• Price history tracking</li>
                <li className="hover:text-white transition-colors cursor-pointer">• Real-time comparison</li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Supported Platforms</h3>
              <div className="flex flex-wrap gap-2">
                <span className="badge bg-orange-100 text-orange-800 px-3 py-1">Jumia</span>
                <span className="badge bg-red-100 text-red-800 px-3 py-1">Kilimall</span>
                <span className="badge bg-orange-100 text-orange-800 px-3 py-1">Alibaba</span>
                <span className="badge bg-yellow-100 text-yellow-800 px-3 py-1">Amazon</span>
                <span className="badge bg-red-100 text-red-800 px-3 py-1">eBay</span>
              </div>
            </div>
          </div>
          
          <div className="mt-8 pt-8 border-t border-gray-800 text-center">
            <p className="text-gray-400">
              &copy; 2026 PriceCompare. All rights reserved. Built with ❤️ for smart shoppers.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
