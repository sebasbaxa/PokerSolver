import { useState } from 'react';
import './FlopSelector.css';

interface FlopSelectorProps {
  selectedCards: string[];
  onCardsChange: (cards: string[]) => void;
}

const RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'];
const SUITS = ['♠', '♥', '♦', '♣'];
const SUIT_COLORS: { [key: string]: string } = {
  '♠': 'black',
  '♣': 'black',
  '♥': 'red',
  '♦': 'red'
};

// Map Unicode suits to backend format
const SUIT_TO_BACKEND: { [key: string]: string } = {
  '♠': 's',
  '♥': 'h',
  '♦': 'd',
  '♣': 'c'
};

// Map backend format to Unicode suits
const BACKEND_TO_SUIT: { [key: string]: string } = {
  's': '♠',
  'h': '♥',
  'd': '♦',
  'c': '♣'
};

// Convert display format (e.g., "A♠") to backend format (e.g., "As")
const toBackendFormat = (displayCard: string): string => {
  const rank = displayCard[0];
  const suit = displayCard[1];
  return `${rank}${SUIT_TO_BACKEND[suit]}`;
};

// Convert backend format (e.g., "As") to display format (e.g., "A♠")
const toDisplayFormat = (backendCard: string): string => {
  const rank = backendCard[0];
  const suit = backendCard[1];
  return `${rank}${BACKEND_TO_SUIT[suit]}`;
};

export default function FlopSelector({ selectedCards, onCardsChange }: FlopSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);

  // Convert backend format cards to display format for internal use
  const displayCards = selectedCards.map(toDisplayFormat);

  const handleCardClick = (displayCard: string) => {
    if (displayCards.includes(displayCard)) {
      // Remove card if already selected - convert to backend format
      const backendCard = toBackendFormat(displayCard);
      onCardsChange(selectedCards.filter(c => c !== backendCard));
    } else if (selectedCards.length < 3) {
      // Add card if less than 3 selected - convert to backend format
      const backendCard = toBackendFormat(displayCard);
      onCardsChange([...selectedCards, backendCard]);
    }
  };

  const clearSelection = () => {
    onCardsChange([]);
  };

  return (
    <div className="flop-selector">
      <div className="flop-display">
        {displayCards.length === 0 ? (
          <div className="empty-flop">Select flop cards</div>
        ) : (
          <div className="selected-cards">
            {displayCards.map((card, idx) => (
              <div key={idx} className={`flop-card ${SUIT_COLORS[card[1]]}`}>
                {card}
              </div>
            ))}
          </div>
        )}
        <button 
          className="select-flop-button" 
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? 'Close' : 'Select Cards'}
        </button>
        {displayCards.length > 0 && (
          <button className="clear-button" onClick={clearSelection}>
            Clear
          </button>
        )}
      </div>

      {isOpen && (
        <div className="card-grid">
          {RANKS.map(rank => (
            <div key={rank} className="rank-row">
              {SUITS.map(suit => {
                const displayCard = `${rank}${suit}`;
                const isSelected = displayCards.includes(displayCard);
                const isDisabled = !isSelected && displayCards.length >= 3;
                
                return (
                  <button
                    key={displayCard}
                    className={`card-button ${isSelected ? 'selected' : ''} ${isDisabled ? 'disabled' : ''}`}
                    onClick={() => handleCardClick(displayCard)}
                    disabled={isDisabled}
                    style={{ color: SUIT_COLORS[suit] }}
                  >
                    {displayCard}
                  </button>
                );
              })}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}