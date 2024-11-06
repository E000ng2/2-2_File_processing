from pathlib import Path # 상대경로 지정

class TestCase:
    
    Buffer_size = 5  # 버퍼 크기 = 5
    
    def __init__(self, caseSize, caseList):  # case의 크기와 값이 담긴 리스트를 받음
        self.caseSize = caseSize
        self.caseList = list(map(int, caseList))  # 문자열을 정수로 변환
        self.Buffer = [None for _ in range(self.Buffer_size)]
        self.Freeze = [None for _ in range(self.Buffer_size)]
        self.RunFile = []  # 2차원 배열로 결과를 저장
        self.Run = []
        self.RunNum = 1
        self.popNum = 0

    def freeze(self, newNum, newidx):
        if (newNum is None): # None일 경우 False
            self.Freeze[newidx] = False
            return
        self.Freeze[newidx] = newNum >= self.popNum  # 새로운 값이 그전에 pop한 값보다 크거나 같을 경우 True, 작경우 False

        

    def findminidx(self):
        minidx = None
        min_value = 100  # 가장 큰 값
        for i in range(len(self.Buffer)):
            if self.Buffer[i] is not None and self.Freeze[i] is not False and self.Buffer[i] < min_value:
                minidx = i
                min_value = self.Buffer[i]
        return minidx

    def popmin(self):
        while True:
            if any(self.Freeze):  # True가 하나라도 있으면
                minidx = self.findminidx()
                self.Run.append(self.Buffer[minidx]) #버퍼에 있는 Flase가 아닌 최솟값 Run파일에 append
                self.popNum = self.Buffer[minidx] #popNum 업데이트
                self.Buffer[minidx] = None #버퍼 비우기
                self.Freeze[minidx] = False #Freeze 값 업데이트 (None일 때도 False)

                if self.caseList:  # caseList에 숫자가 남아 있는 경우
                    self.Buffer[minidx] = self.caseList.pop(0)  # 새로운 숫자 업데이트
                    self.freeze(self.Buffer[minidx], minidx)  # 새로운 숫자 freeze 업데이트

            else:
                if any(x is not None for x in self.Buffer):  # 버퍼에 숫자가 남아있는 경우(전부 freeze됨)
                    self.RunFile.append(self.Run.copy())  # Run의 복사본을 RunFile에 추가 (2차원 배열)
                    self.popNum = 0  # popNum 초기화
                    for i in range(len(self.Freeze)):  # Freeze 초기화
                        self.freeze(self.Buffer[i], i)
                    self.Run = []  # Run 초기화
                    self.RunNum += 1

                else:  # 버퍼에 숫자가 없는 경우
                    self.RunFile.append(self.Run.copy())  # Run의 복사본을 RunFile에 추가 (2차원 배열)
                    return self.RunFile

    def makeBuffer(self):
        for i in range(self.Buffer_size): 
            if i < self.caseSize: # caseSize가 Buffer_size보다 클 경우 Freeze = True
                self.Buffer[i] = self.caseList.pop(0) # 버퍼에 순서대로 값 입력
                self.Freeze[i] = True
            else: # caseSize가 Buffer_size보다 작을 경우 Freeze = False
                self.Buffer[i] = None 
                self.Freeze[i] = False
            
input_path = Path(__file__).parent / 'replacement_input.txt'
output_path = Path(__file__).parent / 'replacement_output.txt'
# input File & output File
input_r = open(input_path, 'r')
output_w = open(output_path, 'w')

# 첫 번째 줄 = Test Case의 개수
testCase = int(input_r.readline())

# testCase의 개수 길이의 리스트 만들기
testCaseSize = []  # 각 Case의 길이 저장
testCaseNumList = []  # 각 Case의 값 리스트 저장

for i in range(testCase):
    # Replacement Selection을 사용하여 정렬할 값의 개수 n (1 <= n <= 100)
    testCaseSize.append(int(input_r.readline()))
    # Replacement Selection을 사용하여 정렬할 space로 구분된 길이 n인 정수의 순열(0 <= 정수 <= 100)
    testCaseNumList.append(input_r.readline().strip().split())


# 각 테스트 케이스에 대해 TestCase 객체를 생성
for i in range(testCase):
    case = TestCase(testCaseSize[i], testCaseNumList[i])  # 올바르게 리스트를 전달
    case.makeBuffer()  # 버퍼를 생성
    case.popmin()  # min 값을 pop
    output_w.write(f"{case.RunNum}\n")
    for a in case.RunFile:
         output_w.write(f"{" ".join(map(str, a))}\n") # RunFile의 내용을 출력


# 파일 닫기
input_r.close()
output_w.close()

