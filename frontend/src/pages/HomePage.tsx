import SearchBar from '../components/SearchBar';
import { ShoppingCart, Zap, TrendingUp, Shield, ArrowRight, Sparkles } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="animate-fade-in">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-50 via-white to-blue-50 py-20 overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-blue-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse-slow"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-purple-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse-slow" style={{ animationDelay: '1s' }}></div>
        
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center mb-12 max-w-4xl mx-auto">
            <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-6 animate-fade-in">
              <Sparkles className="w-4 h-4" />
              <span>AI-Powered Price Comparison</span>
            </div>
            
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold text-gray-900 mb-6 leading-tight">
              Find the Best Deals
              <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Across Multiple Platforms
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Compare prices from <span className="font-semibold text-gray-900">Jumia, Kilimall, Alibaba, Amazon, and eBay</span> instantly.
              Use text search or upload an image to find the best deals.
            </p>
          </div>

          <SearchBar />

          {/* Trust badges */}
          <div className="mt-12 flex flex-wrap justify-center items-center gap-6 text-sm text-gray-600">
            <div className="flex items-center space-x-2">
              <Shield className="w-5 h-5 text-green-600" />
              <span>Secure & Safe</span>
            </div>
            <div className="flex items-center space-x-2">
              <Zap className="w-5 h-5 text-yellow-600" />
              <span>Instant Results</span>
            </div>
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-5 h-5 text-blue-600" />
              <span>Live Price Tracking</span>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Why Choose PriceCompare?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Save time and money with our powerful comparison tools
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="group text-center p-8 rounded-2xl bg-gradient-to-br from-blue-50 to-white hover:shadow-xl transition-all duration-300 border border-gray-100 hover:border-blue-200">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <ShoppingCart className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-gray-900">Multiple Platforms</h3>
              <p className="text-gray-600 leading-relaxed">
                Search across 5 major e-commerce platforms simultaneously to find the best prices
              </p>
            </div>

            <div className="group text-center p-8 rounded-2xl bg-gradient-to-br from-yellow-50 to-white hover:shadow-xl transition-all duration-300 border border-gray-100 hover:border-yellow-200">
              <div className="w-16 h-16 bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <Zap className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-gray-900">Real-time Results</h3>
              <p className="text-gray-600 leading-relaxed">
                Get live price updates as results come in from each platform in seconds
              </p>
            </div>

            <div className="group text-center p-8 rounded-2xl bg-gradient-to-br from-green-50 to-white hover:shadow-xl transition-all duration-300 border border-gray-100 hover:border-green-200">
              <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <TrendingUp className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-gray-900">Price History</h3>
              <p className="text-gray-600 leading-relaxed">
                Track price changes over time to find the best time to buy and save more
              </p>
            </div>

            <div className="group text-center p-8 rounded-2xl bg-gradient-to-br from-purple-50 to-white hover:shadow-xl transition-all duration-300 border border-gray-100 hover:border-purple-200">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <Shield className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-gray-900">AI-Powered</h3>
              <p className="text-gray-600 leading-relaxed">
                Use image recognition to search by uploading product photos with our AI
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Start saving money in three simple steps
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="relative text-center">
              <div className="relative">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-600 to-blue-700 text-white rounded-2xl flex items-center justify-center mx-auto mb-6 text-3xl font-bold shadow-xl">
                  1
                </div>
                {/* Arrow */}
                <div className="hidden md:block absolute top-10 left-full w-full">
                  <ArrowRight className="w-8 h-8 text-blue-300 mx-auto" />
                </div>
              </div>
              <h3 className="text-2xl font-bold mb-3 text-gray-900">Search</h3>
              <p className="text-gray-600 leading-relaxed text-lg">
                Enter a product name or upload an image of what you're looking for
              </p>
            </div>

            <div className="relative text-center">
              <div className="relative">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-600 to-blue-700 text-white rounded-2xl flex items-center justify-center mx-auto mb-6 text-3xl font-bold shadow-xl">
                  2
                </div>
                {/* Arrow */}
                <div className="hidden md:block absolute top-10 left-full w-full">
                  <ArrowRight className="w-8 h-8 text-blue-300 mx-auto" />
                </div>
              </div>
              <h3 className="text-2xl font-bold mb-3 text-gray-900">Compare</h3>
              <p className="text-gray-600 leading-relaxed text-lg">
                See prices from all platforms side by side with ratings and reviews
              </p>
            </div>

            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-600 to-blue-700 text-white rounded-2xl flex items-center justify-center mx-auto mb-6 text-3xl font-bold shadow-xl">
                3
              </div>
              <h3 className="text-2xl font-bold mb-3 text-gray-900">Save</h3>
              <p className="text-gray-600 leading-relaxed text-lg">
                Click through to the best deal and save money on your purchase
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Supported Platforms */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Supported Platforms
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              We search across the most popular e-commerce platforms
            </p>
          </div>

          <div className="flex flex-wrap justify-center items-center gap-12">
            <div className="text-center group cursor-pointer">
              <div className="bg-gradient-to-br from-orange-500 to-orange-600 text-white px-8 py-4 rounded-2xl text-4xl font-bold shadow-lg group-hover:scale-105 transition-transform">
                Jumia
              </div>
            </div>
            <div className="text-center group cursor-pointer">
              <div className="bg-gradient-to-br from-red-500 to-red-600 text-white px-8 py-4 rounded-2xl text-4xl font-bold shadow-lg group-hover:scale-105 transition-transform">
                Kilimall
              </div>
            </div>
            <div className="text-center group cursor-pointer">
              <div className="bg-gradient-to-br from-orange-600 to-orange-700 text-white px-8 py-4 rounded-2xl text-4xl font-bold shadow-lg group-hover:scale-105 transition-transform">
                Alibaba
              </div>
            </div>
            <div className="text-center group cursor-pointer">
              <div className="bg-gradient-to-br from-yellow-500 to-yellow-600 text-white px-8 py-4 rounded-2xl text-4xl font-bold shadow-lg group-hover:scale-105 transition-transform">
                Amazon
              </div>
            </div>
            <div className="text-center group cursor-pointer">
              <div className="bg-gradient-to-br from-red-600 to-red-700 text-white px-8 py-4 rounded-2xl text-4xl font-bold shadow-lg group-hover:scale-105 transition-transform">
                eBay
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
