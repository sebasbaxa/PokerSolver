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
    <div className="relative">
      {/* Grid container with fixed width to prevent layout shift */}
      <div style={{ 
        display: 'inline-block', 
        backgroundColor: '#FFFFFF', 
        padding: '16px', 
        borderRadius: '8px', 
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        width: 'fit-content',
        minWidth: '750px',
      }}>
        {/* Column labels */}
        <div style={{ display: 'grid', gridTemplateColumns: '32px repeat(13, 50px)', gap: 0, marginBottom: '4px' }}>
          <div style={{ width: '32px' }} /> {/* Empty corner */}
          {RANKS.map((rank) => (
            <div key={rank} style={{ textAlign: 'center', fontSize: '12px', fontWeight: 'bold', color: '#4B5563', paddingBottom: '4px' }}>
              {rank}
            </div>
          ))}
        </div>

        {/* Grid rows */}
        {RANKS.map((rowRank, rowIndex) => (
          <div key={rowRank} style={{ display: 'grid', gridTemplateColumns: '32px repeat(13, 50px)', gap: 0 }}>
            {/* Row label */}
            <div style={{ width: '32px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '12px', fontWeight: 'bold', color: '#4B5563', paddingRight: '4px' }}>
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
