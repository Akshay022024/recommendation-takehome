import React from 'react';
import '../styles/UserPreferences.css';

const UserPreferences = ({ preferences, products, onPreferencesChange }) => {
  // Extract unique categories and brands from products for dynamic options
  const categories = products ? [...new Set(products.map(p => p.category))] : [];
  const brands = products ? [...new Set(products.map(p => p.brand))].slice(0, 10) : [];

  const handlePriceRangeChange = (range) => {
    onPreferencesChange({
      ...preferences,
      priceRange: range
    });
  };

  const handleCategoryChange = (category) => {
    const updatedCategories = preferences.categories?.includes(category)
      ? preferences.categories.filter(c => c !== category)
      : [...(preferences.categories || []), category];
    
    onPreferencesChange({
      ...preferences,
      categories: updatedCategories
    });
  };

  const handleBrandChange = (brand) => {
    const updatedBrands = preferences.brands?.includes(brand)
      ? preferences.brands.filter(b => b !== brand)
      : [...(preferences.brands || []), brand];
    
    onPreferencesChange({
      ...preferences,
      brands: updatedBrands
    });
  };

  const getPriceRangeLabel = (range) => {
    const labels = {
      'all': 'All Prices',
      'under-50': 'Under $50',
      '50-100': '$50 - $100',
      '100-200': '$100 - $200',
      'over-200': 'Over $200'
    };
    return labels[range] || range;
  };

  return (
    <div className="preferences-container">
      <h3>Your Preferences</h3>
      
      {/* Price Range Selection */}
      <div className="preference-section">
        <h4>Price Range</h4>
        <div className="price-options">
          {['all', 'under-50', '50-100', '100-200', 'over-200'].map(range => (
            <label key={range} className="price-option">
              <input
                type="radio"
                name="priceRange"
                value={range}
                checked={preferences.priceRange === range}
                onChange={() => handlePriceRangeChange(range)}
              />
              <span>{getPriceRangeLabel(range)}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Category Selection */}
      <div className="preference-section">
        <h4>Categories</h4>
        <div className="category-options">
          {categories.map(category => (
            <label key={category} className="checkbox-option">
              <input
                type="checkbox"
                checked={preferences.categories?.includes(category) || false}
                onChange={() => handleCategoryChange(category)}
              />
              <span>{category}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Brand Selection */}
      <div className="preference-section">
        <h4>Preferred Brands</h4>
        <div className="brand-options">
          {brands.map(brand => (
            <label key={brand} className="checkbox-option">
              <input
                type="checkbox"
                checked={preferences.brands?.includes(brand) || false}
                onChange={() => handleBrandChange(brand)}
              />
              <span>{brand}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Selected Preferences Summary */}
      {(preferences.categories?.length > 0 || preferences.brands?.length > 0 || preferences.priceRange !== 'all') && (
        <div className="preferences-summary">
          <h4>Current Selection:</h4>
          <ul>
            {preferences.priceRange !== 'all' && (
              <li>Price: {getPriceRangeLabel(preferences.priceRange)}</li>
            )}
            {preferences.categories?.length > 0 && (
              <li>Categories: {preferences.categories.join(', ')}</li>
            )}
            {preferences.brands?.length > 0 && (
              <li>Brands: {preferences.brands.join(', ')}</li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
};

export default UserPreferences;