from collections import deque
class Node:
    def __init__(self, parent, authority):
        self.id = id
        self.subnode = []
        self.parent = parent
        self.authority = authority
        self.toggle = True


class Tree:
    def __init__(self, parents, authorities):
        self.nodes = [Node(None, None)]+[Node(parent, authority) for parent, authority in zip(parents, authorities)]
        self.enroll_subnode()
        # print([(node.subnode, node.parent, node.authority) for node in self.nodes])
    def enroll_subnode(self):
        for i, node in enumerate(self.nodes):
            self.nodes[i].id = i
            if i == 0:
                continue
            self.get_node(node.parent).subnode.append(i)
    def get_node(self, idx):
        return self.nodes[idx]

    def toggle_alarm(self, node):
        self.nodes[node].toggle = bool((self.nodes[node].toggle + 1) % 2)

    def change_authority(self, node, power):
        self.nodes[node].authority = power

    def change_parent(self, node1, node2):
        parent_node1 = self.get_node(node1).parent
        parent_node2 = self.get_node(node2).parent
        self.get_node(node1).parent = parent_node2
        self.get_node(node2).parent = parent_node1
        self.get_node(parent_node1).subnode.remove(node1)
        self.get_node(parent_node2).subnode.remove(node2)
        self.get_node(parent_node1).subnode.append(node2)
        self.get_node(parent_node2).subnode.append(node1)

    def traverse_alarm(self, target_node):
        q = deque([(node, 1) for node in self.get_node(target_node).subnode])
        reachable = []
        while q:
            # print(q)
            cur, degree = q.popleft()
            cur = self.get_node(cur)
            if not cur.toggle:
                continue
            if cur.subnode:
                for node in cur.subnode:
                    q.append((node, degree+1))
            if degree <= cur.authority:
                reachable.append(cur.id)
        # print(f"Reachable from {target_node}, {reachable}")
        return len(reachable)


N, M = map(int, input().split())
first_input = list(map(int, input().split()))[1:]
tree = Tree(first_input[:N], first_input[N:])
for i in range(M - 1):
    cmd = list(map(int, input().split()))
    if cmd[0] == 200:
        tree.toggle_alarm(cmd[1])
    if cmd[0] == 300:
        tree.change_authority(cmd[1], cmd[2])
    if cmd[0] == 400:
        tree.change_parent(cmd[1], cmd[2])
    if cmd[0] == 500:
        print(tree.traverse_alarm(cmd[1]))