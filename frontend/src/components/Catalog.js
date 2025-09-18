import React from 'react';

const Catalog = ({ products, onProductClick, browsingHistory }) => {
  if (!products || products.length === 0) {
    return <div>No products available.</div>;
  }

  return (
    <div className="catalog-grid">
      {products.map(product => (
        <div
          key={product.id}
          className={`product-card${browsingHistory.includes(product.id) ? ' viewed' : ''}`}
          onClick={() => onProductClick(product.id)}
          tabIndex={0}
          role="button"
          aria-pressed={browsingHistory.includes(product.id)}
        >
          <h3>{product.name}</h3>
          <p>{product.category} {product.subcategory && <>- {product.subcategory}</>}</p>
          <p><strong>Price:</strong> ${product.price}</p>
          <p><strong>Brand:</strong> {product.brand}</p>
          <p className="product-description">{product.description}</p>
          <div className="product-rating">⭐ {product.rating}</div>
        </div>
      ))}
    </div>
  );
};

export default Catalog;