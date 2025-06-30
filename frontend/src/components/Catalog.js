// Personal note: This took me way too long to get the filtering logic right!
// TODO: Maybe add sorting options later (by price, rating, etc.)

import React, { useState } from 'react';
import '../styles/Catalog.css';

const Catalog = ({ products, onProductClick, browsingHistory, userPreferences }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [productsPerPage] = useState(8); // Better UX with 8 products per page
  const [expandedDescriptions, setExpandedDescriptions] = useState({}); // Track which descriptions are expanded

  // Generate category-based icons instead of placeholder images
  const getCategoryIcon = (category) => {
    const icons = {
      'Electronics': '📱',
      'Clothing': '👕',
      'Footwear': '👟',
      'Home': '🏠',
      'Sports': '⚽',
      'Beauty': '💄',
      'Books': '📚',
      'Accessories': '🎒',
      'Pets': '🐕',
      'Health': '💊',
      'Toys': '🧸',
      'Office': '📝'
    };
    return icons[category] || '📦';
  };

  // Simple star rating display - could be more fancy but this works
  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    for (let i = 0; i < fullStars; i++) {
      stars.push('★');
    }
    if (hasHalfStar) {
      stars.push('☆');
    }
    return stars.join('');
  };

  // Toggle description expansion - had to add this for better UX
  const toggleDescription = (productId, e) => {
    e.stopPropagation(); // Prevent triggering the product click
    setExpandedDescriptions(prev => ({
      ...prev,
      [productId]: !prev[productId]
    }));
  };

  // Pagination functions
  const filterProductsByPreferences = (products, preferences) => {
    if (!preferences) return products;
    
    return products.filter(product => {
      // Price range filter
      if (preferences.priceRange && preferences.priceRange !== 'all') {
        const price = product.price;
        switch (preferences.priceRange) {
          case 'under-50':
            if (price >= 50) return false;
            break;
          case '50-100':
            if (price < 50 || price > 100) return false;
            break;
          case '100-200':
            if (price < 100 || price > 200) return false;
            break;
          case 'over-200':
            if (price <= 200) return false;
            break;
          default:
            break;
        }
      }
      
      // Category filter
      if (preferences.categories && preferences.categories.length > 0) {
        if (!preferences.categories.includes(product.category)) {
          return false;
        }
      }
      
      // Brand filter
      if (preferences.brands && preferences.brands.length > 0) {
        if (!preferences.brands.includes(product.brand)) {
          return false;
        }
      }
      
      return true;
    });
  };

  const filteredProducts = filterProductsByPreferences(products, userPreferences);
  const totalPages = Math.ceil(filteredProducts.length / productsPerPage);
  
  const getCurrentPageProducts = () => {
    const startIndex = (currentPage - 1) * productsPerPage;
    const endIndex = startIndex + productsPerPage;
    return filteredProducts.slice(startIndex, endIndex);
  };

  const goToNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const goToPreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const goToPage = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  return (
    <div className="catalog-container">
      {filteredProducts && filteredProducts.length > 0 ? (
        <>
          {/* Filter Info */}
          <div className="filter-info">
            <span className="filter-count">
              Showing {filteredProducts.length} of {products.length} products
            </span>
            {(userPreferences?.categories?.length > 0 || 
              userPreferences?.brands?.length > 0 || 
              (userPreferences?.priceRange && userPreferences.priceRange !== 'all')) && (
              <button 
                className="clear-filters-btn"
                onClick={() => window.location.reload()} // Simple reset - you can improve this
              >
                Clear Filters
              </button>
            )}
          </div>
          
          {/* Pagination Info */}
          <div className="pagination-info">
            Showing {((currentPage - 1) * productsPerPage) + 1} - {Math.min(currentPage * productsPerPage, filteredProducts.length)} of {filteredProducts.length} filtered products
          </div>
          
          <div className="products-grid">
            {getCurrentPageProducts().map(product => {
            const isExpanded = expandedDescriptions[product.id];
            const shouldShowReadMore = product.description && product.description.length > 100;
            
            return (
              <div 
                key={product.id} 
                className={`product-card ${browsingHistory.includes(product.id) ? 'viewed' : ''}`}
                onClick={() => onProductClick(product.id)}
              >
                {/* Viewed Indicator */}
                {browsingHistory.includes(product.id) && (
                  <span className="viewed-indicator">✓ Viewed</span>
                )}
                
                {/* Product Icon/Image */}
                <div className="product-icon-container">
                  <div className="product-icon">
                    {getCategoryIcon(product.category)}
                  </div>
                  <span className="category-label">{product.category}</span>
                </div>
                
                {/* Product Content */}
                <div className="product-content">
                  <h3 className="product-name">{product.name}</h3>
                  <p className="product-price">${product.price}</p>
                  <p className="product-category">{product.category}</p>
                  <p className="product-brand">{product.brand}</p>
                  
                  {/* Product Rating */}
                  {product.rating && (
                    <div className="product-rating">
                      <span className="rating-stars">{renderStars(product.rating)}</span>
                      <span className="rating-value">({product.rating})</span>
                    </div>
                  )}
                  
                  {/* Product Description with Read More */}
                  {product.description && (
                    <div>
                      <p className={`product-description ${isExpanded ? 'expanded' : 'collapsed'}`}>
                        {isExpanded ? product.description : `${product.description.substring(0, 100)}${product.description.length > 100 ? '...' : ''}`}
                      </p>
                      {shouldShowReadMore && (
                        <button 
                          className="read-more-btn"
                          onClick={(e) => toggleDescription(product.id, e)}
                        >
                          {isExpanded ? 'Read Less' : 'Read More'}
                        </button>
                      )}
                    </div>
                  )}
                  
                  {/* Product Features */}
                  {product.features && product.features.length > 0 && (
                    <div className="product-features">
                      <h4>Features:</h4>
                      <div className="features-list">
                        {product.features.slice(0, 3).map((feature, index) => (
                          <span key={index} className="feature-tag">{feature}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );            })}
          </div>
          
          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="pagination-controls">
              <button 
                className="pagination-btn prev-btn"
                onClick={goToPreviousPage}
                disabled={currentPage === 1}
              >
                ← Previous
              </button>
              
              <div className="page-numbers">
                {Array.from({ length: totalPages }, (_, index) => (
                  <button
                    key={index + 1}
                    className={`page-btn ${currentPage === index + 1 ? 'active' : ''}`}
                    onClick={() => goToPage(index + 1)}
                  >
                    {index + 1}
                  </button>
                ))}
              </div>
              
              <button 
                className="pagination-btn next-btn"
                onClick={goToNextPage}
                disabled={currentPage === totalPages}
              >
                Next →
              </button>
            </div>
          )}
        </>
      ) : (
        <div className="no-products">
          {products && products.length > 0 ? (
            <div>
              <h3>No products match your preferences</h3>
              <p>Try adjusting your filters to see more products</p>
              <button 
                className="clear-filters-btn"
                onClick={() => window.location.reload()}
              >
                Clear All Filters
              </button>
            </div>
          ) : (
            <div>No products available</div>
          )}
        </div>
      )}
    </div>
  );
};

export default Catalog;