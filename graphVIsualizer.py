from graphviz import Digraph
import numpy as np
"""
dot = Digraph(comment="Test Tree")
dot.node("A",'myid:1, myparentId: 2')
dot.node("B",'myid:3, myparentId: 4')
dot.node("C",'myid:5, myparentId: 6')
dot.edge("A","B")
dot.edge("A","C")
print(dot.body[0])
print(type(dot.body[1]))
print(dot.body[2])
dot.render("myTestTree",view=True)
"""
class GraphVisualizer:
    def __init__(self):
        self.nodeIDNodeMatcher = None
        self.parentChildMatcher = None

    #------------------------------------Utility Methods-----------------------------------------------------#
    def generateThreeNodalTree(self, array):
        """Helper function to create the diagraph and add out isotope subsets as the graph's nodes."""
        myGraph = Digraph(comment = 'Tester')
        myGraph.graph_attr["rankdir"] = "TB"
        createdNodes = list()

        for node in array:
            nodeID = node
            myGraph.node(node,node)
            createdNodes.append(nodeID)
        lastParent = self.getLastParent(array)

        for index in range(0,lastParent + 1):
            firstChildIndex = index * 2  + 1
            secondChildIndex = index * 2 + 2
            # Making sure the indices are in range
            if firstChildIndex <= len(array) - 1:
                firstChild = createdNodes[firstChildIndex]
            else: # Creating a dummy node
                firstId = str(self.generateNodeId())
                firstChild = myGraph.node(str(firstId)," ")
            if secondChildIndex <= len(array) - 1:
                secondChild = createdNodes[secondChildIndex]
            else:
                secondId = str(self.generateNodeId())
                myGraph.node(secondId," ")
                secondChild = secondId
            myGraph.edge(createdNodes[index],firstChild)
            myGraph.edge(createdNodes[index],secondChild)
        myGraph.render('ThreeNodal',view=True)


    def getLastParent(self,array):
        """Helper function to get the very last parent node in the tree."""
        return int(len(array) / 2) - 1 


    def generateNodeId(self):
        """Helper function to generate a random id for an empty node to be added
        as a placeholder in the Digraph."""
        currentId = np.random.random_integers(low=10000,high=10000*2,size=None)
        # while currentId in self.nodeIds:
        # currentId = np.random.random_integers(low=10000,high=10000*2,size=None)
        return currentId
    

    def createEdges(self, graph, parent, firstChild, secondChild):
        """Helper function to create a directed edge from the parent node to children nodes."""
        graph.edge(parent,firstChild)
        graph.edge(parent,secondChild)

array = ['A','B','C','D','E','F','G','H','I','J','K','L']
# generateThreeNodalTree(array)