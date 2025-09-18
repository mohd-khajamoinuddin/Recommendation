import React from 'react';

const BrowsingHistory = ({ history, products, onClearHistory }) => {
  if (!history || history.length === 0)
    return (
      <div className="history-container">
        <h3>Your Browsing History</h3>
        <p>No products viewed yet.</p>
      </div>
    );

  const historyProducts = products.filter(p => history.includes(p.id));

  return (
    <div className="history-container">
      <h3>Your Browsing History</h3>
      <ul>
        {historyProducts.map(product => (
          <li key={product.id}>
            <strong>{product.name}</strong> ({product.category})
          </li>
        ))}
      </ul>
      <button className="get-recommendations-btn" onClick={onClearHistory}>
        Clear History
      </button>
    </div>
  );
};

export default BrowsingHistory;