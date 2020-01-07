"""
Nadav's implementation of a graph with adjacancy list implementation.
Basically if the graph is dense i.e. Edges~Nodes^2 (fully connected graph with 
n nodes has n(n-1)/2 edges) it is always better to use adjacancy matrix, however
i will use a list because it is really suitable for python since i can use the dictionary
data type which is super flexible and friendly (i can store both strings and integers,
so i can name nodes as both numbers or strings like in the example).
The adjacancy list is a distionary whos "keys" are nodes, and each key has
an associated list containing all the nodes's names which are connected to the key node. 

"""
# A good practice is to define a class of a node/vertex, however
# this is totally redundant here, an done only for the sake of practice.
# I initialize a node just by assigning it a name.
class vertex:
    def __init__(self, name):
       self.name=name
# a graph is mearly collection of vertices and edges. This Graph data structure
# will be represented by the Adjacancy List self.AdjList (which is a data structure that represents a graph)
# In order to define a graph, we need a method that initializes the Adjacancy List
# (the constructore), a method to add a node to the graph (add_node), and a method 
# that connects the nodes of the graph together (we input which edges exist and
# the function add_edge will complete the AdjList accordigly). I will also add 
# methods to "delete a node" or an edge later on if necessary. 
class graph:
    def __init__(self):
        self.size=0
        self.AdjList={}
    
    def add_node(self,Ver):
        # This method gets a vertex and adds it to the distionary AdjList
        # as a key. Each key has a list containing the connected nodes's names.
        # First check if the variable recieved is of calss "vertex" i.e. a node
        # and check if we didnt already insert it to the AdjList,if both terms
        # are true, we insert it to AdjList
        if isinstance(Ver,vertex) and Ver.name not in self.AdjList:
            self.AdjList[Ver.name]=list()
            self.size+=1

    def add_edge(self, edges):
        # edges will be a list of tuples [('dog', 'cat'), ('A','B')], we itterate
        # though this list and update the AdjList accordigly, as long the egdes
        # sent, were not previously in the list.
        for edge in edges:        
            if edge[0] not in self.AdjList[edge[1]]:
                self.AdjList[edge[1]]+=[edge[0]]
            if edge[1] not in self.AdjList[edge[0]]:
                self.AdjList[edge[0]]+=[edge[1]]
                
    def print_graph(self):
        # simply prin the adjacancy list
        for key in self.AdjList:
            print(key,': ', self.AdjList[key])

def main():
    g=graph()
    g.add_node(vertex(1))
    g.add_node(vertex('B'))
    g.add_node(vertex('C'))
    g.add_node(vertex('D'))
    edges=[(1,'B'),(1,'C'),(1,'B'),(1,'D')]
    g.add_edge(edges)
    g.print_graph()
    
    
if __name__ == "__main__":
    # execute only if run as a script
    main()
     