import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Loader2, AlertCircle, Filter, ArrowUpDown } from 'lucide-react';
import { searchApi } from '../api';
import ProductCard from '../components/ProductCard';
import type { SearchResult, Product, SortOption } from '../types';
import { POLLING_INTERVAL, MAX_POLLING_ATTEMPTS } from '../config';

export default function SearchResultsPage() {
  const [searchParams] = useSearchParams();
  const taskId = searchParams.get('task_id');
  const query = searchParams.get('query') || 'Image Search';

  const [searchResult, setSearchResult] = useState<SearchResult | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pollCount, setPollCount] = useState(0);
  
  // Filters and sorting
  const [sortBy, setSortBy] = useState<SortOption>('price_asc');
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);

  useEffect(() => {
    if (!taskId) {
      setError('No search task ID provided');
      setIsLoading(false);
      return;
    }

    let intervalId: NodeJS.Timeout;

    const pollSearchStatus = async () => {
      try {
        const result = await searchApi.getSearchStatus(taskId);
        setSearchResult(result);

        if (result.status === 'completed' && result.products) {
          setProducts(result.products);
          setIsLoading(false);
          clearInterval(intervalId);
        } else if (result.status === 'failed') {
          setError('Search failed. Please try again.');
          setIsLoading(false);
          clearInterval(intervalId);
        } else {
          setPollCount((prev) => prev + 1);
          
          if (pollCount >= MAX_POLLING_ATTEMPTS) {
            setError('Search timed out. Please try again.');
            setIsLoading(false);
            clearInterval(intervalId);
          }
        }
      } catch (err) {
        console.error('Error polling search status:', err);
        setError('Failed to fetch search results');
        setIsLoading(false);
        clearInterval(intervalId);
      }
    };

    // Initial poll
    pollSearchStatus();

    // Set up polling interval
    intervalId = setInterval(pollSearchStatus, POLLING_INTERVAL);

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [taskId, pollCount]);

  // Sort products
  const sortedProducts = [...products].sort((a, b) => {
    const aPrice = a.lowest_price?.price || Infinity;
    const bPrice = b.lowest_price?.price || Infinity;

    switch (sortBy) {
      case 'price_asc':
        return aPrice - bPrice;
      case 'price_desc':
        return bPrice - aPrice;
      case 'name':
        return a.name.localeCompare(b.name);
      default:
        return 0;
    }
  });

  // Filter products by platform
  const filteredProducts = sortedProducts.filter((product) => {
    if (selectedPlatforms.length === 0) return true;
    return product.listings.some((listing) =>
      selectedPlatforms.includes(listing.platform.name.toLowerCase())
    );
  });

  if (error) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto text-center animate-fade-in">
          <div className="bg-red-50 rounded-3xl p-12 border-2 border-red-200">
            <AlertCircle className="w-20 h-20 text-red-500 mx-auto mb-6" />
            <h2 className="text-3xl font-bold mb-4 text-gray-900">Search Failed</h2>
            <p className="text-lg text-gray-600">{error}</p>
            <a
              href="/"
              className="inline-block mt-6 px-8 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl font-semibold hover:shadow-lg transition-all"
            >
              Try Again
            </a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12 animate-fade-in">
      {/* Header */}
      <div className="mb-10">
        <h1 className="text-4xl md:text-5xl font-extrabold mb-3 text-gray-900">Search Results</h1>
        <p className="text-xl text-gray-600">
          Searching for: <span className="font-bold text-blue-600">{query}</span>
        </p>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="text-center py-20 animate-fade-in">
          <div className="inline-block relative mb-8">
            <Loader2 className="w-20 h-20 animate-spin text-blue-600" />
            <div className="absolute inset-0 w-20 h-20 rounded-full bg-blue-100 animate-pulse-slow opacity-20"></div>
          </div>
          <h2 className="text-2xl font-bold mb-4 text-gray-900">Searching platforms...</h2>
          <p className="text-gray-600 mb-6">Comparing prices across multiple e-commerce sites</p>
          
          {searchResult?.progress && (
            <div className="max-w-md mx-auto">
              <div className="bg-gray-200 rounded-full h-3 mb-3 overflow-hidden shadow-inner">
                <div
                  className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-500 shadow-sm"
                  style={{ width: `${searchResult.progress.percentage}%` }}
                />
              </div>
              <p className="text-sm font-semibold text-gray-700">
                {searchResult.progress.completed} of {searchResult.progress.total} platforms completed
              </p>
            </div>
          )}
        </div>
      )}

      {/* Results */}
      {!isLoading && filteredProducts.length > 0 && (
        <>
          {/* Filters and Sorting */}
          <div className="flex flex-wrap gap-6 mb-8 p-6 bg-white rounded-2xl shadow-md border border-gray-100">
            <div className="flex items-center flex-wrap gap-4">
              <div className="flex items-center space-x-2 text-gray-900">
                <Filter className="w-5 h-5" />
                <span className="font-bold">Filter:</span>
              </div>
              {['jumia', 'kilimall', 'alibaba', 'amazon', 'ebay'].map((platform) => (
                <label key={platform} className="flex items-center space-x-2 cursor-pointer group">
                  <input
                    type="checkbox"
                    checked={selectedPlatforms.includes(platform)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedPlatforms([...selectedPlatforms, platform]);
                      } else {
                        setSelectedPlatforms(selectedPlatforms.filter((p) => p !== platform));
                      }
                    }}
                    className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-2 focus:ring-blue-500"
                  />
                  <span className="capitalize text-sm font-medium text-gray-700 group-hover:text-blue-600 transition-colors">
                    {platform}
                  </span>
                </label>
              ))}
            </div>

            <div className="flex items-center space-x-3 ml-auto">
              <div className="flex items-center space-x-2 text-gray-900">
                <ArrowUpDown className="w-5 h-5" />
                <span className="font-bold">Sort:</span>
              </div>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as SortOption)}
                className="px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none font-medium text-gray-700 bg-white cursor-pointer hover:border-gray-300 transition-colors"
              >
                <option value="price_asc">Price: Low to High</option>
                <option value="price_desc">Price: High to Low</option>
                <option value="name">Name: A to Z</option>
              </select>
            </div>
          </div>

          {/* Product Grid */}
          <div className="space-y-8">
            {filteredProducts.map((product) => (
              <div key={product.id} className="animate-slide-in">
                <div className="flex items-center justify-between mb-5">
                  <h3 className="text-2xl font-bold text-gray-900">{product.name}</h3>
                  <span className="badge badge-blue text-sm">
                    {product.listings.filter((l) => l.availability).length} available
                  </span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {product.listings
                    .filter((listing) => listing.availability)
                    .sort((a, b) => a.total_price - b.total_price)
                    .map((listing, index) => (
                      <ProductCard
                        key={listing.id}
                        listing={listing}
                        highlightBest={index === 0}
                      />
                    ))}
                </div>
              </div>
            ))}
          </div>

          {/* Results Summary */}
          <div className="mt-12 text-center">
            <div className="inline-block bg-gradient-to-r from-blue-50 to-purple-50 px-8 py-4 rounded-2xl border border-blue-200">
              <p className="text-lg font-semibold text-gray-900">
                Found <span className="text-blue-600 text-2xl font-bold">{filteredProducts.length}</span> products across multiple platforms
              </p>
            </div>
          </div>
        </>
      )}

      {/* No Results */}
      {!isLoading && filteredProducts.length === 0 && (
        <div className="text-center py-20 animate-fade-in">
          <div className="bg-gray-50 rounded-3xl p-12 border-2 border-gray-200 max-w-2xl mx-auto">
            <AlertCircle className="w-20 h-20 text-gray-400 mx-auto mb-6" />
            <h2 className="text-3xl font-bold mb-4 text-gray-900">No Results Found</h2>
            <p className="text-lg text-gray-600 mb-6">
              Try adjusting your search query or filters to see more results
            </p>
            <a
              href="/"
              className="inline-block px-8 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl font-semibold hover:shadow-lg transition-all"
            >
              New Search
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
