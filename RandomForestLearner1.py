import numpy as np
import random

class Node:
	'''
	Node on the tree
	'''
	def __init__(self):
		self.Feature = None # feature number, -1 means leaf
		self.SplitVal = None # split value or leaf value 
		self.LNode = None # pointer of root of left tree
		self.RNode = None # pointer of root of right tree

class Tree:
	'''
	generate tree
	'''

	def __init__(self, node):
		'''
		constructor
		@rootnode: root node
		'''
		self.root = node
		self.data = None

	def GenTree(self, data):
		'''
		generate the tree
		@data: the training numpy array data for generating tree
		'''
		self.data = data
		self.GenTreeMatrx(self.root, self.data)

	def GenTreeMatrx(self, root, data):
		'''
		generate the matrix to store the information of tree
		@root: rootnode
		@data: numpy array data for generate the matrix
		'''
		
		LNode = list()
		RNode = list()
		FeatureVal = random.randint(0, np.array(data).shape[1] - 2)

		root.Feature = FeatureVal
		#print FeatureVal

		# The leaf
		if len(data) == 1:
			root.SplitVal = np.array(data)[0][-1]
			root.Feature = -1
			return

		x1 = random.randint(0, len(data) - 1)
		x2 = random.randint(0, len(data) - 1)
		while x1 == x2:
			x2 = random.randint(0, len(data) - 1)
		#print x1, x2

		#print data[x1][FeatureVal]
		
		Split_Val = (np.array(data)[x1][FeatureVal] + np.array(data)[x2][FeatureVal]) / 2.0
		#print Split_Val
		root.SplitVal = Split_Val
		

		for i in range(len(data)):
			if data[i][FeatureVal] <= Split_Val:
				LNode.append(data[i])
			else:
				RNode.append(data[i])

		if len(LNode) > 0:
			root.LNode = Node()
			self.GenTreeMatrx(root.LNode, LNode)

		if len(RNode) > 0:
			root.RNode = Node()
			self.GenTreeMatrx(root.RNode, RNode)

		if len(LNode) == 0 and len(RNode) == 0:
			root.SplitVal = np.sum(np.array(data[:, -1])) / len(data)
			root.Feature = -1
			
		return

	def regressor(self, test, node):
		if node.Feature == -1:
			return node.SplitVal
		if test[node.Feature] <= node.SplitVal:
			return self.regressor(test, node.LNode)
		else:
			return self.regressor(test, node.RNode)

	def print_tree(self, node):
		print node.SplitVal
		self.print_tree(node.LNode)
		self.print_tree(node.RNode)

	
class RandomForestLearner:
	'''
	Random Forest for construct decision tree
	'''

	def __init__(self, k):
		'''
		constructor
		@k: the number of trees in forest
		'''
		self.k = k;
		self.data = None
		self.trees = list()

	def addEvidence(self, Xdata, Ydata):
		'''
		add data be trained
		@Xdata: the feature values colunms
		@Ydata: the prediction values from Xdata 
		'''
		self.data = None
		self.trees = None
		self.trees = list()
		Xrow_n = Xdata.shape[0]
		Xcol_n = Xdata.shape[1]
		Yrow_n = Ydata.shape[0]
		if Yrow_n != Xrow_n:
			print " numbers of X data and Y data are not matching"

		#print Xdata

		data = np.zeros([Xrow_n, Xcol_n+1])
		data[:, 0:Xcol_n] = Xdata
		data[:, Xcol_n] = Ydata[:, 0]
		
		self.data = data


		#pick random 60% data to generate the tree
		data4tree = np.zeros((int(0.6 * Xrow_n), Xcol_n+1))
		#print data4tree.shape[0]
		for i in range(self.k):
			DTree = Tree(Node())
			temp_data = random.sample(range(0, Xrow_n), int(0.6 * Xrow_n))
			#print len(temp_data)
			#print data4tree[1]
			#print self.data[temp_data[1]]
			for j in range(len(temp_data)):
				data4tree[j] = data[temp_data[j]]
			DTree.GenTree(data4tree)
			self.trees.append(DTree)
	
	def query(self, Xdata):
		'''
		Regression the test data
		@Xdata: test data
		'''
		#the number of rows
		row_n = Xdata.shape[0]
		#the number of columns
		col_n = Xdata.shape[1]
		#change test data type from string to float
		Xlearn = np.zeros([row_n, col_n])
		Xlearn[:, 0:col_n] = Xdata
		
		Ylearn = np.zeros([row_n, 1])

		for i in range(0, row_n):
			tree_val = np.zeros(self.k)
			for res in range(self.k):
				t = self.trees[res]
				tree_val[res] = t.regressor(Xlearn[i], t.root)
				#tree_val[res] = t.Classifier(Xtest[i], t.root, t.xtrain, t.ytrain)
				#Yret[i] = mode(tree_val)[0][0]
				Ylearn[i] = np.mean(tree_val)

		return Ylearn
