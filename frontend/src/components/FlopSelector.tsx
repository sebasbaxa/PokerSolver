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

export default function FlopSelector({ selectedCards, onCardsChange }: FlopSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);

  const handleCardClick = (card: string) => {
    if (selectedCards.includes(card)) {
      // Remove card if already selected
      onCardsChange(selectedCards.filter(c => c !== card));
    } else if (selectedCards.length < 3) {
      // Add card if less than 3 selected
      onCardsChange([...selectedCards, card]);
    }
  };

  const clearSelection = () => {
    onCardsChange([]);
  };

  return (
    <div className="flop-selector">
      <div className="flop-display">
        {selectedCards.length === 0 ? (
          <div className="empty-flop">Select flop cards</div>
        ) : (
          <div className="selected-cards">
            {selectedCards.map((card, idx) => (
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
        {selectedCards.length > 0 && (
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
                const card = `${rank}${suit}`;
                const isSelected = selectedCards.includes(card);
                const isDisabled = !isSelected && selectedCards.length >= 3;
                
                return (
                  <button
                    key={card}
                    className={`card-button ${isSelected ? 'selected' : ''} ${isDisabled ? 'disabled' : ''}`}
                    onClick={() => handleCardClick(card)}
                    disabled={isDisabled}
                    style={{ color: SUIT_COLORS[suit] }}
                  >
                    {card}
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