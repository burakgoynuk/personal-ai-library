import copy
import math

idCounter = 0
finalStates = []
heuristicSelection = 0

# return found objects in a list containing info about them
# [ [obj1ID, obj1RowFirst, obj1ColFirst, obj1RowSecond, obj1ColSecond], [...] ]

def returnObjects( numCols, numRows, startMatrix ):
	ids = []
	objList = []
	for row in range(0, numRows):
		for col in range(0, numCols):
			if startMatrix[row][col] != 0:
				if (startMatrix[row][col] in ids) == False:					
					ids.append(startMatrix[row][col])
					objList.append([startMatrix[row][col], row, col, row, col])
				else:
					for i in range(len(objList)):
						if objList[i][0]  ==  startMatrix[row][col]:
							objList[i][3] = row
							objList[i][4] = col
							break
	
	
	return objList

					
			
def calculateHeuristic(selectedHeuristic, state, goalStates):
	
	minHe = 1000000
	tempHe = 1111111
	
	
	if selectedHeuristic == 0:
		
		for goal in goalStates:	
			minHe = 1000000 
			tempHe = 0
			for obj1 in state.objList:
				for obj2 in goal.objList:
					if obj1.identi == obj2.identi:
						rowT = obj1.posRow - obj2.posRow
						colT = obj1.posCol - obj2.posCol
						rowT = abs(rowT)
						colT = abs(colT)
						tempHe = tempHe + rowT + colT
		
			if tempHe < minHe: 
				minHe = tempHe			
	
	
		return minHe
	
	
	else:
		
		for goal in goalStates:	
			minHe = 1000000 
			tempHe = 0
			for obj1 in state.objList:
				for obj2 in goal.objList:
					if obj1.identi == obj2.identi:
						rowT = obj1.posRow - obj2.posRow
						colT = obj1.posCol - obj2.posCol
						rowT *= rowT
						colT *= colT
						tempHe = tempHe + math.sqrt(rowT + colT)
		
			if tempHe < minHe: 
				minHe = tempHe			
	
	
		return minHe
							
	return minHe				



def expandState( state, numRows, numCols ):
	
	global idCounter
	global finalStates
	global  heuristicSelection
	
	
	expandedList = []
	#availables = findAvailableCoordinates(state, numRows, numCols)
	
	availables = []
	notAvailables = []
	
	for oneObject in state.objList:
		for wid in range(oneObject.width):
			for hig in range(oneObject.heigth):
				notAvailables.append((oneObject.posRow+hig, oneObject.posCol+wid))
				
				
	for x in range(numRows):
		for y in range(numCols):
			availables.append((x, y))	
	
	availables = [item for item in availables if item not in notAvailables]	
	
	
	
	for i in range(len(state.objList)):
		
		anObject = state.objList[i]
		
		canRight = False
 		canLeft = False		
		canUp = False
		canDown = False
		
		#### RIGHT
		if anObject.posCol + anObject.width + 1 > numCols:
			canRight = False
		else:
			flag = True
			for h in range(anObject.heigth):
				if (anObject.posRow+h, anObject.posCol+anObject.width) not in availables:
					
					flag = False
					break;

			canRight = flag
		
		
		#### LEFT
		if anObject.posCol <= 0:
			canLeft = False
		else:
			flag = True
			for h in range(anObject.heigth):
				if (anObject.posRow+h, anObject.posCol-1) not in availables:
					flag = False
					break;

			canLeft = flag
		
		
		#### UP 
		if anObject.posRow <= 0:
			canUp = False
		else:
			flag = True
			for w in range(anObject.width):
				if (anObject.posRow-1, anObject.posCol+w) not in availables:
					flag = False
					break;

			canUp = flag
		
		#### DOWN
		if anObject.posRow + anObject.heigth + 1 > numRows:
			canDown = False
		else:
			flag = True
			for w in range(anObject.width):
				if (anObject.posRow+anObject.heigth, anObject.posCol+w) not in availables:
					flag = False
					break;

			canDown = flag
				
		
		
		if canRight:       # i is the index of looking object in objList
		
			addedState = copy.deepcopy(state)
			addedState.g = state.g + 1
			
			addedState.parent = state.id
			addedState.id = idCounter
			idCounter = idCounter + 1
			
			addedState.objList[i].posCol = state.objList[i].posCol + 1
			
			addedState.h = calculateHeuristic(heuristicSelection, addedState, finalStates)
			addedState.f = addedState.h + addedState.g
			
			
			
			expandedList.append(addedState)
			
		
		if canLeft:
	
			addedState = copy.deepcopy(state)
			addedState.g = state.g + 1
			
			addedState.parent =  state.id
			addedState.id = idCounter
			idCounter = idCounter + 1
			
			addedState.objList[i].posCol = state.objList[i].posCol - 1
			
			addedState.h = calculateHeuristic(heuristicSelection, addedState, finalStates)
			addedState.f = addedState.h + addedState.g
			
			
			
			expandedList.append(addedState)
		
		
		
		if canUp:
	
			addedState = copy.deepcopy(state)
			addedState.g = state.g + 1
			
			addedState.parent = state.id
			addedState.id = idCounter
			idCounter = idCounter + 1
			
			addedState.objList[i].posRow = state.objList[i].posRow - 1
			
			addedState.h = calculateHeuristic(heuristicSelection, addedState, finalStates)
			addedState.f = addedState.h + addedState.g
			
			
			
			expandedList.append(addedState)
		
		
		
		if canDown: 
	
			addedState = copy.deepcopy(state)
			addedState.g = state.g + 1
			
			addedState.parent = state.id
			addedState.id = idCounter
			idCounter = idCounter + 1
			
			addedState.objList[i].posRow = state.objList[i].posRow + 1
			
			addedState.h = calculateHeuristic(heuristicSelection, addedState, finalStates)
			addedState.f = addedState.h + addedState.g
			
			
			
			
			expandedList.append(addedState)	


	return expandedList




def findMinFValue( stateList ):
	tempMin = 1000000
	returnState = State()
	
	
	for state in stateList:
		if state.f < tempMin:
			tempMin = state.f
			returnState = state
			
			
	return returnState				
			
def sameObject( obj1, obj2 ):

	return (obj1.posRow == obj2.posRow) and (obj1.posCol == obj2.posCol) and (obj1.identi == obj2.identi) and (obj1.width == obj2.width) and (obj1.heigth == obj2.heigth)
	
	
def objInList( obj1, objList ):


	for obj2 in objList:
		if (obj1.posRow == obj2.posRow) and (obj1.posCol == obj2.posCol) and (obj1.identi == obj2.identi) and (obj1.width == obj2.width) and (obj1.heigth == obj2.heigth):
			return True
			
	return False
	
	
def sameState( state1, state2 ):

	for obj2 in state2.objList:
		if objInList( obj2, state1.objList ) == False:
			return False
			
			
	return True				
			 	




def stateInList( state, stateList ):

	ret = -1

	for i in range(len(stateList)):
		if sameState(state, stateList[i]):
			return i
			
			
	return -1		 
		

def constructPathList(state, stateList):
	
	pathList = []
	currentState = state
	
	while currentState.id != 0:
		
		pathList.append( currentState )
		
		for oneState in stateList:
			if oneState.id == currentState.parent:
				currentState = oneState	


	pathList.append( currentState )
	return pathList
	
def printStates( pathListReverse, numRow, numCol ):

	lenList = len(pathListReverse)
	it = lenList - 1
	
	while it >= 0:
		printOneState( pathListReverse[it], numRow, numCol )
		it -= 1
		
		
def printOneState( state, numRow, numCol ):

	matrixS = []
	for i in range(numRow):
		rowMatrix = []
		for j in range(numCol):
			 rowMatrix.append(0)
		matrixS.append( rowMatrix )	 
	
	for obj in state.objList:
		for w in range(obj.width):
			for h in range(obj.heigth):
				matrixS[obj.posRow + h][obj.posCol + w] = obj.identi  
			 
	
	for i in range(numRow):
		for j in range(numCol):
			print matrixS[i][j],
		print "\n",		

	print ""

class State: 	
	def __cmp__(self, other):
		if self.f > other.f:
			return 1
		elif self.f < other.f:
			return -1
		else:
			return 0
	
	
	objList = []   # obj's left corner position, width, heigth, number
	f = 0
	g = 0
	h = 0
	parent = -1
	id = 0
	
	

class Object:

	def __cmp__(self, other):
		if self.identi > other.identi:
			return 1
		elif self.identi < other.identi:
			return -1
		else:
			return 0


	
	posRow = 0
	posCol = 0
	identi = 0
	width = 0
	heigth = 0	
	
	
				
		
#allStates  = []	 #  the first is Start, then final states
openList = []
closeList = []

startMatrix = []
finalMatrixes = []
iterator = 0




inputFile = open('hw1.inp', 'r')
numberOfTasks = int (inputFile.readline()) 



while iterator < numberOfTasks:
	idCounter = 0
	start = raw_input()
	
	# heuristic selection 
	# 0 for Manhattan
	# 1 for my own
	
	heuristicSelection = int (inputFile.readline())
	
	line = inputFile.readline()
	numRows = int(line.split(" ")[0])
	numCols = int(line.split(" ")[1])
	numPieces = int(line.split(" ")[2])
	numFinals = int(line.split(" ")[3])
	#print numRows, numCols, numPieces, numFinals
	 
		
	line = inputFile.readline() # read S char
		
	for i in range(numRows):
		line = inputFile.readline()
		line = line.split(" ")
		newRow = []
		for j in range(numCols):
			newNum = int(line[j])
			newRow.append(newNum)
		startMatrix.append(newRow)
	
	
	
	
	for k in range(numFinals):
		line = inputFile.readline() # read F char
		finalMatrix = []
		for i in range(numRows):
			line = inputFile.readline()
			line = line.split(" ")
			newRow = []
			for j in range(numCols):
				newNum = int(line[j])
				newRow.append(newNum)
			finalMatrix.append(newRow)
		finalMatrixes.append(finalMatrix)				

	
	startState = State()
	startState.g = 0
	startState.id = idCounter
	idCounter = idCounter + 1
	startState.parent = -1
	startObjList = []
	
	
	
	startObjList = returnObjects( numCols, numRows, startMatrix )
		
	#### Find one start state	
	startState.objList = []
	for obj in startObjList:
		newObj = Object()
		newObj.posRow = obj[1]
		newObj.posCol = obj[2]
		newObj.identi = obj[0]
		newObj.width = obj[4] - obj[2] + 1
		newObj.heigth = obj[3] - obj[1] + 1
		startState.objList.append(newObj)
	
	#printOneState(startState, numRows, numCols)
	#### Construct all final states
	#### And append them allStates
	for i in range(len(finalMatrixes)):
		finalObjList = []
		finalObjList = returnObjects( numCols, numRows, finalMatrixes[i] )
		endState = State()
		endState.id = idCounter
		idCounter = idCounter + 1
		
		endState.objList = []
		for obj in finalObjList:
			newObj = Object()
			newObj.posRow = obj[1]
			newObj.posCol = obj[2]
			newObj.identi = obj[0]
			newObj.width = obj[4] - obj[2] + 1
			newObj.heigth = obj[3] - obj[1] + 1
			endState.objList.append(newObj)			
		finalStates.append(endState)
		#allStates.append(endState)

	startState.h = calculateHeuristic( heuristicSelection, startState, finalStates )
	openList.append(startState)

	
	flag = 1
	
	while len(openList) != 0:
		
	#	print "Loop"
		current = findMinFValue(openList)
		
		
		
		
		if stateInList(current, finalStates) != -1:
			pathListReverse = constructPathList( current, closeList )
			printStates( pathListReverse, numRows, numCols )
			flag = 0
			
			break
				
			
		openList.remove(current)
		closeList.append(current)
		
		expandedList = expandState(current, numRows, numCols)
		
		for neighbour in expandedList:
			
			if stateInList(neighbour, closeList) != -1:
				continue
				
			tentative_g = current.g + 1
			index = stateInList(neighbour, openList) 
			
			if index != -1:
				if openList[index].g > tentative_g:  
				
					openList[index].parent = current.id
					openList[index].g = tentative_g
					openList[index].f = openList[index].g + openList[index].h
				
			
			else:
				openList.append( neighbour )
				
		
	if flag == 1:
		print "FAILURE"			
   


	startMatrix = []
	finalMatrixes = []	 
	openList = []
	closeList = []
	startObjList = []
	finalStates = []
	startState = []
	pathListReverse = []
	iterator = iterator+1


inputFile.close()	








