/**
 * Poker hand grid utilities
 * Converts grid positions to hand strings and vice versa
 */

export const RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'] as const;

export type Rank = typeof RANKS[number];

/**
 * Convert grid position to hand string
 * @param row - Row index (0-12, where 0 = Ace)
 * @param col - Column index (0-12, where 0 = Ace)
 * @returns Hand string like "AKs", "KQo", "AA"
 */
export function gridToHand(row: number, col: number): string {
  const rank1 = RANKS[row];
  const rank2 = RANKS[col];
  
  if (row === col) {
    // Pocket pair (diagonal)
    return `${rank1}${rank2}`;
  } else if (row < col) {
    // Suited (upper triangle)
    return `${rank1}${rank2}s`;
  } else {
    // Offsuit (lower triangle)
    return `${rank2}${rank1}o`;
  }
}

/**
 * Get the number of combinations for a hand
 * @param hand - Hand string like "AKs", "KQo", "AA"
 * @returns Number of combinations (6 for pairs, 4 for suited, 12 for offsuit)
 */
export function getHandCombos(hand: string): number {
  if (hand.length === 2) {
    // Pocket pair
    return 6;
  } else if (hand.endsWith('s')) {
    // Suited
    return 4;
  } else {
    // Offsuit
    return 12;
  }
}

/**
 * Get hand category for styling
 */
export function getHandCategory(row: number, col: number): 'pair' | 'suited' | 'offsuit' {
  if (row === col) return 'pair';
  if (row < col) return 'suited';
  return 'offsuit';
}

/**
 * Convert a specific hand (e.g., "AsAh") to its category (e.g., "AA")
 * @param hand - Specific hand string like "AsAh", "KsQs", "AhKd"
 * @returns Hand category like "AA", "KQs", "AKo"
 */
export function getHandCategoryFromSpecific(hand: string): string {
  if (hand.length < 4) return hand; // Already a category
  
  const rank1 = hand[0];
  const suit1 = hand[1];
  const rank2 = hand[2];
  const suit2 = hand[3];

  if (rank1 === rank2) {
    return `${rank1}${rank2}`; // Pocket pair
  }

  const suited = suit1 === suit2;
  const rankOrder = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'];
  const [highRank, lowRank] = [rank1, rank2].sort((a, b) => 
    rankOrder.indexOf(b) - rankOrder.indexOf(a)
  );

  return `${highRank}${lowRank}${suited ? 's' : 'o'}`;
}

/**
 * Calculate total combinations from a list of hands
 */
export function getTotalCombos(hands: string[]): number {
  return hands.reduce((total, hand) => total + getHandCombos(hand), 0);
}

/**
 * Get percentage of all possible hands
 */
export function getRangePercentage(combos: number): number {
  return Math.round((combos / 1326) * 1000) / 10; // 1326 = total poker hand combos
}
