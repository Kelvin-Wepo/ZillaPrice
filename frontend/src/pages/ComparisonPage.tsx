import { useState } from 'react';
import { useQuery } from 'react-query';
import { Search, Loader2, TrendingDown } from 'lucide-react';
import { productApi } from '../api';
import ProductCard from '../components/ProductCard';
import type { ComparisonData } from '../types';
import { formatPrice } from '../utils';

export default function ComparisonPage() {
  const [query, setQuery] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  const { data, isLoading, error } = useQuery(
    ['compare', searchQuery],
    () => productApi.compareProducts(undefined, searchQuery),
    {
      enabled: !!searchQuery,
    }
  );

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      setSearchQuery(query);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Compare Products</h1>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="max-w-2xl mb-8">
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter product name to compare prices"
            className="input pr-12"
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-primary-600 hover:text-primary-700"
          >
            <Search className="w-6 h-6" />
          </button>
        </div>
      </form>

      {/* Loading State */}
      {isLoading && (
        <div className="text-center py-16">
          <Loader2 className="w-12 h-12 animate-spin text-primary-600 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">Loading comparison data...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="text-center py-16">
          <p className="text-red-600">Failed to load comparison data</p>
        </div>
      )}

      {/* Results */}
      {data && data.comparisons.length > 0 && (
        <div className="space-y-12">
          {data.comparisons.map((comparison: ComparisonData) => (
            <div key={comparison.product.id} className="card">
              {/* Product Header */}
              <div className="mb-6">
                <h2 className="text-2xl font-bold mb-2">{comparison.product.name}</h2>
                {comparison.product.brand && (
                  <p className="text-gray-600 dark:text-gray-400">
                    Brand: {comparison.product.brand}
                  </p>
                )}
              </div>

              {/* Price Stats */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                <div className="card bg-green-50 dark:bg-green-900/20">
                  <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Lowest Price</div>
                  <div className="text-2xl font-bold text-green-600">
                    {formatPrice(comparison.price_stats.min)}
                  </div>
                </div>

                <div className="card bg-red-50 dark:bg-red-900/20">
                  <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Highest Price</div>
                  <div className="text-2xl font-bold text-red-600">
                    {formatPrice(comparison.price_stats.max)}
                  </div>
                </div>

                <div className="card bg-blue-50 dark:bg-blue-900/20">
                  <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Average Price</div>
                  <div className="text-2xl font-bold text-blue-600">
                    {formatPrice(comparison.price_stats.avg)}
                  </div>
                </div>

                <div className="card bg-purple-50 dark:bg-purple-900/20">
                  <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Listings</div>
                  <div className="text-2xl font-bold text-purple-600">
                    {comparison.price_stats.count}
                  </div>
                </div>
              </div>

              {/* Best Deal */}
              {comparison.best_deal && (
                <div className="card bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 mb-6">
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center space-x-2 mb-2">
                        <TrendingDown className="w-5 h-5 text-green-600" />
                        <h3 className="text-lg font-semibold">Best Deal</h3>
                      </div>
                      <p className="text-gray-600 dark:text-gray-400 mb-2">
                        Platform: <span className="font-semibold capitalize">{comparison.best_deal.platform}</span>
                      </p>
                      <p className="text-3xl font-bold text-green-600 mb-2">
                        {formatPrice(comparison.best_deal.total_price)}
                      </p>
                      {comparison.best_deal.savings > 0 && (
                        <p className="text-sm text-green-600 font-medium">
                          Save {formatPrice(comparison.best_deal.savings)} compared to highest price
                        </p>
                      )}
                    </div>
                    <a
                      href={comparison.best_deal.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn btn-primary"
                    >
                      View Deal
                    </a>
                  </div>
                </div>
              )}

              {/* Platform Listings */}
              <div className="space-y-6">
                <h3 className="text-xl font-semibold">Available on:</h3>
                {Object.entries(comparison.platform_prices).map(([platform, listings]) => (
                  <div key={platform}>
                    <h4 className="text-lg font-semibold capitalize mb-3">{platform}</h4>
                    <div className="grid grid-cols-1 gap-4">
                      {listings.map((listing: any) => {
                        // Convert to ProductListing format for ProductCard
                        const listingData = {
                          id: listing.listing_id,
                          platform: { name: platform },
                          title: listing.title,
                          url: listing.url,
                          image_url: comparison.product.image_url || '',
                          price: listing.price,
                          currency: listing.currency,
                          total_price: listing.total_price,
                          rating: listing.rating,
                          review_count: listing.review_count,
                          seller_name: listing.seller,
                          availability: true,
                          scraped_at: '',
                        };

                        return (
                          <ProductCard
                            key={listing.listing_id}
                            listing={listingData as any}
                            showPlatform={false}
                          />
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* No Results */}
      {data && data.comparisons.length === 0 && searchQuery && (
        <div className="text-center py-16">
          <p className="text-gray-600 dark:text-gray-400">
            No products found for "{searchQuery}"
          </p>
        </div>
      )}
    </div>
  );
}
