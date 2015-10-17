def bellman_ford(matrix,s = 0):
    graph_size = len(matrix)
    N = set(range(graph_size))
  
    d = [float("inf")]* graph_size
    p = [0] * graph_size
    d[s] = 0
    d_prim = [None] * graph_size
    V_minus = {i:[j for j in range(graph_size) if matrix[j][i]] for i in range(graph_size)}
    
    while d!=d_prim:
        for i,e in enumerate(d):
            d_prim[i] = e
        for y in N:
            if V_minus[y]:
                x = min(V_minus[y],key = lambda q:d_prim[q] + matrix[q][y])
                if d_prim[x] + matrix[x][y] < d_prim[y]:
                    d[y] = d_prim[x] + matrix[x][y]
                    p[y] = x
        print(d,p)
    return ({"d":d,"p":p}) 
if __name__ == '__main__':
    with open("in.txt") as fin:
        m = [list(map(int,line.split())) for line in fin.read().splitlines()]
    bellman_ford(m)
