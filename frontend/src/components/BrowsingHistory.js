import React from 'react';
import '../styles/BrowsingHistory.css';

const BrowsingHistory = ({ history, products, onClearHistory }) => {
  // Get browsed product details from product catalog
  const getBrowsedProducts = () => {
    if (!history || !products) return [];
    
    return history.map(productId => {
      const product = products.find(p => p.id === productId);
      return product;
    }).filter(Boolean); // Remove any undefined products
  };

  const browsedProducts = getBrowsedProducts();

  const handleClearHistory = () => {
    if (window.confirm('Are you sure you want to clear your browsing history?')) {
      onClearHistory();
    }
  };

  const getCategoryIcon = (category) => {
    const icons = {
      'Electronics': '📱',
      'Clothing': '👕',
      'Footwear': '👟',
      'Home': '🏠',
      'Sports': '⚽',
      'Beauty': '💄',
      'Books': '📚',
      'Accessories': '�',
      'Pets': '🐕',
      'Health': '💊',
      'Toys': '🧸',
      'Office': '📝'
    };
    return icons[category] || '📦';
  };

  return (
    <div className="history-container">
      <div className="history-header">
        <h3>Your Browsing History</h3>
        {browsedProducts.length > 0 && (
          <button className="clear-history-btn" onClick={handleClearHistory}>
            Clear All
          </button>
        )}
      </div>

      {browsedProducts.length > 0 ? (
        <>
          <div className="history-summary">
            <span className="history-count">{browsedProducts.length} item{browsedProducts.length !== 1 ? 's' : ''} viewed</span>
          </div>
          
          <div className="history-items">
            {browsedProducts.map((product, index) => (
              <div key={`${product.id}-${index}`} className="history-item">
                <div className="history-item-icon-container">
                  <div className="history-item-icon">
                    {getCategoryIcon(product.category)}
                  </div>
                </div>
                <div className="history-item-details">
                  <h4 className="history-item-name">{product.name}</h4>
                  <p className="history-item-price">${product.price}</p>
                  <span className="history-item-category">{product.category}</span>
                </div>
                <div className="history-item-badge">
                  #{browsedProducts.length - index}
                </div>
              </div>
            ))}
          </div>
          
          <div className="history-footer">
            <p className="history-note">
              💡 Your browsing history helps us recommend products you'll love!
            </p>
          </div>
        </>
      ) : (
        <div className="empty-history">
          <div className="empty-history-icon">👀</div>
          <h4>No browsing history yet</h4>
          <p>Click on products in the catalog to build your browsing history and get personalized recommendations.</p>
        </div>
      )}
    </div>
  );
};

export default BrowsingHistory;