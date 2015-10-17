def floyd_warshall(matrix):
    n = len(matrix)
  
    d = [ [0 for j in range(n)] for i in range(n)]
    p = [ [0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                d[i][j] = matrix[i][j]
            else:
                d[i][j] = float("inf")
            if i!=j and matrix[i][j]:
                p[i][j] =i
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
                    p[i][j] = p[k][j]
    return d,p

def drum_floyd_warshall(matrix,i=0,j=0):
    d,p = floyd_warshall(matrix)
    n = len(matrix)
    k = n
    if(not j):
        j = n-1
    x = j
    res = [j]
    while x != i:
        res.append(p[i][x]+1)
        x = p[i][x]
    print(res)
    return {"resultat":res}
    
    
if __name__ == '__main__':
    with open("in.txt") as fin:
        m = [list(map(int,line.split())) for line in fin.read().splitlines()]
    drum_floyd_warshall(m)
