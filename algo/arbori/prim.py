
def arbore_minim_prim(matrix,s=0):
   graph_size = len(matrix)
   v = [ (float("inf")) for i in range(graph_size)]
   N = set(range(graph_size))
   v[0] = 0
   A_prim = set()
   N1 = set()
   N1_prim = set(N)
   e = [()for i in range(graph_size)]
   
   while len(N1) != graph_size:
      minim = float("inf")
      y = None
      for x in N1_prim:
         if v[x] < minim:
            y = x
            minim = v[x]
      
      N1.add(y)
    
      N1_prim.remove(y)
     
      if y !=  0:
         A_prim.add(e[y])
      for yPrim,val in enumerate(matrix[y]):
         if yPrim in N1_prim and val and v[yPrim] > val :
            v[yPrim] = val
            e[yPrim] = (y,yPrim)
      #print(v)
   print(A_prim)
   ret = [(pair[0]+1,pair[1]+1) for pair in A_prim]
   return {"T":ret}
             
        
    
if __name__ == '__main__':
    with open("in.txt") as fin:
        m = [list(map(int,line.split())) for line in fin.read().splitlines()]
    arbore_minim_prim(m)
