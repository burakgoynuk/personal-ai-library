import copy
# CLASS DEFINITIONS
class Node:
	nodeId = 0
	nodeType = ""
	successors = []
	rewards = []
	actionList = []

class Action:
	actionId = 0
	appliedNodes = []
	rewards = []
	transitions = []

 # INPUT FILE
inputFile = open('hw4.inp', 'r')

# GLOBALS
vertexSequence = ""
allNodes = []
discountFactor1 = 0
discountFactor2 = 0
numOfTransitionsQL = 0
numOfActions = 0
allActions = []
nodesInRightUniverse = []
nodesInLeftUniverse = []


def nodeInLeft( nodeType ):
	if nodeType == 'R' or nodeType == 'V' or nodeType == 'O':
		return True	
	return False

def nodeInRight( nodeType ):
	if nodeType == 'O' or nodeType == 'S' : # nodeType == 'G' ???
		return True	
	return False	
		

def nodeIndexInAllNodes( nodeId ):
	global allNodes

	i = 0
	while i < len( allNodes ):
		if allNodes[i].nodeId == nodeId:
			return i
		i += 1
	return -1			


def readInput():
	
	global vertexSequence
	global allNodes
	global discountFactor1
	global discountFactor2
	global numOfTransitionsQL
	global numOfActions
	global allActions
	global nodesInRightUniverse
	global nodesInLeftUniverse

	# 1. Line
	vertexSequence = inputFile.readline()
	#vertexSequence = vertexSequence.split(' ')
	tempId = 0
	for nodeType in vertexSequence:
		if nodeType == "R" or nodeType == "V" or nodeType == "O" or nodeType == "S" or nodeType == "G":
			newNode = Node()
			newNode.nodeId = tempId
			newNode.nodeType = nodeType
			
			if nodeInLeft( nodeType ):
				nodesInLeftUniverse.append( tempId )

			if nodeInRight( nodeType ):	
				nodesInRightUniverse.append( tempId )


			newNode.successors =  []
			newNode.rewards = []
			newNode.actionList = []
			allNodes.append( newNode )
			tempId += 1

		
	'''		
	print "Left Uni: "
	print nodesInLeftUniverse
	print "Right Uni:"
	print nodesInRightUniverse		


	print "Node List: "
	print len(allNodes)	
	'''

	# 2. Line	
	secondLine = inputFile.readline().split(' ')
	#print secondLine
	discountFactor1 = float(secondLine[0])
	#print "Here!"
	discountFactor2 = secondLine[1].strip()
	discountFactor2 = float(discountFactor2)
	# 3. Line
	numOfTransitionsQL = int(inputFile.readline())
	# 4. Line to All Transitions
	i = 0
	while i < numOfTransitionsQL:
		oneLine = inputFile.readline().split(' ')
		
		node1 = int(oneLine[0])
		node2 = int(oneLine[1])
		tempReward = int(oneLine[2])

		allNodes[ node1 ].successors.append( node2 )
		allNodes[ node1 ].rewards.append( tempReward )

		i += 1
	
	
	numOfActions = int(inputFile.readline())
	
	# NUM OF ACTIONS DEGIL!!!!
	# RIGHT UNIVERSE TE HER NODE ICIN!!!
	i = 0
	while i < len( nodesInRightUniverse ):
		oneLine = inputFile.readline().split(' ')
		
		node1 = int(oneLine[0])
		
		oneLine = oneLine[1:]
		for action in oneLine:
			allNodes[ node1 ].actionList.append( int(action) )
		i += 1	
		
	wholeLines = []
	while(True):
		oneLine = inputFile.readline().strip()
		if oneLine == 'E':
			break
		if oneLine == '#':
			
			newAction = Action()
			newAction.appliedNodes = []
			newAction.transitions = []
			newAction.rewards = []
			
			actionName = wholeLines[0] 
			#print "Action Name: ", actionName
			newAction.actionId = int(actionName.split(' ')[2])
			
			wholeLines = wholeLines[1:]
			
			betweenDolars = []
			oneNode = []
			
			for char in wholeLines: 
				if char == '$':
					betweenDolars.append( oneNode )
					oneNode = []	
				
				else:	
					oneNode.append( char )	
			
			#print "Dolars: "
			#print betweenDolars
			
			for nodeInfo in betweenDolars:
				#print "Node Info is: ", nodeInfo
				nodeId = int(nodeInfo[0])
				reward = int(nodeInfo[1])
				newAction.appliedNodes.append( nodeId )
				newAction.rewards.append( reward )
				transactions = nodeInfo[2:]
				for trans in transactions:
					newTrans = []
					trans = trans.split(' ')
					nodeId2 = int(trans[0])
					prob1 = int(trans[1])
					newTrans = [ nodeId, nodeId2, prob1 ]
					newAction.transitions.append( newTrans )
				
				
				'''
					CONT from HERE!!
				
				'''
			
			
			
			allActions.append( newAction )
			
			
			
			wholeLines = []
			
			
			#break
		else:
			wholeLines.append(oneLine)
	#print "Whole: ", wholeLines	
	
	
	'''
	print "**********"
	for action in allActions:	
		print "Action: ", action.actionId	
		print action.appliedNodes
		print action.rewards
		print action.transitions
	print "*************"
	for node in allNodes:
		print "Node: ", node.nodeId
		print node.nodeType
		print node.actionList	
	'''

		
def findIndexInList( list, elem ):
	if elem in list:
		return list.index(elem)
	else:
		return -1 

def nodeInRightUniverse(node1):

	if node1.nodeType == 'R' or node1.nodeType == 'V' or node1.nodeType == 'O':
		return True
	return False	

def printMatrix(matrix):
	for line in matrix:
		for char in line:
			print char, 
		print ""	

def findMaxInRewards( list ):
	maxV = 0
	for elem in list:
		if elem != "-":
			if int(elem) > maxV:
				maxV = elem
	return maxV			 

def printValueTable( valueTable ):
	#print valueTable
	print "---Value Table---"	
	for node in valueTable:
		print "Node: ", node[0], "Value: ", node[1]

def printList( gotoList ):
	i = 0
	while i < len( gotoList ):
		print gotoList[i],
		i += 1
	
	return ""
def printPolicy( policy ):
	global allActions
	
	print "---Policy Table---"
	for node in policy:
		nodeId = node[0]
		actionId = node[1]
		action = findAction( allActions, actionId )
		
		gotoList = []
		for trans in action.transitions:
			if trans[0] == nodeId:
				gotoList.append( trans[1] )
				
		
		print "Node:", node[0], " Action:", node[1], " Go to:", printList(gotoList)	

def findActionInPolicy( node, policy ):

	for pair in policy:
		if pair[0] == node:
			return pair[1]
	return -1		

def findRewardInAction( allActions, nodeId, actionId ):
	i = 0
	while i < len( allActions ):
		if allActions[i].actionId == actionId:
			j = 0
			while j < len(allActions[i].appliedNodes):
				if allActions[i].appliedNodes[j] == nodeId:
					return allActions[i].rewards[j]
				j += 1
		i += 1
	return '#'	
					

def findAction( allActions, actionId ):
	for action in allActions:
		if action.actionId == actionId:
			return action

def findValueInTable( valueTable, targetNode ):
	for node in valueTable:
		if node[0] == targetNode:
			return node[1]

	return 0 #'#'		

def findIndexInValue( valueTable, nodeId ):
	i = 0
	while i < len( valueTable ):
		if valueTable[i][0] == nodeId:
			return i
		i += 1	

	return -1


def checkEpsilon( oldValueTable, valueTable ):
	i = 0
	while i < len( oldValueTable ):
		if abs( oldValueTable[i][1] - valueTable[i][1] ) > 0.0001:
			return "Not Same"
		i += 1
	return "Same"			
def main():
	global vertexSequence
	global allNodes
	global discountFactor1
	global discountFactor2
	global numOfTransitionsQL
	global allActions

	readInput()
	
	'''
	for node in allNodes:
		print "************************"
		print "Node Id: ", node.nodeId
		print "Node Type: ", node.nodeType
		print "Successors: ", node.successors
		print "Rewards: ", node.rewards
		print "Actions: ", node.actionList
	'''
	

	QTable = []
	i = 0
	
	QTable = []
	for node in allNodes:
		if nodeInRightUniverse(node):
			rowForNode = []
		
			for node2 in allNodes:
				if nodeInRightUniverse(node2):
					indexInSuccessors = findIndexInList(node.successors, node2.nodeId)
					if (indexInSuccessors != -1):
						rowForNode.append( 0  )
					else:
						rowForNode.append("-")
							
			QTable.append(rowForNode)


	while ( True ):
		
		inputEntered = raw_input()
		if ( inputEntered == "$" ):

			# Intiliaze Value Table & Policy
			# Policy ->  [ [ NodeId, ActionId ], .... ]
			# ValueTable -> [ [ NodeId, Value ], .... ]  
			#print "You have changed your universe!"
			
			policy = []
			valueTable = []

			#print "Node in Left: ", nodesInRightUniverse
			for node in nodesInRightUniverse:
				nodeIndex = nodeIndexInAllNodes( node )
			
				newRowPolicy = []		
				newRowValue = []
			
				newRowPolicy = [ allNodes[nodeIndex].nodeId, allNodes[nodeIndex].actionList[0] ]
				newRowValue = [ allNodes[nodeIndex].nodeId, 0 ]

				policy.append( newRowPolicy )
				valueTable.append( newRowValue )

		
			printValueTable( valueTable ) 
			printPolicy( policy )
				
			
			
			
			inputEntered = raw_input()
			if inputEntered != "c":
				
				while inputEntered != "c":
					print "This is wrong input, please type c or $"
					inputEntered = raw_input()
			
			if inputEntered == "c":
			

				'''
				print "Value Table: "
				print valueTable
				print "Policy: "
				print policy
				'''				
				
				while True: # or Epsilon check!

					# POLICY ITERATION	
					
					# Policy Evaluation:
				
				
					while ( True ):
					
						oldValueTable = copy.deepcopy( valueTable )	

						for nodeId in nodesInRightUniverse:
							actionId = findActionInPolicy( nodeId, policy )
							reward = findRewardInAction( allActions, nodeId, actionId )
							#print "NODE ID: ", nodeId
							#print "REWARD: ", reward
							action = findAction( allActions, actionId )
						
							sumTV = 0
							for transition in action.transitions:
								#print "Node: ", nodeId
								if transition[0] == nodeId: 	
									targetNode = transition[1]
									#print "Target: ", targetNode
									valueOfTarget = findValueInTable( valueTable, targetNode )
									prob = transition[2]/100.0
									#print "Value Of Target: ", valueOfTarget
									sumTV += prob*valueOfTarget

							#print "SUM: ", sumTV
							sumTV *= discountFactor2
							newValue = reward + sumTV

							index = findIndexInValue( valueTable, nodeId )
						
						
							valueTable[index][1] = newValue

					
						if checkEpsilon( oldValueTable, valueTable ) == 'Same':
							break	

					printValueTable( valueTable )	

					# Policy Improvement

				
					for nodeId in nodesInRightUniverse:
						actionId = -1
						maxQVal = -99999
						for action in allActions:
							if nodeId in action.appliedNodes:
								reward = findRewardInAction( allActions, nodeId, action.actionId )
								sumTV = 0
								for transitions in action.transitions:
									if transitions[0] == nodeId:
										targetNode = transitions[1]
										valueOfTarget = findValueInTable( valueTable, targetNode )
										prob = transitions[2]/100.0
										sumTV += prob*valueOfTarget

								sumTV *= discountFactor2
								tempQVal = reward + sumTV

								if tempQVal > maxQVal:
									maxQVal = tempQVal
									actionId = action.actionId
						index = findIndexInValue( valueTable, nodeId )
						policy[index][1] = actionId					
						
					printPolicy( policy )	
					#print "Enter:"
					inputEntered = raw_input()
					if inputEntered == "$":
						break	
					if inputEntered != "c":
						print "This is wrong input, please type c or $"
						
						while inputEntered != "c":
							if inputEntered == "$":
								return 
							print "This is wrong input, please type c or $"	
							inputEntered = raw_input()
						
						continue	
					
			break
		else:
			# Episode Entered!
			# fill & initiliaze Q - Table
					

			#printMatrix(QTable)			

			enteredEpisode = ""
			enteredEpisode = inputEntered.split(' ')

			#print "Episode: ", enteredEpisode

			i = 0
			while ( i < len(enteredEpisode)-1 ):
				sourceNode = int(enteredEpisode[i])		
				destinationNode = int(enteredEpisode[i+1])	
				#print sourceNode, destinationNode, QTable[sourceNode][destinationNode] 

				firstPart = (1 - discountFactor1)*(QTable[sourceNode][destinationNode]) 
				
				indexOfSecondInFirst = findIndexInList( allNodes[sourceNode].successors, destinationNode )
				rewardEarned = allNodes[sourceNode].rewards[indexOfSecondInFirst]
				maxOfDest = findMaxInRewards( QTable[destinationNode] )
				
				secondPart = discountFactor1*(rewardEarned + discountFactor2*maxOfDest)
				
				newQValue = firstPart + secondPart

				QTable[sourceNode][destinationNode] = newQValue
				i += 1
				
			printMatrix(QTable)	

			
	




main()
