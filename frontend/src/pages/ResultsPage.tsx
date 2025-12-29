import { useLocation, useNavigate } from 'react-router-dom';
import type { SolveResponse } from '../api/solver';
import TreeExplorer from '../components/TreeExplorer';
import './ResultsPage.css';

export default function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result as SolveResponse | null;
  const flop = location.state?.flop as string[] | null;

  if (!result) {
    return (
      <div className="results-page">
        <h1>No Results Found</h1>
        <button onClick={() => navigate('/')} className="back-button">
          Go Back to Setup
        </button>
      </div>
    );
  }

  // Get suit class for card display styling
  const getSuitClass = (card: string): string => {
    if (card.length < 2) return '';
    const suit = card[1].toLowerCase();
    switch (suit) {
      case 'h': return 'hearts';
      case 'd': return 'diamonds';
      case 'c': return 'clubs';
      case 's': return 'spades';
      default: return '';
    }
  };

  // Get Unicode suit symbol
  const getSuitSymbol = (card: string): string => {
    if (card.length < 2) return '';
    const suit = card[1].toLowerCase();
    switch (suit) {
      case 'h': return '♥';
      case 'd': return '♦';
      case 'c': return '♣';
      case 's': return '♠';
      default: return '';
    }
  };

  // Format card display with rank and suit symbol
  const formatCard = (card: string): { rank: string; suit: string } => {
    if (card.length < 2) return { rank: '', suit: '' };
    return {
      rank: card[0],
      suit: getSuitSymbol(card)
    };
  };

  return (
    <div className="results-page">
      <div className="results-header">
        <h1>Solver Results</h1>
        <button onClick={() => navigate('/')} className="back-button">
          New Analysis
        </button>
      </div>

      {/* Flop Display */}
      {flop && flop.length > 0 && (
        <div className="flop-display">
          <span className="flop-label">Board:</span>
          <div className="flop-cards">
            {flop.map((card, idx) => {
              const { rank, suit } = formatCard(card);
              return (
                <span key={idx} className={`card ${getSuitClass(card)}`}>
                  <span className="card-rank">{rank}</span>
                  <span className="card-suit">{suit}</span>
                </span>
              );
            })}
          </div>
        </div>
      )}

      {/* Tree Explorer */}
      {result.tree_data ? (
        <div className="tree-explorer-section">
          <h2 className="section-title">Game Tree Explorer</h2>
          <TreeExplorer 
            treeData={result.tree_data} 
          />
        </div>
      ) : (
        <div className="tree-explorer-placeholder">
          <h3>Game Tree Explorer</h3>
          <p>Tree data not available - solve again to enable tree navigation</p>
        </div>
      )}
    </div>
  );
}