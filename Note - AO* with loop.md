一种新的泛化的启发式搜索LAO*，可以找到带有循环的解，可用于解决马尔科夫决策问题，优于动态规划，可以在不评估整个状态空间的情况下找到最佳解决方案。

对于状态空间较大的问题，启发式搜索优于动态编程，因为它可以在不评估整个状态空间的情况下为起始状态找到最佳解决方案。

LAO*解决形式化为MDP的规划问题。

第2节回顾了MDP的动态规划算法和状态空间搜索问题的启发式搜索算法，并讨论了它们之间的关系。 
第3节介绍了LAO*算法。
第4节介绍了该算法的一些扩展，这些示例说明了启发式搜索技术与更有效地解决MDP问题的相关性。
第5节描述了LAO*在两个测试问题上的性能，并讨论了一些影响其效率的搜索控制问题。

2.2 与或图的启发式搜索

S表示可能的状态集
s∈S表示与图的根节点相对应的开始状态
T⊂S表示在图的叶节点处出现的一组目标（或终点）状态
A表示有限的一组动作
A（i）表示适用于状态i的一组动作

k连结符在不确定性规划中解释为具有不确定结果的行动，该行动将一个状态转换为k个可能的后继状态，每个状态都具有一个概率。
Pij(a)表示状态i中采取行动a导致状态转变为j的概率。
Ci(a)表示状态i采取行动a对应的k连结符的成本。
假设每个目标状态成本为0，通过下面的方程组可以找到最低成本解图：


随机最短路径问题具有无限或不确定的范围，传统的与或图搜索框架不能直接应用于解决该问题。

树形式与或图求解：
N.J. Nilsson, Search problem-solving and game-playing trees for minimal cost solutions, in: A. Morrell (Ed.), Information Processing 68, Vol. 2, North-Holland, Amsterdam, 1969, pp. 1556–1562.
N.J. Nilsson, Problem Solving Methods in Artiﬁcial Intelligence, McGraw-Hill, New York, 1971.

非循环与或图求解：
A. Martelli, U. Montanari, Additive AND/OR graphs, in: Proc. IJCAI-73, Stanford, CA, 1973, pp. 1–11.
A. Martelli, U. Montanari, Optimizing decision trees through heuristically guided search, Comm. ACM 21 (12) (1978) 1025–1039.

通用名：
N.J. Nilsson, Principles of Artiﬁcial Intelligence, Tioga Publishing, Palo Alto, CA, 1980.



是goal目标点的tip末端结点或leaf叶结点是terminal终结点，否则叫nonterminal非终结点
一个nonterminal非终结tip末端结点可以通过添加显式图中其连接的k连结符和显式图中尚未存在的任何后继状态来扩展。

无论选择哪个非终结末端结点来扩展，都可以正常工作，但是使用好的选择函数可以提高AO*的效率。选择具有最小估计成本或具有最大到达可能性的结点。

搜索带循环的与或图的可能性：P. Jiménez, C. Torras, An efﬁcient algorithm for searching implicit AND/OR graphs with cycles, Artiﬁcial Intelligence 124 (2000) 1–30.

循环表示不确定的行为，允许多次访问同一状态。

AO*的成本修订步骤是动态规划算法，泛化该步骤。
除了backwards induction向后归纳法外，还可以通过使用针对indeﬁnite-horizon MDPs的动态规划算法，如policy iteration策略迭代和value iteration价值迭代，来更新成本

现在，部分解图的正向搜索将在目标节点，非终结尖端节点或返回当前部分解图的已扩展节点的循环处终止。
允许包含循环，那么AO*动态规划步骤的的反向归纳算法就不能再用了。但是可以通过对infinite-horizon MDPs使用策略迭代或者价值迭代来执行动态规划。

LAO*
1. The explicit graph G’ initially consists of the start node s.
1. 初始化显式图G'由起点s组成
2. Forward search: Expand the best partial solution graph as follow:.
2. 正向搜索：扩展最佳局部解图
(a) Identify the best partial solution graph and its nonterminal tip nodes by searching forward from the start state and following the marked action for each state.
(a) 通过从开始状态正向搜索和跟随每个状态的mark的动作，确定最佳局部解图和非终结叶结点。
(b) If the best partial solution graph has no nonterminal tip nodes, goto 4.
(b) 如果最佳偏解图没有非终结叶节点，转到4。
(c) Else expand some nonterminal tip node n and add any new successor nodes to G’. For each new tip node i added to G’ by expanding n, if i is a goal node then f(i)=0;else f(i ) = h(i).
(c) 否则，扩展一些非终结叶节点n，并将任何新的后继节点添加到G’中。对于通过扩展n添加到G’中的每个新的尖端节点i，如果i是目标节点，f(i)=0;否则f(i)=h(i)。
3. Dynamic programming: Update state costs as follows:
3. 动态规划：更新结点成本
(a) Identify the ancestors in the explicit graph of expanded node n and create a set Z that contains the expanded node and all its ancestors.
(a) 识别显式图G'中被扩展结点n的祖先，并创建一个集合Z包含扩展结点n以及其所有祖先。
(b) Perform policy iteration on the nodes in set Z until convergence or else perform value iteration on the nodes in set Z for one or more iterations. Mark the best action for each state.
(When determining the best action resolve ties arbitrarily, but give preference to the currently marked action.)
(b) 在集合Z中的节点上执行策略迭代，直到收敛为止；或者在集合Z中的节点上执行一次或多次值迭代。标记每个结点的最佳操作。
(在确定最佳动作时，可以任意解决联系，但优先选择当前标记的动作。)
(c) Goto 2.
4. Return the solution graph.

策略迭代：
优势：基于tip节点的启发式估计为显式图G'的每个节点计算出精确的成本。
策略迭代是在节点集合Z上执行的，该节点集合包括显式图中的扩展节点n及其所有祖先。
这些节点中的某些节点可能具有后继节点，后继节点不在此节点集中，但仍属于显式图的一部分。换句话说，策略迭代不一定（或通常）执行整个显式图。这些后继节点的成本可以在动态规划中视为常量，因为它们不受扩展节点或其祖先成本的任何变化的影响，AO*的动态规划也充分说明了这一点。
在这组节点上执行策略迭代可能会更改某些结点的最佳操作，并因此更改最佳的局部解决方案图；AO*的反向归纳算法可以达到相同的效果。因为可能需要策略迭代进行多次迭代才能收敛，所以必须强调必须在该集合中的所有节点上执行策略迭代直到收敛。必须确保显式图中的所有节点都具有准确的可接受成本，包括那些不再是最佳局部解决方案图的一部分的成本。

价值迭代：略

正向搜索：
如何选择扩展对象提高效率？起始状态达到概率最高的结点或成本最小的结点。
也可以一次扩展几个节点，这具有扩展某些不必要节点的风险，但是当动态规划步骤与正向搜索步骤相比相对昂贵时，可以提高算法的性能。

内存受限版本的AO*：Chakrabarti, P.P; Ghosh, S.; Acharya, A.; & DeSarkar, S.C. 1989. Heuristic Search in Restricted Memory. Artificial Intelligence 47:197-221.