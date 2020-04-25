import networkx as nx
from functools import reduce
import numpy as np

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

# 算法开始
# 1. 建立图g，判断startNode是否是终结点
g = DG.subgraph(startNode).copy()

if startNode in goalNodes:
    g.nodes[startNode]['solved'] = True


# 判断结点是否solved
def solved(mg, node):
    return nx.get_node_attributes(mg, 'solved')[node]


# 判断边是否marked
def marked(mg, edge1, edge2):
    return nx.get_edge_attributes(mg, 'marked')[edge1, edge2]


# 找到图中的任一非终结的叶结点，和别人的有出入
def findleaf(g):
    for i in g.nodes:
        # todo: n的选择，此处可能有坑
        if DG.nodes[i]["couplings"] and not g.__getitem__(i):
            return i
    return None


# 获取结点耗散值cost
def cost(mg, node):
    return nx.get_node_attributes(mg, 'cost')[node]


# 添加子节点集进g
def addToG(n, nodeList):
    g.nodes[n]['couplings'] = DG.nodes[n]['couplings']
    for i in nodeList:
        if not g.has_edge(n, i):
            g.add_edge(n, i, marked=False)
            g.nodes[i]['cost'] = cost(DG, i)
            g.nodes[i]['solved'] = False
            if i in goalNodes:
                g.nodes[i]['solved'] = True


# 2.3. 外层循环，直到startNode被标记为solved
while not solved(g, startNode):
    # 4. 根据连接符marked找到待扩展的局部解图gprime
    # gprime局部解图，g为显式图
    gprime = g.subgraph(startNode).copy()
    for i in g.edges:
        if marked(g, i[0], i[1]):
            gprime.add_edge(i[0], i[1])

    # 5. 令n是局部解图gprime中的任一非终结结点
    n = findleaf(gprime)

    # 6. add(expand(n))
    nodeList = list(DG.neighbors(n))
    addToG(n, nodeList)

    # 策略迭代 算法开始

    # 被扩展结点n极其祖先集合z
    z = [n] + list(gprime.predecessors(n))

    # 迭代计数
    iteration = 0

    # 使用当前mark边和默认第一条边初始化策略
    policy = {}
    for s in z:
        find_policy_flag = False
        for index, coupling in enumerate(DG.nodes[s]["couplings"]):
            if find_policy_flag:
                break
            for node in coupling:
                if g.edges[s, node]['marked']:
                    policy[s] = index
                    find_policy_flag = True
                    break
        if not find_policy_flag:
            policy[s] = 0

    # 使用当前启发函数值初始化价值
    while True:
        iteration += 1

        # policy evaluation step
        # 策略评估步骤
        # while True:
        #     biggest_change = 0
        #     for 每一个状态 in z:
        #         计算该策略下，状态的价值
        #         计算价值改变量biggest_change
        #     if biggest_change < 1e-3:
        #         break
        while True:
            biggest_change = 0
            # todo policy(s) exist if it's not a terminal state
            for s in z:
                old_cost = costs[s]
                costs[s] = len(DG.nodes[s]["couplings"][policy[s]]) + sum(costs[x] for x in DG.nodes[s]["couplings"][policy[s]])
                biggest_change = max(biggest_change, np.abs(old_cost - costs[s]))
            if biggest_change < 1e-3:
                break

        # 策略提升步骤
        # is_policy_converged = True
        # for 每一个状态 in z:
        #     for a（每一个动作） in actions:
        #         计算保留具有最小价值的动作
        #     更新该状态的策略
        #     if 策略改变:
        #         # 继续循环
        #         is_policy_converged = False
        #
        # # 如果策略不改变，跳出迭代
        # if is_policy_converged:
        #     break
        is_policy_converged = True
        for s in z:
            old_policy = policy[s]
            best_cost = float('inf')
            q = {}
            for index, coupling in enumerate(DG.nodes[s]["couplings"]):
                q[index] = len(coupling) + sum(costs[x] for x in coupling)
            policy[s] = min(q, key=q.get)
            if old_policy != policy[s]:
                is_policy_converged = False

        if is_policy_converged:
            break

    # 标记最优选择的边
    # for s in z:

    print("ok")

# 算法结果获取
# 别人的思想按边获取，但是会获取到多标记的一些边
# 直接按solved点获取，可以得到答案
markedge = nx.get_edge_attributes(g, 'marked')
print(markedge)
solvenode = nx.get_node_attributes(g, 'solved')
print(solvenode)

# 结果导出
result = {}
for edge in markedge:
    if markedge[edge] and solvenode[edge[0]]:
        if edge[0] not in result:
            result[edge[0]] = [edge[1]]
        else:
            result[edge[0]].append(edge[1])
print(result)

print("all done")