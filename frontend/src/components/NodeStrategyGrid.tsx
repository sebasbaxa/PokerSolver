import { useState, useMemo } from 'react';
import type { HandStrategy } from '../types/tree';
import './NodeStrategyGrid.css';

interface NodeStrategyGridProps {
    strategies: HandStrategy[];
    player: 'OOP' | 'IP';
    isActingPlayer: boolean;
}

interface CategoryData {
    category: string;
    avgRaise: number;
    avgCall: number;
    avgFold: number;
    avgEv: number;
    hands: HandStrategy[];
}

export default function NodeStrategyGrid({ strategies, player, isActingPlayer }: NodeStrategyGridProps) {
    const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

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

    // Parse strategies and group by category
    const categoryData = useMemo(() => {
        const categoryMap = new Map<string, CategoryData>();

        strategies.forEach((item) => {
            const category = getHandCategory(item.hand);

            if (!categoryMap.has(category)) {
                categoryMap.set(category, {
                    category,
                    avgRaise: 0,
                    avgCall: 0,
                    avgFold: 0,
                    avgEv: 0,
                    hands: [],
                });
            }

            categoryMap.get(category)!.hands.push(item);
        });

        // Calculate averages
        categoryMap.forEach((cat) => {
            const count = cat.hands.length;
            cat.avgRaise = cat.hands.reduce((sum, h) => sum + h.raise, 0) / count;
            cat.avgCall = cat.hands.reduce((sum, h) => sum + h.call, 0) / count;
            cat.avgFold = cat.hands.reduce((sum, h) => sum + h.fold, 0) / count;
            cat.avgEv = cat.hands.reduce((sum, h) => sum + h.ev, 0) / count;
        });

        return categoryMap;
    }, [strategies]);

    // Generate 13x13 grid layout
    const grid = useMemo(() => {
        const ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'];
        const gridData: (string | null)[][] = [];

        for (let row = 0; row < 13; row++) {
            const gridRow: (string | null)[] = [];
            for (let col = 0; col < 13; col++) {
                if (row === col) {
                    gridRow.push(`${ranks[row]}${ranks[col]}`);
                } else if (row < col) {
                    gridRow.push(`${ranks[row]}${ranks[col]}s`);
                } else {
                    gridRow.push(`${ranks[col]}${ranks[row]}o`);
                }
            }
            gridData.push(gridRow);
        }

        return gridData;
    }, []);

    const selectedCategoryData = selectedCategory ? categoryData.get(selectedCategory) : null;

    // Format EV for display
    const formatEv = (ev: number): string => {
        if (ev >= 0) return `+${ev.toFixed(2)}`;
        return ev.toFixed(2);
    };

    return (
        <div className="node-strategy-grid">
            <div className="grid-header">
                <h3>
                    {player} Strategy
                    {isActingPlayer && <span className="acting-badge">Acting</span>}
                </h3>
                {strategies.length === 0 && (
                    <p className="no-hands-message">No hands in range for {player}</p>
                )}
            </div>

            <div className="grid-content">
                {/* Main Strategy Grid */}
                <div className="category-grid-container">
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
                                                <>
                                                    <div className="strategy-bar">
                                                        <div
                                                            className="raise-bar"
                                                            style={{ width: `${catData.avgRaise * 100}%` }}
                                                        />
                                                        <div
                                                            className="call-bar"
                                                            style={{ width: `${catData.avgCall * 100}%` }}
                                                        />
                                                        <div
                                                            className="fold-bar"
                                                            style={{ width: `${catData.avgFold * 100}%` }}
                                                        />
                                                    </div>
                                                    <div className="cell-ev" title={`EV: ${formatEv(catData.avgEv)}`}>
                                                        {formatEv(catData.avgEv)}
                                                    </div>
                                                </>
                                            )}
                                        </div>
                                    );
                                })}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Detailed Hand View */}
                <div className="detailed-view">
                    {selectedCategoryData ? (
                        <div className="category-details">
                            <h4>{selectedCategoryData.category} Details</h4>
                            <div className="category-summary">
                                <div className="action-stat raise">
                                    <span className="stat-label">Raise</span>
                                    <span className="stat-value">{(selectedCategoryData.avgRaise * 100).toFixed(1)}%</span>
                                </div>
                                <div className="action-stat call">
                                    <span className="stat-label">Call</span>
                                    <span className="stat-value">{(selectedCategoryData.avgCall * 100).toFixed(1)}%</span>
                                </div>
                                <div className="action-stat fold">
                                    <span className="stat-label">Fold</span>
                                    <span className="stat-value">{(selectedCategoryData.avgFold * 100).toFixed(1)}%</span>
                                </div>
                                <div className="action-stat ev">
                                    <span className="stat-label">EV</span>
                                    <span className="stat-value">{formatEv(selectedCategoryData.avgEv)}</span>
                                </div>
                            </div>
                            
                            <div className="hands-list">
                                <h5>Individual Hands ({selectedCategoryData.hands.length})</h5>
                                <div className="hands-table">
                                    <div className="table-header">
                                        <span>Hand</span>
                                        <span>Raise</span>
                                        <span>Call</span>
                                        <span>Fold</span>
                                        <span>EV</span>
                                    </div>
                                    {selectedCategoryData.hands.map((hand) => (
                                        <div key={hand.hand} className="table-row">
                                            <span className="hand-name">{hand.hand}</span>
                                            <span className="raise-value">{(hand.raise * 100).toFixed(1)}%</span>
                                            <span className="call-value">{(hand.call * 100).toFixed(1)}%</span>
                                            <span className="fold-value">{(hand.fold * 100).toFixed(1)}%</span>
                                            <span className={`ev-value ${hand.ev >= 0 ? 'positive' : 'negative'}`}>
                                                {formatEv(hand.ev)}
                                            </span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="no-selection">
                            <p>Click on a hand category to view detailed breakdown</p>
                        </div>
                    )}
                </div>
            </div>

            {/* Strategy Legend */}
            <div className="strategy-legend">
                <div className="legend-item">
                    <div className="legend-color raise"></div>
                    <span>Raise/Bet</span>
                </div>
                <div className="legend-item">
                    <div className="legend-color call"></div>
                    <span>Call/Check</span>
                </div>
                <div className="legend-item">
                    <div className="legend-color fold"></div>
                    <span>Fold</span>
                </div>
            </div>
        </div>
    );
}
