def ciclue(matrix,s=0):
    n = len(matrix)
    W = [s]
    x = s
    A = [(i,j) for i in range(n) for j in range(n) if matrix[i][j]]
    A_prim = set()
    Ap_barat = set(A)
    V = dict()
    for i,line in enumerate(matrix):
        V[i] = set()
        for j,element in enumerate(line):
            if element:
                V[i].add(j)
            
   
    while V[s]:
       
        y= None
        if len(V[s]) > 1:
            nc = cc(matrix)
            for q in V[x]:
                tmp_matrix = [ [e for e in line] for line in matrix]
                tmp_matrix[x][q] = tmp_matrix[q][x] = 0
                if cc(tmp_matrix) == nc:
                    y = q
                    break
        else:
            y = list(V[x])[0]
        A_prim.add((x,y))
        Ap_barat.remove((x,y))
        V[x].remove(y)
        V[y].remove(x)
        x = y
        W.append(x)
    return {"W":W}        
                    
            
            
def cc(matrix):

    graph_size = len(matrix)

    N = list(range(graph_size+1))[1:]
    W = set()
    U = list(N)
    
    s = U.pop(0)
    V = [s]
    N_prim = [s]
    k = 1
 
    while len(W) != graph_size:
        while V:
            x = V.pop(-1)
            for y in list(U):
                if matrix[x-1][y-1]:
                    U.remove(y)
                    V.append(y)
                    N_prim.append(y)
                  
            W.add(x)
        if U:
            s = U.pop()
            V= [s]
            N_prim = [s]
            k+=1
        
    return k
if __name__ == '__main__':
    with open("in.txt") as fin:
        m = [list(map(int,line.split())) for line in fin.read().splitlines()]
    
    print(ciclue(m))
