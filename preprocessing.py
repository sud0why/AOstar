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
    'n6': [['n7', 'n8'], ['n0']],
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


G = DG.copy()

is_True = {}

for goalNode in goalNodes:
    G.nodes[goalNode]['solved'] = True

# 如果所有子节点都访问过了，
def dfs(node):
    for coupling in G.nodes[node]['couplings']:
        bool_list = []
        for each_node in coupling:
            # if each_node not in visited:
            if each_node not in is_True:
                dfs(each_node)
                bool_list.append(G.nodes[each_node]['solved'])
            else:
                bool_list.append(True)
        if reduce(lambda x, y: x and y, bool_list):
            G.nodes[node]['solved'] = True
        if G.nodes[node]['solved']:
            is_True[node] = True

dfs("n0")




# T = nx.dfs_tree(DG, source='n0')
#
# print(T.nodes)
#
# flag = True
# for goalNode in goalNodes:
#     if goalNode not in list(T.nodes):
#         # return False
#         flag = False
#         print("false")
#         break
#
#
# def check_access(T, node):
#     while True:
#         father = T.pred[node]
#         print(father)
#         time.sleep(2)


# check_access(T, 'n7')

# print(list(nx.dfs_edges(DG, source='n0')))
# print(nx.dfs_successors(DG, source='n0'))

print("all done")