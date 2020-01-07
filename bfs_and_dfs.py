"""
In this script I implement the Breadth First Seach Algorithm or BFS and
Depth First Seach Algorithm or DFS, to determine a route or "traversal"
between nodes in a graph (if such traversal even exists)
In order to do so, i first define a graph on which i implement this seach.
This graph is a grid of size-by-size, where each square is a node, and is 
connected to its 8 surrounding squares (unless its in the edges of the grid than 
we have some special cases)

We stat with BFS: this search aswell as the DFS alg. can be implemened recursivly, however 
it is not common to do so. The way it is ofen implemented is by using a Queue 
(q) in which we stack the nodes we want to visit next. If for each node we stack 
its adjacent nodes (if already in the list) on top of the previous stack, we will
implement BFS by definition. In DFS we mearly satck the nodes at the beginning of the list
rather than its end. This explenation can be seen in [1] and [2,3]

MIT 6.034 Artificial Intelligence, Fall 2010 lecture 4 min 22:
[1] https://www.youtube.com/watch?v=j1H3jAAGlEA&list=PLUl4u3cNGP63gFHB6xb-kVBiQHYe_4hSi&index=5&t=1974s

Joe James's YouTube and GitHub:
[2] https://www.youtube.com/watch?v=-uR7BSfNJko
[3] https://github.com/joeyajames/Python/blob/master/bfs.py
"""

# we will use the graph class which uses te vertex class, thus we import both
from Adj_List_graph import vertex, graph
import numpy as np


# We define a class that manifests a grid as a graph. to initialize an object
# of this class we only need to input its size (e.e. 10 will result in a 10 by 10
# grid with 100 cells as nodes)
class grid_graph:
    def __init__(self, size):
        # to see the graph an its nodes in a grid, we do the following:
        self.grid = np.array([range(1,size**2+1)])
        self.grid = self.grid.reshape((size,size))
        self.size=size
        print(self.grid)
        self.graph=graph()
        
        # to define the grid as an object of class "graph", we need to initialize
        # each of the size^2 nodes as a "vertex" object and add it to the graph.
        # Then afer we determine each nodes' edges and add it to the list of egdes.
        # I brute forced it, so the list will contain pairs like (node1, node2)
        # and (node2, node1) whis is the same in an undirected graph as we implement
        # (the add_edge method in class "graph" adds a connection/edge between 
        # both nodes regardless of their order in the tuple).
        # In order to see the logic of how to determine which nodes are connected,
        # simply write the numbers 1 to size^2 in on a grid, starting from the 
        # top right and filling in each row.
        # If i dont want to allow connections between diagonal nodes just delete the
        # tuples that are of the form (i,i+-size+-1)
        edges=list()
        for i in range(1, size**2+1):
            self.graph.add_node(vertex(i))
            if i==1:
                edges+=[(1,2),(1,size+1),(1,size+2)]
            elif i==size:
                edges+=[(size,size-1),(size,2*size-1),(size,2*size)]
            elif i==(size-1)*size+1:
                edges+=[(i,i+1),(i,i-size+1),(i,i-size)]
            elif i==size**2:
                edges+=[(i,i-1),(i,i-size-1),(i,i-size)]
            elif i%size==1:
                edges+=[(i,i+1),(i,i-size+1),(i,i-size),(i,i+size+1),(i,i+size)]
            elif i%size==0:
                edges+=[(i,i-1),(i,i-size-1),(i,i-size),(i,i+size-1),(i,i+size)]
            elif i in list(range(2,size)):
                edges+=[(i,i+1),(i,i-1),(i,i+size),(i,i+size+1),(i,i+size-1)]
            elif i in list(range(size+1,size**2)):
                edges+=[(i,i+1),(i,i-1),(i,i-size),(i,i-size-1),(i,i-size+1)]                      
        self.graph.add_edge(edges) 
        
        
            
def bfs(graph,start=22,goal=88):
    # to implement bfs we use a Queue "q" as a list which contains nodes's 
    # names, which intend to visit untill we find the goal node.
    q=[start];
    # we dont want to insert to q, a node which it already has (this will just be 
    # redundant as we may even go backwards and end looping endlessly). So, we keep
    # track of the nodes we have already inserted to the Queue, we have a boolian 
    # array that is True if the node has been already inserted (and False otherwise)
    # we implement this again using a dictionary (which is good incase the nodes 
    # names are not necessarily numbers), but this can also be implemented using a simple 
    # 1-by-size^2 array like: [False]*size**2
    
    # inorder to retrive the path once we find the goal node, we need to keep track
    # of which node put another node in the queue. this is manifested as a linked list
    # called "route" which we implements using a dictionary. if we go back from 
    # the goal node, and keep track of who queued who, we will get the path.
    # this is done a the end of this function.
    visited={}
    route={};
    for key in graph.AdjList:
        visited[key]=False
        route[key]=[]
    visited[start]=True
    
    # now we can acrtually start the search. "found" is a boolian that indicates
    # succes in dinding goal and "i" is just an itteration counter.
    found=False
    i=0
    # Run as long as the Queue is not empty (so we have visited each connected node
    # in the graph). The q initially contains only the start node.
    while q and not found:
        # Get the list of all adjacent nodes of the first node in the q. enq
        # stands for EnQueue 
        enq=graph.AdjList[q[0]]
        # now, for each item on this list of adjacent nodes, check if its already
        # EnQueued, if not add it to the q and mark it as EnQueued in the visited dictionary.
        for j in enq:
            if visited[j]==False:
                q+=[j]
                visited[j]=True
                # mark the j'th node as enqued by the q[0] node.
                route[j]=q[0]
                # if we managed to reach the goal node, raise the success flag.
                if j==goal:
        
                    found=True
        # once all adjacent members of q[0] were enqued, we move to the next
        # member of the q. This can be done by :
        #    while not found and i<=graph.size:
        #        enq=graph.AdjList[q[i]]
        #        for j in enq:
        #            if visited[j]==False:
        #                q+=[j]
        #                visited[j]=True
        #                route[j]=q[i]
        #                if j==goal:
        #                    found=True
        #        i+=1
        # or more ellegantly just by deleting the first ellement of q.
        q.pop(0)
        i+=1
    
    # we determine the traversal using the linked-list "route")    
    traversal=[]
    connection=False
    if found:
        connection=True
        done=False
        i=goal
        traversal=[goal]
        while not done and i!=start:
            traversal+=[route[i]]
            i=route[i]
    traversal=traversal[::-1]
    print(traversal,'itterations=',i)
    return connection,traversal

"""
Now we move to DFS:
This is very simmylar to BFS however here, we insert the djacent nodes in each itteration,
at the beginning of the queue. this is explained reasonably good by [1]

MIT 6.034 Artificial Intelligence, Fall 2010 lecture 4 min 22:
[1] https://www.youtube.com/watch?v=j1H3jAAGlEA&list=PLUl4u3cNGP63gFHB6xb-kVBiQHYe_4hSi&index=5&t=1974s

"""
def dfs(graph,start=22,goal=88):
    q=[start];
    visited={}
    route={};
    for key in graph.AdjList:
        visited[key]=False
        route[key]=[]
    visited[start]=True
    found=False
    i=0
############ The only part that differs from BFS ############   
    # now, instead of enqueing at the end of the q, we enqueue in the beginning.
    while not found: #and i<=graph.size**2:
        enq=graph.AdjList[q[i]]
        k=0
        for j in enq:
            if j not in q[0:i+1+k]:
                q=q[0:i+1+k]+[j]+q[i+1+k:-1]
                route[j]=q[i]
            k+=1
            if j==goal:
                found=True
        i+=1
##############################################################        
    traversal=[]
    connection=False
    if found:
        connection=True
        done=False
        i=goal
        traversal=[goal]
        while not done and i!=start:
            traversal+=[route[i]]
            i=route[i]
    traversal=traversal[::-1]
    print(traversal,'itterations=',i)
    return connection,traversal


# here i tried implementing dfs more ellegantly, like in bfs, however
# the results are exactly he same as BFS, so something is clearly wrong
def dfs2(graph,start=22,goal=88):
    q=[start];
    visited={}
    route={};
    for key in graph.AdjList:
        visited[key]=False
        route[key]=[]
#    visited[start]=True
    found=False
    i=0
    while q and not found: #and i<=graph.size**2:
        enq=graph.AdjList[q[0]]
        if visited[q[0]]:
            continue
        else:
            visited[q[0]]=True
        curr_node=q[0]
        q.pop(0)
        for j in enq:
            if not visited[j]:
#                visited[j]=True
                q=[j]+q # q.insert(0,j) is the same
                route[j]=curr_node
            if j==goal:
                found=True
        i+=1
        
    traversal=[]
    connection=False
    if found:
        connection=True
        done=False
        i=goal
        traversal=[goal]
        while not done and i!=start:
            traversal+=[route[i]]
            i=route[i]
    traversal=traversal[::-1]
    print(traversal,'itterations=',i)
    return connection,traversal

def main():
    grid=grid_graph(10)
    print('DFS route and itterations')
    dfs(grid.graph,22,88)
    print('DFS2 route and itterations')
    dfs2(grid.graph,22,88)
    print('BFS route and itterations')
    bfs(grid.graph,22,88)

if __name__ == "__main__":
    # execute only if run as a script
    main()
             
