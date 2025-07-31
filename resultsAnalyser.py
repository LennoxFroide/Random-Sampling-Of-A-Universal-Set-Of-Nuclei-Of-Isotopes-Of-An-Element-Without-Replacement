import Sampling as smp
import traversals as travs
sampler = smp.Sampling(1)
sampler.printHere()
tree = sampler.generateSampleTree(1000,[0.50,0.25,0.25],0.38,True,24)
# print(tree.root.right.parentLevel)
print(sampler.nodeIds)
print(tree.root.right.countsIsotopes)
print(tree.root.right.parentId)
print(tree.root.left.parentId)
listOfNodes = list()
traverse = travs.TraverseSamplingTree()
traverse.inorderTraversal(tree.root,listOfNodes)
print(len(listOfNodes))
traverse.iterateNodesList(listOfNodes)

