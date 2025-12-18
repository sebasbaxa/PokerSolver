from src.tree.node import Node

#TODO: improve cli overall usability
def traverse_tree(node: Node) -> None:
    curr = node
    print(curr)
    action = input("select child >> ")
    while action not in curr.children and action != "exit":
        print("No such child node.")
        action = input("select child >> ")

    if action == "exit":
        return

    curr = curr.children[action]
    traverse_tree(curr)
