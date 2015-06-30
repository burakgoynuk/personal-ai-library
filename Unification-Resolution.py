import copy
##### GLOBALS
numTask = 0
numB = 0
numG = 0 
baseLines = []
goalLines = []
parentsOfLines = [] # keeps indexes of lines in resolutions
## ALL KEPT IN BASE LINES
parsedExpressions = [] 
splittedExpressions = []
nodeExpressions = []
inputFile = ""
outputFile = ""

inputFile = open('input.txt', 'r')
outputFile = open('output.txt', 'w')

class Resolver:
	parent1 = []
	parent2 = []
	result = []	
	parent1Index = -2
	parent2Index = -2





def readFile(): 
	#global numTask
	global numB
	global numG
	global baseLines
	global goalLines
	global inputFile
	
	baseLines = []
	goalLines = []
	
	
	#inputFile = open('input6.txt', 'r')

	 
	line = inputFile.readline()
	# 	print "Line is: ",  line
	numB = int(line.split(' ')[0])
	numG = int(line.split(' ')[1])

	

	for j in range ( numB ):
		line = inputFile.readline()
		baseLines.append(line)
	for k in range ( numG ):
		line = inputFile.readline()
		baseLines.append(line)	  
	return 


def splitClausesToExpr( line ):

	openParant = 0
	listOfExpr = []
	strOfExpr = ""
	for i in range( len(line) - 1 ):
		if line[i] == '(':
			openParant += 1
		elif line[i] == ')':
			openParant -= 1
			
		if openParant == 0:
			if line[i] == ',':
				listOfExpr.append(strOfExpr)
				strOfExpr = ""					
			
			
			else :
				if line[i] == ' ':
					continue
				strOfExpr += line[i]
		else:
			strOfExpr += line[i]
	
	listOfExpr.append(strOfExpr)					

	return listOfExpr

def clearList( oneList ):
	for elem in oneList:
		if type(elem) == list:
			clearList(elem)
		elif elem == ',' or elem == '(' or elem == ')' or elem == ' ':
			oneList.remove(elem)

	return oneList

def parseExprToList( expression ):
	openParant = 0
	resultList = []
	## BASE CASE 
	## ONLY 1 ()
	
	if expression.count('(') == 1:
		i = 0
		while i < len(expression):
			if expression[i].isalpha():
				resultList.append(expression[i])
			elif expression[i] == '~':
				resultList.append( expression[i] + expression[i+1] )
				i += 1
			i += 1
		return resultList	 		
		
	
	## RECURSIVE PART
	i = 0
	while ( i < len(expression) ):	
				
		if expression[i] == '(':
			openParant += 1
		
		elif expression[i] == ')':
			openParant -= 1
			 	
		if openParant <= 1:
			if expression[i].isalpha():
				resultList.append(expression[i])
			elif expression[i] == '~':
				negatedStr = expression[i] + expression[i+1]
				resultList.append(negatedStr)
				i += 1
				
		elif openParant == 2:
			recursiveStr = ""
			poped = resultList.pop()
			recursiveStr += poped
			recursiveStr += expression[i]
			i += 1
			
			while openParant != 1:	
				oneChar = expression[i]
				recursiveStr += oneChar
				
				if expression[i] == '(':
					openParant += 1
		
				elif expression[i] == ')':
					openParant -= 1
			
				i += 1
			
			recList = parseExprToList( recursiveStr )
			
			resultList.append( recList )
		i += 1	
	return resultList

# CHANGE! 
def isStrInList ( char, lookList ):

	i = 0
	while i < len(lookList):
		if type ( lookList[i] ) != list:
			if lookList[i] == char:
				return True
				
				
		else:
			if isStrInList( char, lookList[i] ):
				return True		
		i += 1		 

	return False	

# CHANGE! 
def changeStrInList ( char, lookList, newChar ) : 
	i = 0
	while i < len(lookList):
		if type ( lookList[i] ) != list:
			if lookList[i] == char:
				lookList[i] = newChar
				
		else:
			changeStrInList( char, lookList[i], newChar )		
		i += 1		 

	return lookList

# FIND FUNCS IN EXPRESSION PARSED
def findFunctions ( expressionList ):

	resultList = []
	
	if expressionList == [] or expressionList == [[]]:
		return []	
	
	if type(expressionList) == list: 
		
		#print expressionList
		
		if ( expressionList[0][0] == '~' ):
			resultList.append(expressionList[0][1])
		else:	
			resultList.append(expressionList[0])
		
	i = 0
	while i < len(expressionList):
		if type(expressionList[i]) == list:
			resultList  = resultList + findFunctions(expressionList[i])	
		i += 1
		
	return resultList

# apply [[x, y]] to [ expression ]
def applyUnify( appliedList, expression ):
	
	for elem in appliedList:
		changeStrInList( elem[0], expression, elem[1] )
		
	return expression	
		

def compose( appliedList1, appliedList2 ):
	return appliedList1 + appliedList2 
	



# Call With Deep Copy
def unifyAlgorithm( expression1, expression2, functions1, functions2 ):
	
	if expression1 == [] and expression2 == []:
		return []
	unificationList = []
	
	# E1 == atom or E2 == atom
	if type(expression1) != list or type(expression2) != list:	
		# IF BOTH SAME ATOM, RETURN EMPTY LIST
		if expression1 == expression2:
			return []
		
		# IF E1 is VARIABLE	
		if (type(expression1) != list) and (expression1 not in functions1) and  (expression1 == expression1.lower() ) :	
			
			if isStrInList( expression1, expression2 ):
				#print "1!"
				return False
			
			else:	
				unificationList.append(expression1)
				unificationList.append(expression2)
				return [unificationList]
				
				
		# IF E2 is VARIABLE		
		if (type(expression2) != list) and (expression2 not in functions2) and (expression2 == expression2.lower()) :			
			if isStrInList( expression2, expression1 ):
				#print "2!"
				return False
			
			else:	
				unificationList.append(expression2)
				unificationList.append(expression1)
				return [unificationList]
		#print "3!"
		return False
		
	# BOTH ARE FUNCTIONS
	f1 = expression1[0]
	t1 = expression1[1:]
	
	f2 = expression2[0]
	t2 = expression2[1:]

	z1 = unifyAlgorithm( f1, f2, functions1, functions2  )
	if z1 == False:
		#print "4!"
		return False
		
	
	
	g1 = applyUnify( z1, t1 )
	g2 = applyUnify( z1, t2 )

	z2 = unifyAlgorithm( g1, g2, functions1, functions2  )
	if z2 == False:
		#print "5!"
		return False
		
	else:
		return compose(z1, z2)

	return



# takes two lines 
# return applied unification to them
# return False if no unification FOUND!!
def resolveTwoLine( expression1, expression2 ):

	unificationOccur = False
	i = 0
	func1 = findFunctions( expression1 )
	func2 = findFunctions( expression2 )
	while i < len(expression1):
	
		j = 0
		while j < len(expression2):
			
			if expression1[i][0][0] == '~' and expression2[j][0][0] != '~':
				
				expression1[i][0] = expression1[i][0][1]
				resultOfUnify = unifyAlgorithm( expression1[i], expression2[j], func1, func2 )
				expression1[i][0] = '~' + expression1[i][0][0]
				if resultOfUnify != False:
					unificationOccur = True
					expression1.pop(i)
					expression2.pop(j)
					i -= 1
					j -= 1
					
					i1 = 0
					while i1 < len( expression1 ):
						expression1[i1] = applyUnify( resultOfUnify, expression1[i1] )
						i1 += 1
						
					j1 = 0
					while j1 < len(expression2):
						expression2[j1] = applyUnify( resultOfUnify, expression2[j1] )
						j1 += 1			
					break
					
					
			elif expression1[i][0][0] != '~' and expression2[j][0][0] == '~':
						
				expression2[j][0] = expression2[j][0][1]
				resultOfUnify = unifyAlgorithm( expression1[i], expression2[j], func1, func2 )
				expression2[j][0] = '~' + expression2[j][0][0]
				if resultOfUnify != False:
					unificationOccur = True
					expression1.pop(i)
					expression2.pop(j)
					i -= 1
					j -= 1
					
					i1 = 0
					while i1 < len( expression1 ):
						expression1[i1] = applyUnify( resultOfUnify, expression1[i1] )
						i1 += 1
						
					j1 = 0
					while j1 < len(expression2):
						expression2[j1] = applyUnify( resultOfUnify, expression2[j1] )
						j1 += 1	
					break
			
			j += 1   
		i += 1	

	if unificationOccur:
		resultList = []
		i = 0
		while i < len( expression1 ):
			resultList.append( expression1[i] )
			i += 1
		i = 0
		while i < len( expression2 ):
			resultList.append( expression2[i] )
			i += 1
		return resultList
		
	else:
		return False				


'''def resolveTwoSet( nodeExpressions1, len1 ):

	resolveTwo = []
	firstList = nodeExpressions1[:len1]
	secondList = nodeExpressions1[len1:]
	
	print "First: "
	for elem in firstList:
		print elem.parent1, elem.parent2, elem.result
		
	print "Second: "
	for elem in secondList:
		print elem.parent1, elem.parent2, elem.result

'''


# TAKES SECOND CLAUSE LIST
# CARTESIEN OF THEM
# ONE LINE
def resolveLinesEachOther( nodeExpressions2 ):
	
	x = 0
	resolvedResult = []
	i = 0
	while i < len(nodeExpressions2):
		j = i + 1
		while j < len(nodeExpressions2):
			copyLine1 = copy.deepcopy( nodeExpressions2[i].result )
			copyLine2 = copy.deepcopy( nodeExpressions2[j].result )
			
			tryUnifyTwoLine = resolveTwoLine( copyLine1, copyLine2 )
			
			if tryUnifyTwoLine == False:
				x += 1
			else:
 				r1 = Resolver() 
				r1.parent1 = nodeExpressions2[i].result
				r1.parent2 = nodeExpressions2[j].result
				r1.result = tryUnifyTwoLine
 				resolvedResult.append( r1 )
 			j += 1
 		i += 1 	 


	return resolvedResult

# TAKES TWO DIFFERENT CLAUSES
# MAKE COMP WISE OF THEM
# TWO LINES
def resolveLinesDifferent( nodeExpressions1, nodeExpressions2 ):

	x = 0
	resolvedResult = []
	i = 0
	while i < len(nodeExpressions1):
		j = 0
		while j < len(nodeExpressions2):
			copyLine1 = copy.deepcopy( nodeExpressions1[i].result )
			copyLine2 = copy.deepcopy( nodeExpressions2[j].result )
			
			tryUnifyTwoLine = resolveTwoLine( copyLine1, copyLine2 )
			
			if tryUnifyTwoLine == False:
				x += 1
			else:
				r1 = Resolver()
				r1.parent1 = nodeExpressions1[i].result
				r1.parent2 = nodeExpressions2[j].result
				r1.result = tryUnifyTwoLine
				resolvedResult.append( r1 )
			j += 1
		i += 1
		
	return resolvedResult			

def printList( index ):

	global nodeExpressions
	list1 = nodeExpressions[:index]
	list2 = nodeExpressions[index:]
	
	print "List1: "
	for elem in list1:
		print elem.parent1, " - ", elem.parent2, " - ", elem.result
		
		
	print "List2: "
	for elem in list2:
		print elem.parent1, " - ", elem.parent2, " - ", elem.result		



	
def resolveAllLines( ):
	global nodeExpressions
	'''print "NODES BEFORE: "
	
	for elem in nodeExpressions:
		print elem.parent1, elem.parent2, elem.result	
	'''
	index = 0
	while True:
		
		list1 = copy.deepcopy(nodeExpressions[:index])
		list2 = copy.deepcopy(nodeExpressions[index:])
		
		result1 = resolveLinesDifferent( list1, list2 )
		result2 = resolveLinesEachOther( list2 )
		
		wholeResult = result1 + result2 
		if wholeResult == []:
			return False
		
		else:
			#index = len(wholeResult)
			i = 0
			while i < len(wholeResult):
				cp1 = copy.deepcopy( wholeResult[i] )
				nodeExpressions.append( cp1 )
				if wholeResult[i].result == []:
					#break
					return True
				# EMPTY CHECK
				# RETURN TRUE
				i += 1
			index = len(nodeExpressions) - len(wholeResult)
			#printList( index )
			j = 0
			while j < len(wholeResult):
				if wholeResult[j].result ==  []:	
					return True
				j += 1	
			
			
			
			#index = len(nodeExpressions) - len(wholeResult)	
			'''print "IN F: "
			list1 = nodeExpressions[:index]
			list2 = nodeExpressions[index:]
			
			print "List1: "
			for elem in list1:
				elem.parent1, " - ", elem.parent2, " - ", elem.result
			print "List2: "
			for elem in list2: 
				elem.parent1, " - ", elem.parent2, " - ", elem.result	
				
			print "Index: ", index
			#break			
			
	'''
	'''	
	print "Index: " ,index
	print "IN FUNCTION: "
	list1 = nodeExpressions[:index]
	list2 = nodeExpressions[index:]
	for elem in list1:
		print elem.parent1, " - ", elem.parent2, " - ", elem.result
	
	print "List 2: "
	for elem in list2:
		print elem.parent1, " - ", elem.parent2, " - ", elem.result
	'''
	
	
	#resolveTwoSet( nodeExpressions1, len1 )
	#for elem in nodeExpressions:
	#	print elem.parent1, elem.parent2, elem.result


# takes nodeExpressions[result] and returns its index
def findIndexOfLine( nodeResult ):
	
	global nodeExpressions
	findIndex = -1
	i = 0
	while i < len(nodeExpressions):
		if nodeExpressions[i].result == nodeResult:
			findIndex = i
			break
		i += 1	
	return findIndex

# each node's parent1 & parent2 are ready!
# but their parentIndexs are -1
# this function fills their index
def fillParentIndex():
	
	global nodeExpressions
	i = 0
	# Fill input lines' parent
	while i < len(nodeExpressions):
		if nodeExpressions[i].parent1 == []:
			nodeExpressions[i].parent1Index = -1
		
		if nodeExpressions[i].parent2 == []:
			nodeExpressions[i].parent2Index = -1
		i += 1
		
		
	i = 0
	while i < len(nodeExpressions):		 	
		if nodeExpressions[i].parent1Index == -2:
			tempIndex1 = findIndexOfLine( nodeExpressions[i].parent1 )
			if ( tempIndex1 != -1 ):
				nodeExpressions[i].parent1Index = tempIndex1
				
		if nodeExpressions[i].parent2Index == -2:		
			tempIndex2 = findIndexOfLine( nodeExpressions[i].parent2 )
			if ( tempIndex2 != -1 ):
				nodeExpressions[i].parent2Index = tempIndex2
		i += 1
	return 


def generateStringFromList( oneLine ):

	returnString = ""
	
	includeList = False
	
	for elem in oneLine:
		if type(elem) == list:
			includeList = True
			break
	
	# BASE CASE
	if includeList == False:
	 	i = 0
	 	while i < len(oneLine):
	 		if i == 0:
	 			returnString +=  oneLine[i] + "("
	 		elif i == len(oneLine)-1:
	 			returnString += oneLine[i] + ")"
	 		else:
	 			returnString += oneLine[i] + ","
	 		i += 1
	 	return returnString		 			
	
	# RECURSIVE PART
	i = 0
	while i < len(oneLine):
		
		if i == 0:
			returnString += oneLine[0] + "("
		
		elif type( oneLine[i] ) == list:
			returnString += generateStringFromList( oneLine[i] )
			
		else:
			returnString += oneLine[i]
		
		if (i != 0) and (i != len(oneLine)-1):	
			returnString += "," 
			
		i += 1

	returnString += ")"


	return returnString

def fillParentsList( lineResult ):

	global nodeExpressions
	global parentsOfLines
	
	index = findIndexOfLine( lineResult )
	hasParent1 = False
	hasParent2 = False

	if nodeExpressions[index].parent1Index == -1 and nodeExpressions[index].parent2Index == -1:
		return

	if nodeExpressions[index].parent1Index != -1:
		hasParent1 = True
		parentsOfLines.append( nodeExpressions[index].parent1Index )

	if nodeExpressions[index].parent2Index != -1:			
		hasParent2 = True
		parentsOfLines.append( nodeExpressions[index].parent2Index )

	if hasParent1:
		fillParentsList( nodeExpressions[index].parent1 )
	if hasParent2:
		fillParentsList( nodeExpressions[index].parent2 )		



def printLinePart( linePart ):
	generatedStr = ""
	i = 0
	while i < len(linePart):

		generatedStr += generateStringFromList( linePart[i] )
		if i != len(linePart)-1:
			generatedStr += ","	

		i += 1	
	return generatedStr

def printOneLine( line ):
	global outputFile
	
	parent1 = printLinePart( line.parent1 )
	parent2 = printLinePart( line.parent2 )
	result = printLinePart( line.result )

	 
	if result == "":
		#print parent1, "$" , parent2 , "$" , "empty_clause"
		writtenString = parent1 + "$" + parent2 + "$" + "empty_clause\n"
		outputFile.write( writtenString )
	else:
		#print parent1, "$" , parent2 , "$" , result		
		writtenString = parent1 + "$"  + parent2  + "$" + result + "\n"
		outputFile.write( writtenString )

	return

	
def printParentsList():

	global parentsOfLines
	global nodeExpressions
	global numB
	global numG

	i = 0
	while i < len( parentsOfLines ):
		if nodeExpressions[ parentsOfLines[i] ].parent1Index != -1 and nodeExpressions[ parentsOfLines[i] ].parent2Index != -1 :
			printOneLine( nodeExpressions[ parentsOfLines[i] ] )	
		i += 1

def sortParentListAndFilter():
 
 	global parentsOfLines
 	parentsOfLines.sort()
 	 
 	parentsOfLines = list(set( parentsOfLines ))
 	
	return

def mainProcess():

	global inputFile
	global numTask
	
	
	global numB 
	global	numG 
	global	baseLines 
	global	goalLines 
	global	parentsOfLines  # keeps indexes of lines in resolutions
	global	parsedExpressions  
	global	splittedExpressions 
	global	nodeExpressions 
	global outputFile
	
	
	taskCounter = 0
	
	
	
	
	
	numTask = int (inputFile.readline()) 
	
	while taskCounter < numTask:
		
		start = raw_input()
		
		numB = 0
		numG = 0 
		baseLines = []
		goalLines = []
		parentsOfLines = [] # keeps indexes of lines in resolutions
		parsedExpressions = [] 
		splittedExpressions = []
		nodeExpressions = []
		
		readFile()
		
		
		
		
		for i in range(numB + numG): 
			parsedExpressions.append( splitClausesToExpr( baseLines[i] ) )
		### LISTED EXPRESSIONS
		splittedExpressions = []
		for line in parsedExpressions:
			oneLine = []
			for expr in line:
				oneLine.append( parseExprToList(expr) )	 
			splittedExpressions.append(oneLine)

		i = 0
		while i < len(splittedExpressions):
			r1 = Resolver()
			r1.parent1 = []
			r1.parent2 = []
			r1.result = splittedExpressions[i]
			nodeExpressions.append(r1)
			i += 1
	
		resultOfResolution = resolveAllLines()
		if resultOfResolution == True:
			outputFile.write("yes\n")
			#print "yes"
		else:
			#print "no"
			outputFile.write("no\n")
			break	
	

		fillParentIndex()


		parentsOfLines.append( len(nodeExpressions) - 1 )
		fillParentsList( nodeExpressions[-1] )
	

	
		sortParentListAndFilter()
	

		printParentsList() 
		
		taskCounter += 1


	
	return	

def resolver():

	global splittedExpressions
	
	i = 0
	while i < len(splittedExpressions):
		k = 0
		while k < len(splittedExpressions[i]):
			cExpr1 = copy.deepcopy(splittedExpressions[i][k])
			j = i + 1
			
			while j < len(splittedExpressions):
				
				l = 0
				while l < len(splittedExpressions[j]):
				
					cExpr2 = copy.deepcopy( splittedExpressions[j][l] )
					# CHECK FOR UNIFY
					if cExpr1[0][0] != '~' and cExpr2[0][0] == '~':
						
						print "SECOND is ~"
						print "1: ", cExpr1
						print "2: ", cExpr2
						cExpr2[0] = cExpr2[0][1]
						print "2: ", cExpr2
						funcs1 = findFunctions( cExpr1 )
						funcs2 = findFunctions( cExpr2 )
						print "F1: ", funcs1
						print "F2: ", funcs2
						result = unifyAlgorithm( cExpr1, cExpr2, funcs1, funcs2 )
						cExpr2[0] = '~' + cExpr2[0] 
						print "2: ", cExpr2
						print "Result: ", result
						if type(result) == list and result != False and len(result) != 0:
							for exp11 in splittedExpressions[i]:
								print exp11 ,
							print "$",
							
							for exp22 in splittedExpressions[j]:
								print exp22 ,
							print "$",
							
							i1 = 0
							isEmpty = True
							addedLine = []
							while i1 < len(splittedExpressions[i]):
								if i1 != i:
									isEmpty = False
									cExp11 = copy.deepcopy( splittedExpressions[i][i1] )
									e11 = applyUnify( result, cExp11 )
									e111 = copy.deepcopy(e11)
									addedLine.append(e11)
									#splittedExpressions.append( [e11] )
									print e11, 
								i1 += 1
							j1 = 0
							while j1 < len(splittedExpressions[j]):
								if j1 != j:
									isEmpty = False
									cExp22 = copy.deepcopy( splittedExpressions[j][j1] )
									e22 = applyUnify( result, cExp22 )
									e222 = copy.deepcopy(e22)
									addedLine.append(e222)
									#splittedExpressions.append( [e22] )
									print e22,
								j1 += 1	
							if isEmpty:
								print "empty_clause"
							else:
								splittedExpressions.append(addedLine)
								print ""		
						break # DEL						
					elif cExpr1[0][0] == '~' and cExpr2[0][0] != '~':
						print "FIRST is ~"
						print "1: ", cExpr1
						print "2: ", cExpr2 
						cExpr1[0] = cExpr1[0][1]
						print "1: ", cExpr1
						funcs1 = findFunctions( cExpr1 )
						funcs2 = findFunctions( cExpr2 )
						print "F1: ", funcs1
						print "F2: ", funcs2
						result = unifyAlgorithm( cExpr1, cExpr2, funcs1, funcs2 )
						print "R: ", result
						cExpr1[0] = '~' + cExpr1[0]
						
						if type(result) == list and result != False and len(result) != 0:
							for exp11 in splittedExpressions[i]:
								print exp11 ,
							print "$" ,
							
							for exp22 in splittedExpressions[j]:
								print exp22 ,
							print "$" , 
							
							i1 = 0
							isEmpty = True
							addedLine1 = []
							while i1 < len(splittedExpressions[i]):
								if i1 != i:
									isEmpty = False
									cExp11 = copy.deepcopy( splittedExpressions[i][i1] )
									e11 = applyUnify( result, cExp11 )
									e111 = copy.deepcopy(e11)
									addedLine1.append( e111 )
									#splittedExpressions.append( [e11] )
									print e11, 
								i1 += 1
							#print "\n"
							
							j1 = 0
							while j1 < len(splittedExpressions[j]):
								if j1 != j:
									isEmpty = False
									cExp22 = copy.deepcopy( splittedExpressions[j][j1] )
									e22 = applyUnify( result, cExp22 )
									e222 = copy.deepcopy(e22)
									addedLine1.append( e222 )
									#splittedExpressions.append( [e22] )
									print e22,
								j1 += 1	
								
							if isEmpty: 
								print "empty_clause"
							else:
								splittedExpressions.append( addedLine1 )
								print ""	
					
						break #DEL
					l += 1		
				j += 1
			k += 1
	
		i += 1


	

mainProcess()
inputFile.close()
outputFile.close()
'''
print splitExpressions( baseLines[0] )
print splitExpressions( baseLines[1] )
print splitExpressions( baseLines[2] )
'''
