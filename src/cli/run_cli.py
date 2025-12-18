from src.cli.global_info import get_info
from src.cli.traverse_func import traverse_tree
from src.cli.range_selection import select_ranges
from src.tree.tree_builder import TreeBuilder
from src.cfr.winrates import create_win_cache
from src.cfr.cfr import CFRSolver



def run_cli():
    print("Poker Solver CLI")
    ranges = select_ranges()
    info = get_info()
    inters = input("Enter number of CFR iterations: ")

    tree_builder = TreeBuilder(
        ranges,
        info['stacks'],
        info['contributions'],
        info['pot'],
        info['flop']
    )

    print("Generating game tree...")
    tree_builder.generate_tree()
    root = tree_builder.root
    print("Game tree generated.")

    print("Generating win rate cache...")
    win_cache = create_win_cache(ranges['IP'], ranges['OOP'], root)
    print("Win rate cache generated.")

    print(f"Running CFR with {inters} iterations...")
    cfr_solver = CFRSolver(root, win_cache)
    for _ in range(int(inters)):
            cfr_solver.calc_stratagy(root, 'IP')
            cfr_solver.calc_stratagy(root, 'OOP')
            cfr_solver.propagate_reach(root)
            cfr_solver.calc_IP_values(root)
            cfr_solver.calc_OOP_values(root)
        
    traverse_tree(root)


if __name__ == "__main__":
    run_cli()