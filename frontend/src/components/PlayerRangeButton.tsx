import { useState } from 'react';
import RangeBuilder from './RangeBuilder';

interface PlayerRangeButtonProps {
    player: 'IP' | 'OOP';
    selectedHands: string[];
    onRangeChange: (hands: string[]) => void;
}

export default function PlayerRangeButton({ player, selectedHands, onRangeChange }: PlayerRangeButtonProps) {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <>
      <button
        onClick={() => setIsOpen(true)}
        className="range-button"
      >
        {player} Range ({selectedHands.length} hands)
      </button>

      {isOpen && (
        <div className="modal-overlay" onClick={() => setIsOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Select {player} Range</h2>
              <button onClick={() => setIsOpen(false)} className="close-button">×</button>
            </div>
            <RangeBuilder
              player={player}
              selectedHands={selectedHands}
              onRangeChange={onRangeChange}
            />
            <div className="modal-footer">
              <button onClick={() => setIsOpen(false)} className="done-button">Done</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}