import { useParams } from 'react-router-dom';
import { useQuery } from 'react-query';
import { Loader2, TrendingUp, TrendingDown } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { productApi } from '../api';
import ProductCard from '../components/ProductCard';
import { formatPrice, formatDate } from '../utils';

export default function ProductDetailsPage() {
  const { id } = useParams<{ id: string }>();
  
  const { data: product, isLoading: productLoading } = useQuery(
    ['product', id],
    () => productApi.getProduct(Number(id)),
    {
      enabled: !!id,
    }
  );

  const { data: priceHistory, isLoading: historyLoading } = useQuery(
    ['priceHistory', id],
    () => productApi.getPriceHistory(Number(id)),
    {
      enabled: !!id,
    }
  );

  if (productLoading || historyLoading) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <Loader2 className="w-12 h-12 animate-spin text-primary-600 mx-auto mb-4" />
        <p className="text-gray-600 dark:text-gray-400">Loading product details...</p>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <p className="text-red-600">Product not found</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Product Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">{product.name}</h1>
        {product.brand && (
          <p className="text-xl text-gray-600 dark:text-gray-400">
            Brand: {product.brand}
          </p>
        )}
        {product.category && (
          <p className="text-gray-600 dark:text-gray-400">
            Category: {product.category}
          </p>
        )}
      </div>

      {/* Price Stats */}
      {product.price_range && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center space-x-2 mb-2">
              <TrendingDown className="w-5 h-5 text-green-600" />
              <span className="text-sm text-gray-600 dark:text-gray-400">Lowest Price</span>
            </div>
            <div className="text-2xl font-bold text-green-600">
              {formatPrice(product.price_range.min)}
            </div>
            {product.lowest_price && (
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                on {product.lowest_price.platform}
              </p>
            )}
          </div>

          <div className="card">
            <div className="flex items-center space-x-2 mb-2">
              <TrendingUp className="w-5 h-5 text-red-600" />
              <span className="text-sm text-gray-600 dark:text-gray-400">Highest Price</span>
            </div>
            <div className="text-2xl font-bold text-red-600">
              {formatPrice(product.price_range.max)}
            </div>
          </div>

          <div className="card">
            <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">Average Price</div>
            <div className="text-2xl font-bold text-blue-600">
              {formatPrice(product.price_range.avg)}
            </div>
          </div>
        </div>
      )}

      {/* Price History Chart */}
      {priceHistory && priceHistory.length > 0 && (
        <div className="card mb-8">
          <h2 className="text-2xl font-bold mb-4">Price History</h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={priceHistory}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="recorded_at"
                tickFormatter={(value) => formatDate(value)}
              />
              <YAxis />
              <Tooltip
                labelFormatter={(value) => formatDate(value as string)}
                formatter={(value: number) => formatPrice(value)}
              />
              <Legend />
              {priceHistory.map((platformHistory: any, index: number) => (
                <Line
                  key={platformHistory.platform}
                  type="monotone"
                  dataKey="price"
                  data={platformHistory.history}
                  name={platformHistory.platform}
                  stroke={`hsl(${index * 60}, 70%, 50%)`}
                  strokeWidth={2}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Current Listings */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Current Listings</h2>
        <div className="grid grid-cols-1 gap-4">
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
    </div>
  );
}
