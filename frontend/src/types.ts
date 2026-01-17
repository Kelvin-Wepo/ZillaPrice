/**
 * TypeScript type definitions
 */

export interface Platform {
  id: number;
  name: string;
  base_url: string;
  is_active: boolean;
}

export interface PriceHistory {
  price: number;
  recorded_at: string;
}

export interface ProductListing {
  id: number;
  platform: Platform;
  title: string;
  url: string;
  image_url: string;
  price: number;
  currency: string;
  shipping_cost?: number;
  total_price: number;
  rating?: number;
  review_count?: number;
  availability: boolean;
  seller_name?: string;
  confidence_score?: number;
  scraped_at: string;
  price_history?: PriceHistory[];
}

export interface Product {
  id: number;
  name: string;
  brand?: string;
  category?: string;
  description?: string;
  image_url?: string;
  created_at: string;
  updated_at: string;
  search_count: number;
  listings: ProductListing[];
  lowest_price?: {
    price: number;
    currency: string;
    platform: string;
  };
  price_range?: {
    min: number;
    max: number;
    avg: number;
  };
}

export interface SearchResult {
  task_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  message: string;
  products?: Product[];
  search_info?: {
    product_name?: string;
    brand?: string;
    category?: string;
    confidence?: string;
  };
  progress?: {
    completed: number;
    total: number;
    percentage: number;
  };
}

export interface ComparisonData {
  product: Product;
  platform_prices: {
    [platform: string]: Array<{
      listing_id: number;
      title: string;
      price: number;
      currency: string;
      total_price: number;
      url: string;
      rating?: number;
      review_count?: number;
      seller?: string;
    }>;
  };
  best_deal: {
    platform: string;
    price: number;
    total_price: number;
    url: string;
    savings: number;
  };
  price_stats: {
    min: number;
    max: number;
    avg: number;
    count: number;
  };
}

export interface SearchHistory {
  id: number;
  query: string;
  search_type: 'text' | 'image';
  results_count: number;
  created_at: string;
}

export type SortOption = 'price_asc' | 'price_desc' | 'rating' | 'name';
export type FilterOption = 'all' | 'available' | 'with_rating';
