
def arbore_minim_generic(matrix,s=0):
   
    graph_size = len(matrix)
    N = [set([i]) for i in range(graph_size)]
    A = [set() for i in range(graph_size)]
    print(N,A)
    for k in range(graph_size-1):
        
        ni = None
        ai = None
        for i,s in enumerate(N):
            if s:
                break
        
        minim = float("inf")
        y_min = None
        y_prim = None
        for x in s:
            for j in range(graph_size):
                if j not in s and 0< matrix[x][j] < minim:
                    minim = matrix[x][j]
                    y_min = x
                    y_prim = j
        for j,Nj in enumerate(N):
            if y_prim in Nj:
                N[i] =  N[i] | Nj
                N[j]= set()
                A[i] = A[i] | A[j] | set([tuple([y_min,y_prim])])
                A[j] = set()
        print(N,A)
        if k==graph_size-2:
            print(A[i])
            ret = [(pair[0]+1,pair[1]+1) for pair in A[i]]
            return({"T":ret})
            
        
    
if __name__ == '__main__':
    with open("in.txt") as fin:
        m = [list(map(int,line.split())) for line in fin.read().splitlines()]
    arbore_minim_generic(m)
