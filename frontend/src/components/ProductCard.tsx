import { ExternalLink, Star, TrendingDown } from 'lucide-react';
import type { ProductListing } from '../types';
import { formatPrice, getImageUrl, getPlatformColor, truncateText } from '../utils';

interface ProductCardProps {
  listing: ProductListing;
  showPlatform?: boolean;
  highlightBest?: boolean;
}

export default function ProductCard({ listing, showPlatform = true, highlightBest = false }: ProductCardProps) {
  const platformColor = getPlatformColor(listing.platform.name);

  return (
    <div
      className={`group relative bg-white rounded-2xl shadow-md hover:shadow-2xl transition-all duration-300 overflow-hidden border border-gray-100 hover:border-gray-200 ${
        highlightBest ? 'ring-2 ring-green-500 shadow-lg' : ''
      }`}
    >
      {highlightBest && (
        <div className="absolute top-4 right-4 z-10 bg-gradient-to-r from-green-500 to-green-600 text-white px-4 py-2 rounded-full text-sm font-bold flex items-center space-x-1 shadow-lg animate-fade-in">
          <TrendingDown className="w-4 h-4" />
          <span>Best Deal</span>
        </div>
      )}

      <div className="p-6">
        {/* Platform Badge */}
        {showPlatform && (
          <div
            className="inline-flex items-center px-4 py-1.5 rounded-full text-white text-sm font-semibold mb-4 shadow-md"
            style={{ backgroundColor: platformColor }}
          >
            {listing.platform.name}
          </div>
        )}

        <div className="flex flex-col">
          {/* Product Image */}
          <div className="flex-shrink-0 mb-4">
            <div className="relative w-full h-48 rounded-xl overflow-hidden bg-gray-100 group-hover:scale-105 transition-transform duration-300">
              <img
                src={getImageUrl(listing.image_url)}
                alt={listing.title}
                className="w-full h-full object-cover"
                onError={(e) => {
                  e.currentTarget.src = 'https://via.placeholder.com/300x200?text=No+Image';
                }}
              />
            </div>
          </div>

          {/* Product Details */}
          <div className="flex-1 min-w-0 flex flex-col">
            <h3 className="text-lg font-bold mb-3 line-clamp-2 text-gray-900 group-hover:text-blue-600 transition-colors" title={listing.title}>
              {truncateText(listing.title, 60)}
            </h3>

            {/* Price */}
            <div className="mb-3">
              <div className="text-3xl font-extrabold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                {formatPrice(listing.price, listing.currency)}
              </div>
              {listing.shipping_cost && listing.shipping_cost > 0 && (
                <div className="text-sm text-gray-500 font-medium mt-1">
                  + {formatPrice(listing.shipping_cost, listing.currency)} shipping
                </div>
              )}
            </div>

            {/* Rating */}
            {listing.rating && typeof listing.rating === 'number' && (
              <div className="flex items-center space-x-2 mb-3">
                <div className="flex items-center space-x-1 bg-yellow-50 px-3 py-1 rounded-full">
                  <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                  <span className="text-sm font-bold text-gray-900">{Number(listing.rating).toFixed(1)}</span>
                </div>
                {listing.review_count && (
                  <span className="text-sm text-gray-500 font-medium">({listing.review_count} reviews)</span>
                )}
              </div>
            )}

            {/* Seller */}
            {listing.seller_name && (
              <div className="text-sm text-gray-600 mb-3 font-medium">
                Sold by: <span className="text-gray-900">{listing.seller_name}</span>
              </div>
            )}

            {/* Availability & CTA */}
            <div className="flex items-center justify-between mt-auto pt-4 border-t border-gray-100">
              <span
                className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-bold ${
                  listing.availability
                    ? 'bg-green-100 text-green-700'
                    : 'bg-red-100 text-red-700'
                }`}
              >
                {listing.availability ? '✓ In Stock' : '✗ Out of Stock'}
              </span>

              <a
                href={listing.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center space-x-2 px-6 py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl font-semibold hover:shadow-lg transition-all group-hover:scale-105"
              >
                <span>View Deal</span>
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>

            {/* Confidence Score for Image Search */}
            {listing.confidence_score && (
              <div className="mt-3 inline-flex items-center bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-xs font-semibold">
                Match confidence: {listing.confidence_score}%
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
