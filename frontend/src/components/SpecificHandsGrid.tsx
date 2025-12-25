import './SpecificHandsGrid.css';

interface HandStrategy {
  hand: string;
  raise: number;
  call: number;
  fold: number;
}

interface SpecificHandsGridProps {
  hands: HandStrategy[];
  category: string;
}

// Map backend suit format to Unicode symbols
const SUIT_SYMBOLS: { [key: string]: string } = {
  's': '♠',
  'h': '♥',
  'd': '♦',
  'c': '♣'
};

const SUIT_COLORS: { [key: string]: string } = {
  's': 'black',
  'h': 'red',
  'd': 'red',
  'c': 'black'
};

export default function SpecificHandsGrid({ hands, category }: SpecificHandsGridProps) {
  // Convert hand notation to display format with suits
  const formatHandDisplay = (hand: string) => {
    const rank1 = hand[0];
    const suit1 = hand[1];
    const rank2 = hand[2];
    const suit2 = hand[3];

    return (
      <span className="hand-display">
        <span style={{ color: SUIT_COLORS[suit1] }}>
          {rank1}{SUIT_SYMBOLS[suit1]}
        </span>
        <span style={{ color: SUIT_COLORS[suit2] }}>
          {rank2}{SUIT_SYMBOLS[suit2]}
        </span>
      </span>
    );
  };

  // Calculate grid dimensions based on number of hands
  const getGridDimensions = (count: number): { cols: number; rows: number } => {
    if (count <= 4) return { cols: 2, rows: 2 };
    if (count <= 6) return { cols: 3, rows: 2 };
    if (count <= 9) return { cols: 3, rows: 3 };
    if (count <= 12) return { cols: 4, rows: 3 };
    return { cols: 4, rows: 4 };
  };

  const { cols, rows } = getGridDimensions(hands.length);

  // Calculate cell size based on grid dimensions to maintain consistent overall size
  const getCellSize = (cols: number, rows: number): number => {
    // Target overall grid size: ~320px x 320px
    const targetWidth = 320;
    const targetHeight = 320;
    const gap = 4; // matches CSS gap
    
    const cellWidth = (targetWidth - (gap * (cols - 1))) / cols;
    const cellHeight = (targetHeight - (gap * (rows - 1))) / rows;
    
    // Use the smaller dimension to keep cells square
    return Math.floor(Math.min(cellWidth, cellHeight));
  };

  const cellSize = getCellSize(cols, rows);

  return (
    <div className="specific-hands-grid-container">
      <h3>{category} - All Combinations</h3>
      <div 
        className="specific-hands-grid"
        style={{
          gridTemplateColumns: `repeat(${cols}, ${cellSize}px)`,
          gridTemplateRows: `repeat(${rows}, ${cellSize}px)`
        }}
      >
        {hands.map((hand, idx) => (
          <div key={idx} className="specific-hand-cell">
            <div className="hand-label-top">
              {formatHandDisplay(hand.hand)}
            </div>
            
            <div className="strategy-bar-specific">
              <div
                className="raise-bar"
                style={{ height: `${hand.raise * 100}%` }}
              />
              <div
                className="call-bar"
                style={{ height: `${hand.call * 100}%` }}
              />
              <div
                className="fold-bar"
                style={{ height: `${hand.fold * 100}%` }}
              />
            </div>

            <div className="strategy-percentages">
              <span className="raise-pct">{(hand.raise * 100).toFixed(0)}%</span>
              <span className="call-pct">{(hand.call * 100).toFixed(0)}%</span>
              <span className="fold-pct">{(hand.fold * 100).toFixed(0)}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}