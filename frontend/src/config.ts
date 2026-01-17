/**
 * API configuration and base URL
 */
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const API_ENDPOINTS = {
  textSearch: '/api/search/text/',
  imageSearch: '/api/search/image/',
  searchStatus: '/api/search/status/',
  compare: '/api/compare/',
  products: '/api/products/',
  platforms: '/api/platforms/',
  searchHistory: '/api/search/history/',
};

/**
 * Platform configuration
 */
export const PLATFORMS = [
  { id: 'jumia', name: 'Jumia', color: '#f68b1e' },
  { id: 'kilimall', name: 'Kilimall', color: '#e31e24' },
  { id: 'alibaba', name: 'Alibaba', color: '#ff6a00' },
  { id: 'amazon', name: 'Amazon', color: '#ff9900' },
  { id: 'ebay', name: 'eBay', color: '#e53238' },
];

/**
 * Polling configuration for search status
 */
export const POLLING_INTERVAL = 3000; // 3 seconds
export const MAX_POLLING_ATTEMPTS = 40; // 2 minutes max
