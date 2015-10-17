def djikstra(matrix,s=0):
    graph_size = len(matrix)
    W = N = set(range(graph_size))
    d = [float("inf")]*graph_size
    d[s] = 0
    p = [None]*graph_size
    while W:
        x = min(W,key = lambda y: d[y])
        W.remove(x)
        for y in ((j) for j,el in enumerate(matrix[x]) if el>0):
            if d[x] + matrix[x][y] < d[y]:
                d[y] = d[x] + matrix[x][y]
                p[y] = x
        print(d,p)
    ret = []
    for i in p:
        if i == None:
            ret.append(0)
        else:
            ret.append(i+1)
    return {"d":d,"p":p}
                
    
if __name__ == '__main__':
    with open("in.txt") as fin:
        m = [list(map(int,line.split())) for line in fin.read().splitlines()]
    djikstra(m)
