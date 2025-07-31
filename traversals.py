class TraverseSamplingTree:
    def __init__(self):
        pass
    
    #--------------------------Utility Functions------------------------------#
    def inorderTraversal(self,node,nodesList):
        """Performs inorder traversal of the isotope partition tree."""
        if node is None:
            return
        self.inorderTraversal(node.left,nodesList)
        nodesList.append(node)
        self.inorderTraversal(node.right,nodesList)

    def preOrderTraversal(self,node):
        """Performs preorder traversal of the isotope partition tree."""
        pass

    def iterateNodesList(self,array):
        for node in array:
            parentId = node.parentId
            currentNodeId = node.nodeId
            node.countsIsotopes['parentId'] = parentId
            node.countsIsotopes['myId'] = currentNodeId
            print(node.countsIsotopes)