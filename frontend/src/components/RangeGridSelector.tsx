import { useState } from 'react';
import GridCell from './GridCell';
import { RANKS, gridToHand } from '../utils/handUtils';

interface RangeGridSelectorProps {
  selectedHands: Set<string>;
  onHandsChange: (hands: Set<string>) => void;
}

export default function RangeGridSelector({ selectedHands, onHandsChange }: RangeGridSelectorProps) {
  const [hoveredHand, setHoveredHand] = useState<string | null>(null);

  const handleCellClick = (hand: string) => {
    // Toggle selection on click
    const newSelection = new Set(selectedHands);
    if (newSelection.has(hand)) {
      newSelection.delete(hand);
    } else {
      newSelection.add(hand);
    }
    onHandsChange(newSelection);
  };

  const handleMouseLeave = () => {
    setHoveredHand(null);
  };

  return (
    <div className="range-grid-selector">
      {/* Grid container */}
      <div className="range-grid-container">
        {/* Column labels */}
        <div className="grid-labels-row">
          <div className="corner-cell" />
          {RANKS.map((rank) => (
            <div key={rank} className="column-label">
              {rank}
            </div>
          ))}
        </div>

        {/* Grid rows */}
        {RANKS.map((rowRank, rowIndex) => (
          <div key={rowRank} className="grid-data-row">
            {/* Row label */}
            <div className="row-label">
              {rowRank}
            </div>

            {/* Grid cells */}
            {RANKS.map((_, colIndex) => {
              const hand = gridToHand(rowIndex, colIndex);
              return (
                <GridCell
                  key={`${rowIndex}-${colIndex}`}
                  hand={hand}
                  row={rowIndex}
                  col={colIndex}
                  isSelected={selectedHands.has(hand)}
                  isHovered={hoveredHand === hand}
                  onMouseEnter={() => setHoveredHand(hand)}
                  onMouseLeave={handleMouseLeave}
                  onClick={() => handleCellClick(hand)}
                />
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}
