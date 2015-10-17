def kruskal(matrix,s=0):
    
    graph_size = len(matrix)
    T = set()
    V = [set([i]) for i in range(graph_size)]
    edges = set((min([i,j]),max([i,j])) for j in range(graph_size) for i in range(graph_size) if matrix[i][j]!=0)
    edges = sorted(edges, key = lambda p: matrix[p[0]][p[1]])
    
    for edge in edges:
        u,v  = edge
        for s in V:
            if u in s:
                uSet = s
            if v in s:
                vSet = s
        if uSet != vSet:
            T.add((u+1,v+1))
            V.remove(uSet)
            V.remove(vSet)
            V.append(uSet | vSet)
          
        
    return({"T":T})

if __name__ == '__main__':
    with open("in.txt") as fin:
        m = [list(map(int,line.split())) for line in fin.read().splitlines()]
    kruskal(m)
