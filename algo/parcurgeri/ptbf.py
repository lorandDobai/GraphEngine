
def ptbf(matrix,s=0):

    graph_size = len(matrix)

    N = list(range(graph_size+1))[1:]
    W = set()
    U = list(N)
    
    s = U.pop(0)
    V = [s]

    k = 1
    p = [0]*graph_size
    l = [float("inf")]*graph_size
    l[s-1] = 0
    while len(W)!= graph_size:
        while V:
            x = V.pop()
            for y in U:
                if matrix[x-1][y-1]:
                    U.remove(y)
                    V.append(y)
                    p[y-1]=x
                    l[y-1]=l[x-1]+1
            W.add(x)
        print(W,V,U,p,l)
        if U:
            s = U.pop()
            V=[s]
            l[s-1]=0
    return {"p":p,"l":l}

if __name__ == '__main__':
    with open("in.txt") as fin:
        m = [list(map(int,line.split())) for line in fin.read().splitlines()]
    pbf(m)
