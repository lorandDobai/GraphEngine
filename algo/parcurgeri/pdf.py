
def pdf(matrix):

    graph_size = len(matrix)

    N = list(range(graph_size+1))[1:]
    W = set()
    U = list(N)
    
    s = U.pop(0)
    V = [s]

    k = 1
    p = [0]*graph_size
    t = 1
    t1 = [float("inf")]*graph_size
    t2 = [float("inf")]*graph_size

    t1[s-1]= 1

    while V:
        x = V.pop(-1)
        for y in list(U):
            if matrix[x-1][y-1]:
                U.remove(y)
                V.append(y)
                p[y-1]=x
                t=t+1
                t1[y-1]=t
        W.add(x)
        t=t+1
        t2[x-1] = t
    print(W,U,V,p,t1,t2)
    

if __name__ == '__main__':
    with open("in.txt") as fin:
        m = [list(map(int,line.split())) for line in fin.read().splitlines()]
    pdf(m)
