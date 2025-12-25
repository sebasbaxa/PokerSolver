import { useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import type { SolveResponse } from '../api/solver';
import SpecificHandsGrid from '../components/SpecificHandsGrid';
import './ResultsPage.css';

interface HandStrategy {
  hand: string;
  raise: number;
  call: number;
  fold: number;
}

interface CategoryStrategy {
  category: string;
  avgRaise: number;
  avgCall: number;
  avgFold: number;
  hands: HandStrategy[];
}

export default function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result as SolveResponse | null;
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

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

  // Parse strategy data and group by hand category
  const parseStrategy = (strategy: any[]): Map<string, CategoryStrategy> => {
    const categoryMap = new Map<string, CategoryStrategy>();

    console.log('Parsing strategy:', strategy);

    strategy.forEach((item) => {
      const hand = item.hand;
      const category = getHandCategory(hand);
      
      const handStrategy: HandStrategy = {
        hand: hand,
        raise: item.raise || 0,
        call: item.call || 0,
        fold: item.fold || 0,
      };

      console.log('Hand:', hand, 'Category:', category, 'Strategy:', handStrategy);

      if (!categoryMap.has(category)) {
        categoryMap.set(category, {
          category,
          avgRaise: 0,
          avgCall: 0,
          avgFold: 0,
          hands: [],
        });
      }

      categoryMap.get(category)!.hands.push(handStrategy);
    });

    // Calculate averages for each category
    categoryMap.forEach((cat) => {
      const count = cat.hands.length;
      cat.avgRaise = cat.hands.reduce((sum, h) => sum + h.raise, 0) / count;
      cat.avgCall = cat.hands.reduce((sum, h) => sum + h.call, 0) / count;
      cat.avgFold = cat.hands.reduce((sum, h) => sum + h.fold, 0) / count;
    });

    console.log('Category data:', categoryMap);
    return categoryMap;
  };

  // Convert specific hand to category (e.g., "AsAh" -> "AA")
  const getHandCategory = (hand: string): string => {
    const rank1 = hand[0];
    const suit1 = hand[1];
    const rank2 = hand[2];
    const suit2 = hand[3];

    if (rank1 === rank2) {
      return `${rank1}${rank2}`; // Pocket pair
    }

    const suited = suit1 === suit2;
    const [highRank, lowRank] = [rank1, rank2].sort((a, b) => 
      getRankValue(b) - getRankValue(a)
    );

    return `${highRank}${lowRank}${suited ? 's' : 'o'}`;
  };

  const getRankValue = (rank: string): number => {
    const ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'];
    return ranks.indexOf(rank);
  };

  // Generate 13x13 grid layout
  const generateGrid = (): (string | null)[][] => {
    const ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'];
    const grid: (string | null)[][] = [];

    for (let row = 0; row < 13; row++) {
      const gridRow: (string | null)[] = [];
      for (let col = 0; col < 13; col++) {
        if (row === col) {
          // Pocket pairs on diagonal
          gridRow.push(`${ranks[row]}${ranks[col]}`);
        } else if (row < col) {
          // Suited hands above diagonal
          gridRow.push(`${ranks[row]}${ranks[col]}s`);
        } else {
          // Offsuit hands below diagonal
          gridRow.push(`${ranks[col]}${ranks[row]}o`);
        }
      }
      grid.push(gridRow);
    }

    return grid;
  };

  const categoryData = parseStrategy(result.oop_strategy);
  const grid = generateGrid();
  const selectedCategoryData = selectedCategory ? categoryData.get(selectedCategory) : null;

  return (
    <div className="results-page">
      <div className="results-header">
        <h1>Solver Results</h1>
        <button onClick={() => navigate('/')} className="back-button">
          New Analysis
        </button>
      </div>

      {/* Placeholder for Tree Explorer */}
      <div className="tree-explorer-placeholder">
        <h3>Tree Explorer (Coming Soon)</h3>
        <p>Navigate through the game tree to view strategies at different nodes</p>
      </div>

      <div className="results-content">
        {/* Main Strategy Grid */}
        <div className="strategy-grid-container">
          <h2>OOP Strategy Overview</h2>
          <div className="hand-category-grid">
            {grid.map((row, rowIdx) => (
              <div key={rowIdx} className="grid-row">
                {row.map((category, colIdx) => {
                  const catData = category ? categoryData.get(category) : null;
                  const isInRange = catData && catData.hands.length > 0;

                  return (
                    <div
                      key={`${rowIdx}-${colIdx}`}
                      className={`grid-cell ${isInRange ? 'in-range' : 'out-of-range'} ${
                        selectedCategory === category ? 'selected' : ''
                      }`}
                      onClick={() => isInRange && setSelectedCategory(category)}
                    >
                      <div className="cell-label">{category}</div>
                      {isInRange && catData && (
                        <div className="strategy-bar">
                          <div
                            className="raise-bar"
                            style={{ height: `${catData.avgRaise * 100}%` }}
                            title={`Raise: ${(catData.avgRaise * 100).toFixed(1)}%`}
                          />
                          <div
                            className="call-bar"
                            style={{ height: `${catData.avgCall * 100}%` }}
                            title={`Call: ${(catData.avgCall * 100).toFixed(1)}%`}
                          />
                          <div
                            className="fold-bar"
                            style={{ height: `${catData.avgFold * 100}%` }}
                            title={`Fold: ${(catData.avgFold * 100).toFixed(1)}%`}
                          />
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            ))}
          </div>
        </div>

        {/* Detailed Hand View */}
        <div className="detailed-hand-view">
          {selectedCategoryData ? (
            <>
              <h2>{selectedCategoryData.category} Details</h2>
              <div className="category-summary">
                <div className="action-stat raise">
                  Raise: {(selectedCategoryData.avgRaise * 100).toFixed(1)}%
                </div>
                <div className="action-stat call">
                  Call: {(selectedCategoryData.avgCall * 100).toFixed(1)}%
                </div>
                <div className="action-stat fold">
                  Fold: {(selectedCategoryData.avgFold * 100).toFixed(1)}%
                </div>
              </div>
              <SpecificHandsGrid 
                hands={selectedCategoryData.hands} 
                category={selectedCategoryData.category}
              />
            </>
          ) : (
            <div className="no-selection">
              <p>Click on a hand category to view detailed breakdown</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}