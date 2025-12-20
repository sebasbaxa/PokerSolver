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

  if (loading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4 text-red-600">{error}</div>;
  if (!presets) return <div className="p-4">No presets available</div>;

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Range Presets</h2>
      {Object.entries(presets).map(([name, hands]) => (
        <div key={name} className="mb-4 p-3 border rounded">
          <h3 className="font-semibold capitalize">{name}</h3>
          <p className="text-sm text-gray-600">
            {Array.isArray(hands) ? hands.join(', ') : 'Invalid data'}
          </p>
        </div>
      ))}
    </div>
  );
}