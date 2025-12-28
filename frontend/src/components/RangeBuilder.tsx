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
    <div className="range-builder">
      {/* Controls Section */}
      <div className="range-builder-controls">
        {/* Player display (read-only) */}
        <div className="player-display">
          <label>Player:</label>
          <span className="player-name">{player}</span>
        </div>

        {/* Selection Summary */}
        <div className="selection-summary">
          <div className="summary-item hands">
            <span className="label">Selected: </span>
            <span className="value">{selectedHands.size} hands</span>
          </div>
          <div className="summary-item combos">
            <span className="label">Combos: </span>
            <span className="value">{totalCombos} / 1326</span>
          </div>
          <div className="summary-item percentage">
            <span className="label">Range: </span>
            <span className="value">{percentage}%</span>
          </div>
        </div>

        {/* Clear All Button */}
        <div className="range-actions">
          <button
            onClick={handleClearAll}
            disabled={selectedHands.size === 0}
            className="clear-button"
            style={{ fontSize: '15px' }}
          >
            Clear
          </button>
        </div>
      </div>

      {/* Grid Section */}
      <div className="range-grid-section">
        <h3>Select Hands</h3>
        <div className="grid-wrapper">
          <RangeGridSelector
            selectedHands={selectedHands}
            onHandsChange={onHandsChange}
          />
        </div>
      </div>

      {/* Selected Hands List */}
      {selectedHands.size > 0 && (
        <div className="selected-hands-list">
          <h3>Selected Hands ({selectedHands.size})</h3>
          <div className="hands-container">
            {Array.from(selectedHands).sort().map((hand) => (
              <span key={hand} className="hand-tag">
                {hand}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}



