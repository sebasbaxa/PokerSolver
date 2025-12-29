import { useState, useCallback, useMemo } from 'react';
import type { TreeNodeData } from '../types/tree';
import NodeStrategyGrid from './NodeStrategyGrid';
import { getHandCategoryFromSpecific } from '../utils/handUtils';
import './TreeExplorer.css';

interface TreeExplorerProps {
    treeData: TreeNodeData;
}

export default function TreeExplorer({ treeData }: TreeExplorerProps) {
    const [currentNode, setCurrentNode] = useState<TreeNodeData>(treeData);
    const [handFilter, setHandFilter] = useState<string>('');
    const [showRangeModal, setShowRangeModal] = useState<'OOP' | 'IP' | null>(null);

    // Extract ranges from root node (all hands in strategy = player's range)
    const ranges = useMemo(() => {
        const oopHands = treeData.oop_strategy.map(s => s.hand);
        const ipHands = treeData.ip_strategy.map(s => s.hand);
        return { OOP: oopHands, IP: ipHands };
    }, [treeData]);

    // Group hands by category for range display
    const groupHandsByCategory = useCallback((hands: string[]) => {
        const categories: Record<string, string[]> = {};
        for (const hand of hands) {
            const category = getHandCategoryFromSpecific(hand);
            if (!categories[category]) {
                categories[category] = [];
            }
            categories[category].push(hand);
        }
        return categories;
    }, []);

    // Navigate to a node by following the path through the tree structure
    const getNodeByPath = useCallback((path: string): TreeNodeData => {
        if (path === 'root') return treeData;
        
        const actions = path.split('->').slice(1); // Remove 'root'
        let node = treeData;
        
        for (const action of actions) {
            if (node.children[action]) {
                node = node.children[action];
            } else {
                throw new Error(`Invalid path: ${path}`);
            }
        }
        
        return node;
    }, [treeData]);

    // Parse breadcrumb from path
    const breadcrumbs = currentNode.path.split('->');

    // Navigate to a child node
    const navigateToAction = useCallback((action: string) => {
        if (currentNode.children[action]) {
            setCurrentNode(currentNode.children[action]);
        }
    }, [currentNode]);

    // Navigate to a specific path (for breadcrumb clicks)
    const navigateToPath = useCallback((path: string) => {
        try {
            const node = getNodeByPath(path);
            setCurrentNode(node);
        } catch (err) {
            console.error('Failed to navigate:', err);
        }
    }, [getNodeByPath]);

    // Go back one step
    const goBack = useCallback(() => {
        if (breadcrumbs.length <= 1) return;
        const parentPath = breadcrumbs.slice(0, -1).join('->');
        navigateToPath(parentPath);
    }, [breadcrumbs, navigateToPath]);

    // Reset to root
    const resetToRoot = useCallback(() => {
        setCurrentNode(treeData);
    }, [treeData]);

    // Get the acting player at current node
    const actingPlayer = currentNode.turn;

    // Get strategies for the acting player
    const strategies = actingPlayer === 'OOP' 
        ? currentNode.oop_strategy 
        : currentNode.ip_strategy;

    // Apply hand filter - filter by hand category (e.g., "KK", "AKs", "AA, KK, QQ")
    const filteredStrategies = handFilter.trim()
        ? strategies.filter(s => {
            const category = getHandCategoryFromSpecific(s.hand);
            const categoryLower = category.toLowerCase();
            
            // Support comma-separated filters like "AA, KK, QQ"
            const filters = handFilter.toLowerCase().split(',').map(f => f.trim()).filter(f => f);
            
            return filters.some(filter => {
                // Exact match for full category (e.g., "KK" matches "KK", "AKs" matches "AKs")
                if (categoryLower === filter) return true;
                // Partial match: "AK" matches both "AKs" and "AKo"
                if (filter.length === 2 && categoryLower.startsWith(filter)) return true;
                return false;
            });
        })
        : strategies;

    // Format action labels
    const formatAction = (action: string): string => {
        const labels: Record<string, string> = {
            fold: 'Fold',
            call: 'Call/Check',
            raise: 'Bet/Raise',
        };
        return labels[action] || action;
    };

    return (
        <div className="tree-explorer">
            {/* Navigation Header */}
            <div className="tree-nav-header">
                <div className="breadcrumb-container">
                    <button 
                        className="nav-button reset-button"
                        onClick={resetToRoot}
                        disabled={currentNode.path === 'root'}
                    >
                        ⟲ Reset
                    </button>
                    <button 
                        className="nav-button back-button"
                        onClick={goBack}
                        disabled={breadcrumbs.length <= 1}
                    >
                        ← Back
                    </button>
                    <div className="breadcrumbs">
                        {breadcrumbs.map((crumb, idx) => {
                            const path = breadcrumbs.slice(0, idx + 1).join('->');
                            const isLast = idx === breadcrumbs.length - 1;
                            return (
                                <span key={path}>
                                    <button 
                                        className={`breadcrumb ${isLast ? 'current' : ''}`}
                                        onClick={() => navigateToPath(path)}
                                        disabled={isLast}
                                    >
                                        {crumb === 'root' ? 'Root' : formatAction(crumb)}
                                    </button>
                                    {!isLast && <span className="breadcrumb-separator">→</span>}
                                </span>
                            );
                        })}
                    </div>
                </div>
            </div>

            {/* Node Info Panel */}
            <div className="node-info-panel">
                <div className="node-info-grid">
                    <div className={`info-item turn ${currentNode.turn.toLowerCase()}`}>
                        <span className="info-label">Turn</span>
                        <span className="info-value">{currentNode.turn}</span>
                    </div>
                    <div className="info-item">
                        <span className="info-label">Street</span>
                        <span className="info-value">{currentNode.street}</span>
                    </div>
                    <div className="info-item">
                        <span className="info-label">Pot</span>
                        <span className="info-value">{currentNode.pot} BB</span>
                    </div>
                    <div className="info-item">
                        <span className="info-label">OOP Stack</span>
                        <span className="info-value">{currentNode.stacks.OOP} BB</span>
                    </div>
                    <div className="info-item">
                        <span className="info-label">IP Stack</span>
                        <span className="info-value">{currentNode.stacks.IP} BB</span>
                    </div>
                    <div className="info-item">
                        <span className="info-label">State</span>
                        <span className={`info-value state-${currentNode.state}`}>
                            {currentNode.state}
                        </span>
                    </div>
                </div>
            </div>

            {/* Action Buttons */}
            {!currentNode.isTerminal && (
                <div className="action-buttons-container">
                    <h4>Navigate to Action:</h4>
                    <div className="action-buttons">
                        {Object.keys(currentNode.children).map(action => (
                            <button
                                key={action}
                                className={`action-button action-${action}`}
                                onClick={() => navigateToAction(action)}
                            >
                                {formatAction(action)}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Terminal Node Message */}
            {currentNode.isTerminal && (
                <div className={`terminal-message state-${currentNode.state}`}>
                    {currentNode.state === 'fold' 
                        ? ' Player Folded - Terminal Node' 
                        : ' Showdown - Terminal Node'}
                </div>
            )}

            {/* Strategy Controls */}
            <div className="strategy-controls">
                <div className="range-buttons">
                    <span className="control-label">View Ranges:</span>
                    <button
                        className={`range-button oop ${showRangeModal === 'OOP' ? 'active' : ''}`}
                        onClick={() => setShowRangeModal(showRangeModal === 'OOP' ? null : 'OOP')}
                    >
                        OOP Range ({ranges.OOP.length})
                    </button>
                    <button
                        className={`range-button ip ${showRangeModal === 'IP' ? 'active' : ''}`}
                        onClick={() => setShowRangeModal(showRangeModal === 'IP' ? null : 'IP')}
                    >
                        IP Range ({ranges.IP.length})
                    </button>
                </div>
                <div className="hand-filter">
                    <span className="control-label">Filter Hands:</span>
                    <input
                        type="text"
                        placeholder="e.g. AA, AKs, QJ..."
                        value={handFilter}
                        onChange={(e) => setHandFilter(e.target.value)}
                        className="filter-input"
                    />
                    {handFilter && (
                        <button 
                            className="clear-filter"
                            onClick={() => setHandFilter('')}
                        >
                            ✕
                        </button>
                    )}
                </div>
            </div>

            {/* Range Modal */}
            {showRangeModal && (
                <div className="range-modal">
                    <div className="range-modal-header">
                        <h4>{showRangeModal} Range ({ranges[showRangeModal].length} combos)</h4>
                        <button 
                            className="close-modal"
                            onClick={() => setShowRangeModal(null)}
                        >
                            ✕
                        </button>
                    </div>
                    <div className="range-modal-content">
                        {Object.entries(groupHandsByCategory(ranges[showRangeModal])).map(([category, hands]) => (
                            <div key={category} className="range-category">
                                <span className="category-name">{category}</span>
                                <span className="category-count">({hands.length})</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Strategy Grid */}
            <NodeStrategyGrid 
                strategies={filteredStrategies}
                player={actingPlayer}
                isActingPlayer={true}
            />
        </div>
    );
}
