import React from 'react';
import '../styles/Recommendations.css';

const Recommendations = ({ recommendations, isLoading, error }) => {
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

  const renderConfidenceStars = (score) => {
    const maxStars = 5;
    const filledStars = Math.round((score / 10) * maxStars);
    return Array.from({ length: maxStars }, (_, i) => (
      <span key={i} className={i < filledStars ? 'star filled' : 'star'}>★</span>
    ));
  };

  const renderLoadingState = () => (
    <div className="loading-state">
      <div className="loading-spinner"></div>
      <h3>Generating AI Recommendations...</h3>
      <p>Our AI is analyzing your preferences and browsing history to find the perfect products for you.</p>
      <div className="loading-steps">
        <div className="loading-step">🧠 Analyzing your preferences</div>
        <div className="loading-step">📊 Processing browsing history</div>
        <div className="loading-step">🤖 Generating personalized recommendations</div>
      </div>
    </div>
  );

  const renderEmptyState = () => (
    <div className="empty-state">
      <div className="empty-icon">🎯</div>
      <h3>No recommendations yet</h3>
      <p>Set your preferences and browse some products to get personalized AI recommendations!</p>
      <div className="empty-tips">
        <div className="tip">💡 Select your preferred categories</div>
        <div className="tip">💰 Choose your price range</div>
        <div className="tip">👆 Click on products you like</div>
      </div>
    </div>
  );

  const renderErrorState = () => (
    <div className="error-state">
      <div className="error-icon">⚠️</div>
      <h3>Unable to generate recommendations</h3>
      <p>{error || 'Something went wrong while generating recommendations. Please try again.'}</p>
      <button className="retry-btn" onClick={() => window.location.reload()}>
        Try Again
      </button>
    </div>
  );

  const renderRecommendations = () => (
    <div className="recommendations-content">
      <div className="recommendations-header">
        <h3>🤖 AI Recommendations for You</h3>
        <p className="recommendations-subtitle">
          Based on your preferences and browsing history, here are {recommendations.length} products we think you'll love:
        </p>
      </div>

      <div className="recommendations-grid">
        {recommendations.map((recommendation, index) => {
          const product = recommendation.product;
          const explanation = recommendation.explanation;
          const confidence = recommendation.confidence_score || 5;

          return (
            <div key={`${product.id}-${index}`} className="recommendation-card">
              <div className="recommendation-rank">#{index + 1}</div>
              
              <div className="recommendation-icon-container">
                <div className="recommendation-icon">
                  {getCategoryIcon(product.category)}
                </div>
                <span className="recommendation-category-label">{product.category}</span>
              </div>
              
              <div className="recommendation-content">
                <h4 className="recommendation-name">{product.name}</h4>
                <p className="recommendation-price">${product.price}</p>
                <span className="recommendation-category">{product.category}</span>
                
                <div className="recommendation-confidence">
                  <span className="confidence-label">AI Confidence:</span>
                  <div className="confidence-stars">
                    {renderConfidenceStars(confidence)}
                  </div>
                  <span className="confidence-score">({confidence}/10)</span>
                </div>
                
                <div className="recommendation-explanation">
                  <h5>Why we recommend this:</h5>
                  <p>{explanation}</p>
                </div>

                {product.features && product.features.length > 0 && (
                  <div className="recommendation-features">
                    <h5>Key features:</h5>
                    <div className="features-tags">
                      {product.features.slice(0, 3).map((feature, idx) => (
                        <span key={idx} className="feature-tag">{feature}</span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <div className="recommendations-footer">
        <p className="recommendations-note">
          💡 These recommendations improve as you browse more products and update your preferences!
        </p>
      </div>
    </div>
  );

  return (
    <div className="recommendations-container">
      {isLoading ? renderLoadingState() :
       error ? renderErrorState() :
       recommendations && recommendations.length > 0 ? renderRecommendations() :
       renderEmptyState()}
    </div>
  );
};

export default Recommendations;


