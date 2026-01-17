import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Image as ImageIcon, Loader2 } from 'lucide-react';
import { searchApi } from '../api';

export default function SearchBar() {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState<'text' | 'image'>('text');
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [isSearching, setIsSearching] = useState(false);
  const navigate = useNavigate();

  const handleTextSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsSearching(true);
    try {
      const result = await searchApi.textSearch(query);
      navigate(`/search?task_id=${result.task_id}&query=${encodeURIComponent(query)}`);
    } catch (error) {
      console.error('Search failed:', error);
      alert('Search failed. Please try again.');
    } finally {
      setIsSearching(false);
    }
  };

  const handleImageSearch = async () => {
    if (!imageFile) return;

    setIsSearching(true);
    try {
      const result = await searchApi.imageSearch(imageFile);
      navigate(`/search?task_id=${result.task_id}&type=image`);
    } catch (error) {
      console.error('Image search failed:', error);
      alert('Image search failed. Please try again.');
    } finally {
      setIsSearching(false);
    }
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImageFile(file);
      setSearchType('image');
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto animate-slide-in">
      {/* Search Type Tabs */}
      <div className="flex space-x-3 mb-6 bg-white rounded-2xl p-2 shadow-lg border border-gray-100">
        <button
          onClick={() => setSearchType('text')}
          className={`flex items-center space-x-2 px-6 py-3 rounded-xl font-semibold transition-all duration-300 flex-1 ${
            searchType === 'text'
              ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-md scale-[1.02]'
              : 'bg-white text-gray-600 hover:bg-gray-50'
          }`}
        >
          <Search className="w-5 h-5" />
          <span>Text Search</span>
        </button>
        <button
          onClick={() => setSearchType('image')}
          className={`flex items-center space-x-2 px-6 py-3 rounded-xl font-semibold transition-all duration-300 flex-1 ${
            searchType === 'image'
              ? 'bg-gradient-to-r from-purple-600 to-purple-700 text-white shadow-md scale-[1.02]'
              : 'bg-white text-gray-600 hover:bg-gray-50'
          }`}
        >
          <ImageIcon className="w-5 h-5" />
          <span>Image Search</span>
        </button>
      </div>

      {/* Search Input */}
      {searchType === 'text' ? (
        <form onSubmit={handleTextSearch} className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for products (e.g., iPhone 15 Pro, Samsung TV, Nike shoes)"
            className="w-full px-6 py-5 pr-16 text-lg rounded-2xl border-2 border-gray-200 focus:border-blue-500 focus:ring-4 focus:ring-blue-100 outline-none transition-all shadow-lg"
            disabled={isSearching}
          />
          <button
            type="submit"
            disabled={isSearching || !query.trim()}
            className="absolute right-3 top-1/2 -translate-y-1/2 p-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-none"
          >
            {isSearching ? (
              <Loader2 className="w-6 h-6 animate-spin" />
            ) : (
              <Search className="w-6 h-6" />
            )}
          </button>
        </form>
      ) : (
        <div className="space-y-4">
          <div className="border-3 border-dashed border-purple-300 bg-purple-50 rounded-2xl p-12 text-center transition-all hover:border-purple-400 hover:bg-purple-100 shadow-lg">
            <input
              type="file"
              id="image-upload"
              accept="image/*"
              onChange={handleImageChange}
              className="hidden"
              disabled={isSearching}
            />
            <label
              htmlFor="image-upload"
              className="cursor-pointer flex flex-col items-center space-y-3"
            >
              <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
                <ImageIcon className="w-10 h-10 text-white" />
              </div>
              <div>
                <span className="text-lg font-semibold text-gray-700 block">
                  {imageFile ? imageFile.name : 'Click to upload or drag image here'}
                </span>
                <span className="text-sm text-gray-500 mt-1 block">
                  Supports JPG, PNG, GIF (Max 10MB)
                </span>
              </div>
            </label>
          </div>

          {imageFile && (
            <button
              onClick={handleImageSearch}
              disabled={isSearching}
              className="w-full py-4 px-6 bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-2xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              {isSearching ? (
                <>
                  <Loader2 className="w-6 h-6 animate-spin" />
                  <span>Processing Image...</span>
                </>
              ) : (
                <>
                  <Search className="w-6 h-6" />
                  <span>Search with Image</span>
                </>
              )}
            </button>
          )}
        </div>
      )}

      {/* Popular Searches */}
      <div className="mt-6 flex flex-wrap items-center gap-3">
        <span className="text-sm font-medium text-gray-500">Popular searches:</span>
        {['iPhone 15', 'Samsung Galaxy', 'MacBook Pro', 'AirPods'].map((term) => (
          <button
            key={term}
            onClick={() => {
              setQuery(term);
              setSearchType('text');
            }}
            className="text-sm px-4 py-2 bg-gradient-to-r from-gray-100 to-gray-200 text-gray-700 rounded-full hover:from-blue-100 hover:to-blue-200 hover:text-blue-700 transition-all shadow-sm hover:shadow-md font-medium"
          >
            {term}
          </button>
        ))}
      </div>
    </div>
  );
}
