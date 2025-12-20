import { useState } from 'react';
import { rangesApi, type RangeResponse as ApiRangeResponse } from '../api/ranges';
import RangeGridSelector from './RangeGridSelector';
import { getTotalCombos, getRangePercentage } from '../utils/handUtils';

type RangeResponse = ApiRangeResponse;

export default function RangeBuilder() {
  const [player, setPlayer] = useState<string>('OOP');
  const [selectedHands, setSelectedHands] = useState<Set<string>>(new Set());
  const [result, setResult] = useState<RangeResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleCreateRange = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Convert Set to Array for API
      const handsArray = Array.from(selectedHands);
      
      const response = await rangesApi.createRange(player, handsArray);
      setResult(response);
    } catch (err) {
      setError('Failed to create range. Please check your inputs.');
    } finally {
      setLoading(false);
    }
  };

  const handleClearAll = () => {
    setSelectedHands(new Set());
    setResult(null);
    setError(null);
  };

  const totalCombos = getTotalCombos(Array.from(selectedHands));
  const percentage = getRangePercentage(totalCombos);

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-3xl font-bold text-gray-800">Range Builder</h2>
      
      {/* Controls Section */}
      <div className="bg-white p-4 rounded-lg shadow-md space-y-4">
        {/* Player selector */}
        <div>
          <label className="block text-sm font-medium mb-2 text-gray-700">Player:</label>
          <select 
            value={player}
            onChange={(e) => setPlayer(e.target.value)}
            className="w-48 border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="OOP">OOP (Out of Position)</option>
            <option value="IP">IP (In Position)</option>
          </select>
        </div>

        {/* Selection Summary */}
        <div className="flex items-center gap-4 text-sm">
          <div className="px-4 py-2 bg-blue-50 rounded-lg">
            <span className="font-semibold text-blue-900">Selected: </span>
            <span className="text-blue-700">{selectedHands.size} hands</span>
          </div>
          <div className="px-4 py-2 bg-green-50 rounded-lg">
            <span className="font-semibold text-green-900">Combos: </span>
            <span className="text-green-700">{totalCombos} / 1326</span>
          </div>
          <div className="px-4 py-2 bg-purple-50 rounded-lg">
            <span className="font-semibold text-purple-900">Range: </span>
            <span className="text-purple-700">{percentage}%</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          <button
            onClick={handleCreateRange}
            disabled={selectedHands.size === 0 || loading}
            className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed font-medium transition-colors"
          >
            {loading ? 'Creating...' : 'Create Range'}
          </button>
          <button
            onClick={handleClearAll}
            disabled={selectedHands.size === 0}
            className="bg-red-500 text-white px-6 py-2 rounded-lg hover:bg-red-600 disabled:bg-gray-300 disabled:cursor-not-allowed font-medium transition-colors"
          >
            Clear All
          </button>
        </div>
      </div>

      {/* Grid Section */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">Select Hands</h3>
        <div className="flex justify-center">
          <RangeGridSelector
            selectedHands={selectedHands}
            onHandsChange={setSelectedHands}
          />
        </div>
      </div>

      {/* Selected Hands List */}
      {selectedHands.size > 0 && (
        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-md">
          <h3 className="text-lg font-semibold mb-3 text-gray-800">
            Selected Hands ({selectedHands.size})
          </h3>
          <div className="bg-gray-50 p-4 rounded border border-gray-300 max-h-64 overflow-y-auto">
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {Array.from(selectedHands).sort().map((hand) => (
                <span
                  key={hand}
                  style={{
                    display: 'inline-block',
                    backgroundColor: '#DBEAFE',
                    color: '#1E40AF',
                    padding: '4px 12px',
                    borderRadius: '6px',
                    fontSize: '14px',
                    fontWeight: 600,
                  }}
                >
                  {hand}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Error display */}
      {error && (
        <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          <p className="font-semibold">Error:</p>
          <p>{error}</p>
        </div>
      )}

      {/* Result display */}
      {result && (
        <div className="p-6 bg-green-50 border border-green-200 rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-green-900">Range Created Successfully!</h3>
          <div className="space-y-2">
            <p className="text-sm text-green-800">
              <span className="font-semibold">Player:</span> {result.player}
            </p>
            <p className="text-sm text-green-800">
              <span className="font-semibold">Total Hand Combinations:</span> {result.count}
            </p>
            <div className="mt-4">
              <p className="font-semibold text-sm text-green-900 mb-2">Expanded Hands:</p>
              <div className="bg-white p-3 rounded border border-green-200 max-h-48 overflow-y-auto">
                <p className="text-xs text-gray-700 font-mono">
                  {result.hands.join(', ')}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}





