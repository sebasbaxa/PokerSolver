// Types for the game tree explorer

export interface HandStrategy {
    hand: string;
    fold: number;
    call: number;
    raise: number;
    ev: number;
}

export interface TreeNodeData {
    // Node identification
    path: string;           // e.g., "root", "root->call", "root->call->raise"
    
    // Game state
    turn: 'OOP' | 'IP';     // Whose turn to act
    street: 'flop' | 'turn' | 'river';
    state: 'action' | 'fold' | 'showdown' | 'allin';
    
    // Pot and stacks
    pot: number;
    stacks: { OOP: number; IP: number };
    contributions: { OOP: number; IP: number };
    
    // Children nodes (full nested tree structure)
    children: { [action: string]: TreeNodeData };
    
    // Strategies for both players at this node
    oop_strategy: HandStrategy[];
    ip_strategy: HandStrategy[];
    
    // Whether this is a terminal node
    isTerminal: boolean;
}
