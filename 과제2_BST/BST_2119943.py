from pathlib import Path # 상대경로 지정

class Node: #BST의 Node
    def __init__(self, newItem, left, right):
        self.item = newItem #Key 값
        self.left = left    #왼쪽
        self.right = right  #오른쪽

class BinarySearchTree:
    def __init__(self):
        self.__root = None

    def insert(self, newItem):
        self.__root = self.__insertItem(self.__root, newItem)

    def __insertItem(self, bNode, newItem):
        if (bNode == None):
            bNode = Node(newItem, None, None)
        elif (newItem == bNode.item):
            return None
        elif (newItem < bNode.item):
            bNode.left = self.__insertItem(bNode.left, newItem)
        else:
            bNode.right = self.__insertItem(bNode.right, newItem)
        return bNode
    
    def search(self, key):
        self.searchResult = ['R']
        return self.__searchItem(self.__root, key)


    def __searchItem(self, bNode, key):
        if bNode is None:
            return None
        
        if (key == bNode.item):
            return self.searchResult
        elif (key < bNode.item):
            self.searchResult.append('0')
            return self.__searchItem(bNode.left, key)
        else:
            self.searchResult.append('1')
            return self.__searchItem(bNode.right, key)
            
    def delete(self, key):
        self.__root = self.__deleteItem(self.__root, key)
    
    def __deleteItem(self, bNode, key):
        if bNode is None:  # bNode가 None이면 더 이상 진행할 수 없습니다.
            return None
        if (key == bNode.item):
            bNode = self.__deleteNode(bNode)
        elif (key < bNode.item):
            bNode.left = self.__deleteItem(bNode.left, key)
        else:
            bNode.right = self.__deleteItem(bNode.right, key)
        return bNode
    
    def __deleteNode(self, bNode):
        if (bNode.left == None and bNode.right == None):
            return None
        elif (bNode.left == None):
            return bNode.right
        elif (bNode.right == None):
            return bNode.left
        else:
            (rItem, rNode) = self.__deleteMinItem(bNode.right)
            bNode.item = rItem
            bNode.right = rNode
            return bNode
        
    def __deleteMinItem(self, bNode):
        if (bNode.left == None):
            return (bNode.item, bNode.right)
        else:
            (rItem, rNode) = self.__deleteMinItem(bNode.left)
            bNode.left = rNode

            return (rItem, bNode)
        

input_path = Path(__file__).parent / 'bst_input.txt'
output_path = Path(__file__).parent / 'bst_output.txt'

# input File & output File
input_r = open(input_path, 'r')
output_w = open(output_path, 'w')

#Test Case 갯수
test_case = int(input_r.readline())

test_case_values_amount = 0
test_case_values = []
test_case_search = []

for i in range(test_case):
        test = BinarySearchTree()
        #첫번째 insert
        test_case_values_amount = int(input_r.readline())
        test_case_values = list(map(int, input_r.readline().strip().split()))
        for value in test_case_values:
            test.insert(value)

        #초기화
        test_case_values = []
        
        #두번째 search
        test_case_values_amount = int(input_r.readline())
        test_case_values = list(map(int, input_r.readline().strip().split()))
        for value in test_case_values:
            test_case_search.append(test.search(value))

        #초기화
        test_case_values = []

        #세번째 delete
        test_case_values_amount = int(input_r.readline())
        test_case_values = list(map(int, input_r.readline().strip().split()))
        for value in test_case_values:
            test.delete(value)
            
        
        #초기화
        test_case_values = []
        
        #네번째 search
        test_case_values_amount = int(input_r.readline())
        test_case_values = list(map(int, input_r.readline().strip().split()))
        for value in test_case_values:
            test_case_search.append(test.search(value))
        
        test_case_values = []

        #out_w파일에 쓰기
        for a in test_case_search:
            output_w.write(f"{"".join(map(str, a))}\n")
        
        test_case_search = []

# 파일 닫기
input_r.close()
output_w.close()

