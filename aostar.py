import networkx as nx
from functools import reduce

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
    gprime = g.subgraph(startNode).copy()
    for i in g.edges:
        if marked(g, i[0], i[1]):
            gprime.add_edge(i[0], i[1])

    # 5. 令n是局部解图gprime中的任一非终结结点
    n = findleaf(gprime)

    # 6. add(expand(n))
    nodeList = list(DG.neighbors(n))
    addToG(n, nodeList)

    # 7. 含n的单一结点集合
    s = [n]

    # 8.9. 内层循环，直到s为空
    while s:
        # 10. remove(m, s)移除后裔不出现在s中的结点m
        # m的选择，此处可能有坑，原坑已修改，不清楚有没有新坑
        for i in s:
            flag = True
            for j in list(g.neighbors(i)):
                if j not in s:
                    flag = flag and True
                else:
                    flag = flag and False
            if flag:
                m = s.pop(s.index(i))
                break
            # if i not in list(g.neighbors(i)):
            #     m = s.pop(s.index(i))
            #     break

        # 11. 计算连接符的耗散值
        q = {}
        for index, coupling in enumerate(DG.nodes[m]["couplings"]):
             q[index] = len(coupling) + sum(costs[x] for x in coupling)
        mincoupling = min(q, key=q.get)

        # 11. marked最小耗散值的连接符
        bool_list = []
        for i in DG.nodes[m]["couplings"][mincoupling]:
            g.edges[m, i]['marked'] = True
            bool_list.append(g.nodes[i]['solved'])
            # 删除其他marked
            # 此处可能有坑，会多标记一条边，但是原算法是这么做的，也会有多的这个标记
            # 怎么理解：如果以前的标记情况与此不同，则抹掉以前的标记
            for j in list(g.neighbors(m)):
                if j != i and j not in DG.nodes[m]["couplings"][mincoupling]:
                    g.edges[m, j]['marked'] = False
                    # for a in list(g.neighbors(j)):
                    #     g.edges[j, a]['marked'] = False

        # 如果子节点可解，当前节点也可解
        if reduce(lambda x, y: x and y, bool_list):
            g.nodes[m]['solved'] = True

        # 12. 如果当前节点可解或当前节点耗散值更新，更新耗散值，并添加父节点到s
        if solved(g, m) or costs[m] != q[mincoupling]:
            costs[m] = q[mincoupling]
            for i in list(g.predecessors(m)):
                if i not in s:
                    s.append(i)

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