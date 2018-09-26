import matplotlib.pyplot as plt
nodes5 = [200890, 1475, 278, 16]
nodes4 = [49683, 196161, 138070, 2846]
nodes3 = [1240, 506, 156, 67]
nodes = [nodes3, nodes5, nodes4]
dfs = []
bfs = []
ids = []
astar = []
for i in range(3):
    dfs.append(nodes[i][0])
    bfs.append(nodes[i][1])
    ids.append(nodes[i][2])
    astar.append(nodes[i][3])
print(dfs)
print(bfs)
print(ids)
print(astar)
plt.bar(range(0,12,4),dfs, label = "DFS", color = 'r')
plt.bar(range(1,12,4),bfs, label = "BFS", color = 'b')
plt.bar(range(2,12,4),ids, label = "IDS", color = 'g')
plt.bar(range(3,12,4),astar, label = "A*", color = 'y')
plt.ylabel('Nodes expanded')
plt.xlabel('Difficulty of the problem')
plt.xticks(range(2,12,4), ('3', '5', '4'))
plt.title('Nodes expanded for each search method')
plt.legend()
plt.savefig('C:/Users/vneze/Desktop/scalability.png')
plt.show()
