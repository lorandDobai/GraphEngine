
def ptg(matrix,s=0):

    graph_size = len(matrix)

    N = set(list(range(graph_size+1))[1:])
    W = set()
    U = set(N)
    s = U.pop()
    V = set([s])

    k = 1
    p = [0]*graph_size
    o = [float("inf")]*graph_size
    o[s-1] = 1
    while len(W)!= graph_size:
        while V:
            x = V.pop()
            for y in list(U):
                if matrix[x-1][y-1]:
                    U.remove(y)
                    V.add(y)
                    p[y-1]=x
                    k+=1
                    o[y-1]=k
            W.add(x)
       
        if U:
            s = U.pop()
            V=set([s])
            k+=1
            o[s-1]=k
   
    return {"p":p,"o":o}
        
            
            
        
    
if __name__ == '__main__':
    with open("in.txt") as fin:
        m = [list(map(int,line.split())) for line in fin.read().splitlines()]
    ptg(m)
