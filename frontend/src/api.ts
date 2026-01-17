/**
 * API service for making HTTP requests
 */
import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS } from './config';
import type { Product, SearchResult, ComparisonData, SearchHistory } from './types';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchApi = {
  /**
   * Search for products using text query
   */
  textSearch: async (query: string, platforms?: string[], maxResults = 20) => {
    const response = await api.post<SearchResult>(API_ENDPOINTS.textSearch, {
      query,
      platforms,
      max_results: maxResults,
    });
    return response.data;
  },

  /**
   * Search for products using image
   */
  imageSearch: async (imageFile: File, maxResults = 20) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('max_results', maxResults.toString());

    const response = await api.post<SearchResult>(API_ENDPOINTS.imageSearch, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Check search task status
   */
  getSearchStatus: async (taskId: string) => {
    const response = await api.get<SearchResult>(
      `${API_ENDPOINTS.searchStatus}${taskId}/`
    );
    return response.data;
  },

  /**
   * Get search history
   */
  getSearchHistory: async () => {
    const response = await api.get<SearchHistory[]>(API_ENDPOINTS.searchHistory);
    return response.data;
  },
};

export const productApi = {
  /**
   * Get product by ID
   */
  getProduct: async (id: number) => {
    const response = await api.get<Product>(`${API_ENDPOINTS.products}${id}/`);
    return response.data;
  },

  /**
   * Get product price history
   */
  getPriceHistory: async (id: number) => {
    const response = await api.get(`${API_ENDPOINTS.products}${id}/price_history/`);
    return response.data;
  },

  /**
   * Compare products
   */
  compareProducts: async (productId?: number, query?: string) => {
    const params: Record<string, string> = {};
    if (productId) params.product_id = productId.toString();
    if (query) params.query = query;

    const response = await api.get<{ comparisons: ComparisonData[]; total_products: number }>(
      API_ENDPOINTS.compare,
      { params }
    );
    return response.data;
  },
};

export default api;
