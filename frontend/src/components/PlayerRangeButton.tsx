import { useState, useEffect } from 'react';
import RangeBuilder from './RangeBuilder';
import { rangesApi } from '../api/ranges';

interface PlayerRangeButtonProps {
    player: string;
    selectedHands: string[];
    onRangeChange: (hands: string[]) => void;
}

export default function PlayerRangeButton({ player, selectedHands, onRangeChange }: PlayerRangeButtonProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [localSelectedHands, setLocalSelectedHands] = useState<Set<string>>(new Set());

    // Initialize local state when modal opens
    useEffect(() => {
        if (isOpen) {
            setLocalSelectedHands(new Set(selectedHands));
        }
    }, [isOpen, selectedHands]);

    const handleDone = async () => {
        // Save immediately to parent
        const handsArray = Array.from(localSelectedHands);
        onRangeChange(handsArray);
        
        // Close modal
        setIsOpen(false);

        // creating range on backend for validation
        rangesApi.createRange(player, handsArray)
            .then(response => {
                console.log(`${player} range validated:`, response);
            })
            .catch(error => {
                console.warn(`${player} range validation failed:`, error);
            });
    };

    const handleClose = () => {
        // X button: save without validation
        const handsArray = Array.from(localSelectedHands);
        onRangeChange(handsArray);
        setIsOpen(false);
    };

    return (
        <>
      <button
        onClick={() => setIsOpen(true)}
        className="range-button"
      >
        {player} Range
      </button>

      {isOpen && (
        <div className="modal-overlay" onClick={handleClose}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Select {player} Range</h2>
              <button onClick={handleClose} className="close-button">×</button>
            </div>
            <RangeBuilder
              player={player}
              selectedHands={localSelectedHands}
              onHandsChange={setLocalSelectedHands}
            />
            <div className="modal-footer">
              <button 
                onClick={handleDone} 
                disabled={localSelectedHands.size === 0}
                className="done-button"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}