import React from 'react';

const Recommendations = ({ recommendations, isLoading }) => {
  if (isLoading) return <p>Loading recommendations...</p>;

  if (!recommendations || recommendations.length === 0)
    return <p>No recommendations yet. Set your preferences and browse some products!</p>;

  return (
    <div className="recommendations-list">
      {recommendations.map((rec, idx) => {
        const product = rec.product || {};
        return (
          <div key={product.id || idx} className="product-card recommendation-card">
            <h3>{product.name}</h3>
            <p>
              {product.category}
              {product.subcategory ? <> - {product.subcategory}</> : null}
            </p>
            <p><strong>Price:</strong> ${product.price}</p>
            <p><strong>Brand:</strong> {product.brand}</p>
            <div className="product-rating">⭐ {product.rating}</div>
            {rec.explanation && (
              <p className="recommendation-explanation">
                <strong>Why?</strong> {rec.explanation}
              </p>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default Recommendations;