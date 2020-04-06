import networkx as nx
from functools import reduce
import time

# 结点node需要标记solved,cost和连接符coupling
# 问题1：and关系标记在哪？
# 标记在点，容易索引，就是连接符
# 边edge需要标记marked

# 输入数据

costs = {'n0': 3, 'n1': 2, 'n2': 4, 'n3': 4, 'n4': 1, 'n5': 1, 'n6': 2, 'n7': 0, 'n8': 0}
goalNodes = ['n7', 'n8']
startNode = 'n0'
allcouplings = {
    'n0': [['n1'], ['n4', 'n5']],
    'n1': [['n2'], ['n3']],
    'n2': [['n3'], ['n4', 'n5']],
    'n3': [['n5', 'n6']],
    'n4': [['n5'], ['n8']],
    'n5': [['n6'], ['n7', 'n8']],
    'n6': [['n7', 'n8']],
    'n7': [],
    'n8': []
}

# 实例化一个有向图
DG = nx.DiGraph()

# 根据连接符构建图
for node in allcouplings:
    couplings = allcouplings[node]
    # 初始化结点
    DG.add_node(node, solved=False, cost=costs[node], couplings=couplings)
    for coupling in couplings:
        for pointednode in coupling:
            # 初始化边
            DG.add_edge(node, pointednode, marked=False)

# 算法目标，判断可达性，随便找到一条路可达就ok
# 即，dfs(root)运行结束后，root可解，说明可达，否则不可达
# dfs():
#     if 可解
#         标记访问过
#     else 不可解
#         if 未访问过且为上锁
#             上锁，访问（一个连结符为真就跳出），去锁
#         标记访问过

# 可达性算法开始
G = DG.copy()

# dfs结束，即访问过的点
visited = {}
# 访问中，上锁的点
visiting = {}

for goalNode in goalNodes:
    G.nodes[goalNode]['solved'] = True


# 如果所有子节点都访问过了，
def dfs(node):
    # 如果可解，直接标记访问过，结点不再访问
    if G.nodes[node]['solved']:
        visited[node] = G.nodes[node]['solved']
    else:
        # 如果不可解，且结点没有访问过，结点没有上访问锁
        if node not in visited and node not in visiting:
            # 正在访问结点上锁
            visiting[node] = True
            # 遍历每个连接符
            for coupling in G.nodes[node]['couplings']:
                bool_list = []
                # 每个连接符的每个结点，如果
                for each_node in coupling:
                    # if each_node not in visited:
                    if each_node not in visited and each_node not in visiting:
                        dfs(each_node)
                    bool_list.append(G.nodes[each_node]['solved'])
                # 如果有一个连结符为可解，那么该结点直接标记可解，跳出循环
                if reduce(lambda x, y: x and y, bool_list):
                    G.nodes[node]['solved'] = True
                    break
            # 删除访问锁
            del visiting[node]
        # 如果结点不可解，结点被锁，或者结点访问过？
        visited[node] = G.nodes[node]['solved']


root = 'n0'
dfs(root)
print(G.nodes[root]['solved'])

print("all done")