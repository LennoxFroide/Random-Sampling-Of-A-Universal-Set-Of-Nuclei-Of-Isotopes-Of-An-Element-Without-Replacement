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
        # Instantiating our digraph
        self.myGraph = Digraph(comment = 'Tester')
        self.myGraph.graph_attr["rankdir"] = "TB"

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

        # Getting the furthest parent to iterate
        lastParent = self.getLastParent(array)

        for index in range(0,lastParent + 1):
            # Getting the indices of our children nodes dynamically
            firstChildIndex = index * 2  + 1
            secondChildIndex = index * 2 + 2

            # Making sure the indices are in range
            if firstChildIndex <= len(array) - 1:
                firstChild = createdNodes[firstChildIndex]
            else: # Creating a dummy node for missing left child
                firstId = str(self.generateNodeId())
                firstChild = myGraph.node(firstId," ")

            if secondChildIndex <= len(array) - 1:
                secondChild = createdNodes[secondChildIndex]
            else:# Creating a dummy node for missing right child
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

    def preprocessTree(self,root):
        """Helper function to perform the preprocessing step to building the visualizing digraph."""
        currentNode = root
        parentChildMatcher = {}
        nodeIdNodeMatcher = {}
        # Storing these values
        self.parentChildMatcher, self.nodeIDNodeMatcher = self.traverseTreeAndCreateMappers(currentNode,parentChildMatcher,nodeIdNodeMatcher,1)
    
    def traverseTreeAndCreateMappers(self,node,parentChildMap,nodeIdNodeMap,currentLevel):
        """Helper function to create two important maps: parentChildMap and nodeIdNodeMap.
        This is an important preprocessing step to building the visualizing digraph."""
        current = node
        if current is None:
            return
        # Traversing the left subtree
        self.traverseTreeAndCreateMappers(current.left,parentChildMap,nodeIdNodeMap,currentLevel + 1)
        # Processing the current node
        self.buildParentChildMapper(current,parentChildMap,currentLevel)
        self.buildNodeIdNodeMapper(current,nodeIdNodeMap)
        # Traversing the right subtree
        self.traverseTreeAndCreateMappers(current.right,parentChildMap,nodeIdNodeMap,currentLevel + 1)
        
        return (parentChildMap, nodeIdNodeMap)
    
    def buildParentChildMapper(self,node,mapper,level):
        """Helper function to match each parent with its children."""
        parentId = node.parentId
        nodeId = node.nodeId
        parentLevel = level - 1
        if parentId not in mapper:
            mapper[parentId] = [parentLevel]
        mapper[parentId].append(nodeId)
    
    def buildNodeIdNodeMapper(self,node,mapper):
        """Helper function to match each node id to the actual node."""
        nodeId = node.nodeId
        mapper[nodeId] = node
    
    def getListOfParentNodes(self):
        """Helper function to get the ids of all the parent nodes of the
        isotope tree."""
        parentChildMap = self.parentChildMatcher
        # Sorting the map according to the level of parent nodes in the tree
        sortedParentChildMap = dict(sorted(parentChildMap.items(), key=lambda item: item[1][0]))
        return list(sortedParentChildMap.keys())
    
    def buildNodeIdDigraph(self,parentsList):
        """Helper function to plot the isotope tree with the node ids in each node."""
        for index in range(1,len(parentsList)):
            parentId = parentsList[index]
            self.myGraph.node(str(parentId),str(parentId))
            childrenList = self.parentChildMatcher[parentId]
            if len(childrenList) > 1:
                firstChildId = str(childrenList[1])
                self.myGraph.node(firstChildId,firstChildId)
                if len(childrenList) > 2:
                    secondChildId = str(childrenList[2])
                    self.myGraph.node(secondChildId,secondChildId)
                else:
                    secondChildId = str(self.generateNodeId)
                    self.myGraph.node(secondChildId,"")
            else:
                firstChildId = str(self.generateNodeId)
                self.myGraph.node(firstChildId,"")
                secondChildId = str(self.generateNodeId)
                self.myGraph.node(secondChildId,"")
            # Adding edges
            self.myGraph.edge(str(parentId),firstChildId)
            self.myGraph.edge(str(parentId),secondChildId)

        # Displaying our digraph
        self.myGraph.render('NodalIds',view=True)
    
    def buildIsotopeDistributionDigraph(self,parentsList):
        # TODO: Change hard coded node-token generation to be dynamic.
        """Helper function to plot the isotope tree with the distribution of
        each isotope shown in each node."""
        for index in range(1,len(parentsList)):
            parentId = parentsList[index]
            parentNode = self.nodeIDNodeMatcher[parentId]
            parentNodeToken = self.getNodalToken(parentNode)
            self.myGraph.node(str(parentId),parentNodeToken[0] + "\n" + parentNodeToken[1] + "\n" + parentNodeToken[2])
            childrenList = self.parentChildMatcher[parentId]
            if len(childrenList) > 1:
                firstChildId = str(childrenList[1])
                firstChildNode = self.nodeIDNodeMatcher[childrenList[1]]
                firstNodeToken = self.getNodalToken(firstChildNode)
                self.myGraph.node(firstChildId,firstNodeToken[0] + "\n" + firstNodeToken[1] + "\n" + firstNodeToken[2])
                if len(childrenList) > 2:
                    secondChildId = str(childrenList[2])
                    secondChildNode = self.nodeIDNodeMatcher[childrenList[2]]
                    secondNodalToken = self.getNodalToken(secondChildNode)
                    self.myGraph.node(secondChildId,secondNodalToken[0] + "\n" + secondNodalToken[1] + "\n" + secondNodalToken[2])
                else:
                    secondChildId = str(self.generateNodeId)
                    self.myGraph.node(secondChildId,"")
            else:
                firstChildId = str(self.generateNodeId)
                self.myGraph.node(firstChildId,"")
                secondChildId = str(self.generateNodeId)
                self.myGraph.node(secondChildId,"")
            # Adding edges
            self.myGraph.edge(str(parentId),firstChildId)
            self.myGraph.edge(str(parentId),secondChildId)

        # Displaying our digraph
        self.myGraph.render('IsotopeDistribution',view=True)

    def getNodalToken(self,node):
        """Helper function that takes the isotope distribution data and converts
        them into strings to allow for easier isotope tree plot generation."""
        isotopeCounts = node.countsIsotopes
        nodalTokens = list()
        for key, value in isotopeCounts.items():
            nodalTokens.append(str(key) + ":" + str(int(value)))
        return nodalTokens

    
#-------------Executable--------------------#
array = ['A','B','C','D','E','F','G','H','I','J']
graph = GraphVisualizer()
# graph.generateThreeNodalTree(array)