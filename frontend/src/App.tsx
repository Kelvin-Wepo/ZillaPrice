import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import SearchResultsPage from './pages/SearchResultsPage';
import ComparisonPage from './pages/ComparisonPage';
import ProductDetailsPage from './pages/ProductDetailsPage';

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<SearchResultsPage />} />
        <Route path="/compare" element={<ComparisonPage />} />
        <Route path="/product/:id" element={<ProductDetailsPage />} />
      </Routes>
    </Layout>
  );
}

export default App;
