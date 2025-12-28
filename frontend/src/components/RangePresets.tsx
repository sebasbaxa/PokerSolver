import { useState, useEffect } from 'react';
import { rangesApi } from '../api/ranges';

interface Presets {
  [key: string]: string[];
}

export default function RangePresets() {
  const [presets, setPresets] = useState<Presets | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    rangesApi.getPresets()
      .then(data => {
        console.log('Presets data:', data); // Debug log
        setPresets(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching presets:', err);
        setError('Failed to load presets');
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="presets-loading">Loading...</div>;
  if (error) return <div className="presets-error">{error}</div>;
  if (!presets) return <div className="presets-empty">No presets available</div>;

  return (
    <div className="presets-container">
      <h2 className="presets-title">Range Presets</h2>
      {Object.entries(presets).map(([name, hands]) => (
        <div key={name} className="preset-item">
          <h3 className="preset-name">{name}</h3>
          <p className="preset-hands">
            {Array.isArray(hands) ? hands.join(', ') : 'Invalid data'}
          </p>
        </div>
      ))}
    </div>
  );
}