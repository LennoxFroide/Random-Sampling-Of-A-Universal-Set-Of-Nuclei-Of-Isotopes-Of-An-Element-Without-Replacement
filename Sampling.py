import numpy as np
import copy as cp
class ElementProperties:
    """Stores the cardinality of the universal set of particles of an element and
    the number of different isotopes that the element has."""
    def __init__(self,sizeofUniversalSet,numberOfIsotopes):
        self.universalSetCardinality = sizeofUniversalSet
        self.numberOfIsotope = numberOfIsotopes

class IsotopeTree:
    """Binary tree where each node is a partition of the universal set.
    You can directly track which two subsets arise from randomly selecting elements of
    a particular subset down the tree."""
    def __init__(self,root):
        self.root = root

class IsotopeNode:
    """Node to store the isotopes that belong to a specific partition/subset of the 
    universal set of particles"""
    def __init__(self,countsDictionary,parentId,nodeId):
        self.parentId = parentId
        self.nodeId = nodeId
        self.countsIsotopes = countsDictionary
        self.cardinality = self.getCardinality(countsDictionary)
        self.left = None
        self.right = None
    
    def getCardinality(self,isotopeMapper): # O(numberOfIsotopes) time | O(1) space
        cardinality = 0
        for _, value in isotopeMapper.items():
            cardinality += value
        
        return cardinality

class Sampling:
    def __init__(self,value):
        self.value = value
        self.nodeIds = set()

    def printHere(self):
        print("Sampler is live!")
    
    #------------------------------Utility Functions--------------------------------------#
    def initializeCountsIsotopes(self,isotopeDistribution,cardinality):
        """Takes in an array containing the portion of the particles in the universal
        set that belong to a specific isotope of an element."""
        countsIsotopes = dict()
        currentIsotopeIndex = 1
        for distribution in isotopeDistribution:
            countsIsotopes[currentIsotopeIndex] = distribution * cardinality
            currentIsotopeIndex += 1
        return countsIsotopes
       
    def randomParticleSelector(self,ratioOfSelection,countsIsotopes):
        # For each new subset the distribution of particles will differ so we need
        # to ensure we only sample from existing subset of exisiting particles
        availableParticles = cp.deepcopy(countsIsotopes)
        # Initializing map to store the isotopes picked in the new subset
        isotopeCounts = {isotopeIndex:0 for isotopeIndex in countsIsotopes.keys()}
        totalNumberOfParticles = self.getCardinality(countsIsotopes)
        particlesToSelect = ratioOfSelection * totalNumberOfParticles

        while particlesToSelect > 0:
            # Selecting an particle which will be one of the isotopes
            isotopeSelected = np.random.random_integers(low=1,high=len(countsIsotopes),size=None)
            if availableParticles[isotopeSelected] > 0:
                isotopeCounts[isotopeSelected] += 1
                availableParticles[isotopeSelected] -= 1
                particlesToSelect -= 1
            else:
                continue
        return isotopeCounts
    
    def generateSampleTree(self,numberOfParticles,isotopeDistribution,samplingRatio,epochal=True,epochs=None,minCardinality=None):
        # Storing the properties of the element
        elementCharacteristics = ElementProperties(numberOfParticles,len(isotopeDistribution))
        # Initializing the root node
        rootNodeIsotopeCounts = self.initializeCountsIsotopes(isotopeDistribution,numberOfParticles)
        nodeId = self.generateNodeId()
        self.nodeIds.add(nodeId)
        rootNode = IsotopeNode(rootNodeIsotopeCounts,0,nodeId)
        samplingTree = IsotopeTree(rootNode)
        # Grabbing our first set
        currentNode = rootNode
        if epochal:
            self.performEpochalSampling(currentNode,samplingRatio,epochs)
        else:
            self.subsetSizeRestrictiveSampling(currentNode,samplingRatio,minCardinality)
        return samplingTree

    def performEpochalSampling(self,node,samplingRatio,epochs):
        # Not splitting single element subsets even when we have more epochs
        if node.cardinality == 1:
            return 
        if epochs > 0:
            # Selecting particles through random picks
            leftNodeElements = self.randomParticleSelector(samplingRatio,node.countsIsotopes)
            rightNodeElements = self.getRightchildElements(node.countsIsotopes,leftNodeElements)
            # Initializing left and right children nodes
            leftNodeId = self.generateNodeId()
            self.nodeIds.add(leftNodeId)
            rightNodeId = self.generateNodeId()
            self.nodeIds.add(rightNodeId)
            leftNode = IsotopeNode(leftNodeElements,node.nodeId,leftNodeId)
            rightNode = IsotopeNode(rightNodeElements,node.nodeId,rightNodeId)
            # Connecting out children nodes/ subsets to their parent node/superset
            node.left = leftNode
            node.right = rightNode
            # Sampling from the newly created subsets
            self.performEpochalSampling(leftNode,samplingRatio,epochs/2 - 1)
            self.performEpochalSampling(rightNode,samplingRatio,epochs/2 - 1)
            # self.performEpochalSampling(leftNode,samplingRatio,epochs - 1)
            # self.performEpochalSampling(rightNode,samplingRatio,epochs - 1)

        return 
    def getRightchildElements(self,mainSetElements,subSetElements):
        rightChildElements = {}
        for key in mainSetElements.keys():
            isotopeCountsInSet = mainSetElements[key]
            isotopeCountsInSubSet = subSetElements[key]
            isotopeCountsInComlementarySubset = isotopeCountsInSet - isotopeCountsInSubSet
            rightChildElements[key] = isotopeCountsInComlementarySubset
        return rightChildElements

    def getCardinality(self,isotopeMapper): # O(numberOfIsotopes) time | O(1) space
        cardinality = 0
        for _, value in isotopeMapper.items():
            cardinality += value
        
        return cardinality
    
    def generateNodeId(self):
        currentId = np.random.random_integers(low=10000,high=10000*2,size=None)
        while currentId in self.nodeIds:
            currentId = np.random.random_integers(low=10000,high=10000*2,size=None)
        return currentId
        