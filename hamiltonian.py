#Taylor Heilman
#an undirected simple graph
#Feb 11, 2016

import copy
import random



class Graph(object):

    def __init__(self):
        #Graph constructor
        self.Graph = {}


    def add_vertices(self, vertices):
        #Add a list of vertices to the graph
        length = len(vertices)
        for i in range (length):
            if vertices[i] not in self.Graph:   #check if vertex exists in dictionary already
                self.Graph[vertices[i]] = []


    def delete_vertex(self, v):
        #Delete a vertex from the graph.
        if v in self.Graph:
            del self.Graph[v]           #delete key from dictionary
            for item in self.Graph:
                if v in self.Graph[item]:       #delete vertex from other keys' values
                    self.Graph[item].remove(v)
    


    def delete_edge(self, e):
        vertex1=e[0]        #first element of edge
        vertex2=e[1]        #second element of edge
        if vertex1 in self.Graph and vertex2 in self.Graph:
            if vertex1 in self.Graph[vertex2]:          #check if element1 is in element2's values
                    self.Graph[vertex2].remove(vertex1)     #remove element1 from values if true
            if vertex2 in self.Graph[vertex1]:          #check if element2 is in element1's values
                    self.Graph[vertex1].remove(vertex2) #remove element2 from values if true
          

    def vertices(self):
        #Return a list of nodes in the graph.
        return list(self.Graph.keys())

    def add_edges(self, edges):
        #Add a list of edges to the graph
        edges = list(edges)
        length1 = len(edges)
        for i in range (length1):
            temp = edges[i]
            first = temp[0]     #first vertex of pair
            second = temp[1]    #second vertex of pair

            if first not in self.Graph:         #Vertex1 is not in dictionary
                self.Graph[first] = [second]
            else:
                if second not in self.Graph[first]:     #Vertex1 in dictionary but Vertex 2 isn't
                    self.Graph[first].append(second)

            if second not in self.Graph:        #Vertex2 is not in dictionary
                self.Graph[second] = [first]

            else:
                if first not in self.Graph[second]:     #Vertex2 is in dictionary but Vertex1 isn't
                    self.Graph[second].append(first)
                


    def edges(self):
        #Return a list of edges in the graph
        edge = []
        for vertex1 in self.Graph:
            for vertex2 in self.Graph[vertex1]:
                if (vertex2, vertex1) not in edge:      #check if inverse of edge is already in the list
                    edge.append((vertex1, vertex2))     #ex. if (u,v) is in list (v,u) won't be appended


        return edge



    
    def isCycle(self):       #modified DFS to check for cycles since we assume G is connected
        if(len(self.edges()) == 0):
           return False
           
        keys = self.vertices()
        v = keys[0]             #arbitrarily pick a vertex for v
        #step 1
        graph = copy.deepcopy(self.Graph)       #create copy of self.Graph
        S = [v]              #list
        T = []               #empty list of edges
        history = [v]        #history of vertices that are used as bstar
        bstar = v
        pstar = v
        label = []           #list to hold labels
        label.append(v)     #label v as 0
        U1 = graph.keys()   #keys of dict
        U = []              #list of unlabeled vertices
        for item in U1:
            U.append(item)
        U.remove(v)         #remove v since it is labeled
        U.sort()
        neighbors = graph[v]        #list of neighbors of v
        neighbors.sort()
        intersection = list(set(U) & set(neighbors))        #U intersect neighbors
        intersection.sort()
        #step 2
        while (True):
            while (intersection):
                w = intersection[0]
                label.append(w)          #label neighbor of bstar
                T.append((bstar,w))      #add edge to T
                U.remove(w)              #remove labeled vertex from unlabeled list
                pstar = bstar               #help for backtracking
                bstar = w
                history.append(bstar)       #update history list
                neighbors = graph[bstar]    #get niehgbors
                neighbors.sort()
                intersection = list(set(U) & set(neighbors)) #get intersect of U and neighbors
                intersection.sort()

        #MAIN EDIT
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                cycle = list(set(history) & set(neighbors)) #take the intersection of the bstar's neighbors and history(visited vertices)    
                if (len(cycle) >= 2):                    # IF 2 OR MORE NEIGHBORS OF CURRENT VERTEX HAVE BEEN VISITED
                    return (True)              #A CYCLE HAS BEEN FOUND, RETURN FALSE
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            neighbors = graph[bstar]
            neighbors.sort()
            intersection = list(set(U) & set(neighbors))     #used to check for halting condition
            intersection.sort()

            
            if (len(intersection) == 0):    #if U intersect neighbors = []
                num = history.index(bstar)
                bstar = history[num-1]      #bstar = pstar
            
            if (bstar == v and intersection == [] and len(U) == 0): #halting condition
                return False        #IF DFS COMPLETES NORMALLY, RETURN TRUE

            if (intersection != []):
                history.append(bstar)       #update history list




        
        
    def Hamiltonian(self):
        head = random.choice(self.vertices())          #randomly choose vertex as head
        unusedEdges = self.edges()                      #list of edges that haven't been used yet
        cycle = copy.deepcopy(self.Graph)               #copy graph

        x = len(self.edges())
        while(len(self.edges()) > 0):                               #remove all edges and vertices from self.Graph so we can append edges of the
            self.delete_edge(unusedEdges[x-1])                      #Head path and can use isCycle to check
            x = x-1
        while(len(self.vertices()) > 0):
              self.delete_vertex(self.vertices()[0])
              
        while(len(unusedEdges) > 0 and self.isCycle() == False):  #isCycle = True means we found a cycle
            if (len(cycle[head]) > 0):
                nextEdge = cycle[head]
                nextEdge = nextEdge[0]
                if(nextEdge not in self.vertices()):    #vertex u is not in the path already
                    self.add_edges([(head,nextEdge)])
                    cycle[head].remove(nextEdge)
                    cycle[nextEdge].remove(head)
                    if( ((head,nextEdge)) not in unusedEdges):
                        unusedEdges.remove((nextEdge,head))
                    else:
                        unusedEdges.remove((head,nextEdge))
                    head = nextEdge
                else:
                    length = len(self.vertices())
                    for i in range (length):
                        if(self.vertices()[i] == nextEdge):
                            u = self.vertices()[i]
                            self.add_edges([(head,u)])
                            if( ((head,nextEdge)) not in unusedEdges):
                                
                                unusedEdges.remove((u,head))
                            else:
                                unusedEdges.remove((head,u))
    
                    
        if(self.isCycle() == True):
            print("Hamiltonian Cycle Found:")
            return self.Graph
        else:
            return("No Hamiltonian Cycle")
            





def main():
    #call functions from here
    G = Graph()
    print("Should return cycle")
    G.add_edges([(1,2),(2,3),(3,4),(4,1)])
    print(G.Hamiltonian())
    print('\n')
    
    H = Graph()
    print("Should return cycle")
    H.add_edges([(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,1)])
    print(H.Hamiltonian())
    print('\n')

    I = Graph()
    print("Should not return cycle")
    I.add_edges([(1,2)])
    print(I.Hamiltonian())
    print('\n')


    J = Graph()
    print("Should not return cycle")
    J.add_edges([(1,2),(2,3),(3,4)])
    print(J.Hamiltonian())
   
    

    


main()

