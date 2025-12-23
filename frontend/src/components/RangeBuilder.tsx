import RangeGridSelector from './RangeGridSelector';
import { getTotalCombos, getRangePercentage } from '../utils/handUtils';

interface RangeBuilderProps {
  player: string;
  selectedHands: Set<string>;
  onHandsChange: (hands: Set<string>) => void;
}

export default function RangeBuilder({ player, selectedHands, onHandsChange }: RangeBuilderProps) {
  const handleClearAll = () => {
    onHandsChange(new Set());
  };

  const totalCombos = getTotalCombos(Array.from(selectedHands));
  const percentage = getRangePercentage(totalCombos);

  return (
    <div className="p-2 space-y-3">
      {/* Controls Section */}
      <div className="bg-white p-2 rounded-lg shadow-md space-y-2">
        {/* Player display (read-only) */}
        <div>
          <label className="block text-sm font-medium mb-2 text-gray-700">Player:</label>
          <div className="text-lg font-semibold text-gray-800">{player}</div>
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

        {/* Clear All Button */}
        <div className="flex gap-2">
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
      <div className="bg-gray-50 p-3 rounded-lg border border-gray-200">
        <h3 className="text-base font-semibold mb-2 text-gray-800">Select Hands</h3>
        <div className="flex justify-center">
          <RangeGridSelector
            selectedHands={selectedHands}
            onHandsChange={onHandsChange}
          />
        </div>
      </div>

      {/* Selected Hands List */}
      {selectedHands.size > 0 && (
        <div className="bg-white p-2 rounded-lg border border-gray-200 shadow-md">
          <h3 className="text-sm font-semibold mb-2 text-gray-800">
            Selected Hands ({selectedHands.size})
          </h3>
          <div className="bg-gray-50 p-2 rounded border border-gray-300 max-h-64 overflow-y-auto">
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
    </div>
  );
}



