import React, { useState } from 'react';

// Helper: extract unique categories/brands from products
const getUnique = (products, key) =>
  [...new Set(products.map(p => p[key]).filter(Boolean))];

const priceRanges = [
  { label: 'Any', value: 'all' },
  { label: 'Under $50', value: '0-50' },
  { label: '$50 - $100', value: '50-100' },
  { label: '$100 - $200', value: '100-200' },
  { label: 'Over $200', value: '200-' }
];

const UserPreferences = ({ preferences, products, onPreferencesChange }) => {
  const categories = getUnique(products, 'category');
  const brands = getUnique(products, 'brand');

  const [form, setForm] = useState({
    priceRange: preferences.priceRange || 'all',
    categories: preferences.categories || [],
    brands: preferences.brands || []
  });

  const handleChange = e => {
    const { name, value, type, checked } = e.target;
    if (type === 'checkbox') {
      setForm(prev => ({
        ...prev,
        [name]: checked
          ? [...prev[name], value]
          : prev[name].filter(v => v !== value)
      }));
    } else {
      setForm(prev => ({ ...prev, [name]: value }));
    }
  };

  // Notify parent on change
  React.useEffect(() => {
    onPreferencesChange(form);
    // eslint-disable-next-line
  }, [form]);

  return (
    <div className="preferences-container">
      <h3>Your Preferences</h3>
      <label>
        Price Range:
        <select name="priceRange" value={form.priceRange} onChange={handleChange}>
          {priceRanges.map(pr => (
            <option value={pr.value} key={pr.value}>{pr.label}</option>
          ))}
        </select>
      </label>

      <fieldset>
        <legend>Categories:</legend>
        {categories.map(cat => (
          <label key={cat}>
            <input
              type="checkbox"
              name="categories"
              value={cat}
              checked={form.categories.includes(cat)}
              onChange={handleChange}
            />
            {cat}
          </label>
        ))}
      </fieldset>

      <fieldset>
        <legend>Brands:</legend>
        {brands.map(brand => (
          <label key={brand}>
            <input
              type="checkbox"
              name="brands"
              value={brand}
              checked={form.brands.includes(brand)}
              onChange={handleChange}
            />
            {brand}
          </label>
        ))}
      </fieldset>
    </div>
  );
};

export default UserPreferences;