from pathlib import Path # 상대경로 지정

class Eachcase:
    
    Buffer_size = 5  # 버퍼 크기 = 5
    buffer = [None for _ in range(Buffer_size)]
    freeze = [None for _ in range(Buffer_size)]
    run_count = 1
    last_popped = 0

    
    def __init__(self, case_size, case_values):  # case의 크기와 값이 담긴 리스트를 받음
        self.case_size = case_size
        self.case_values = list(map(int, case_values))  # 문자열을 정수로 변환
        self.sorted_runs = []  # 2차원 배열로 결과를 저장
        self.run = []


    def update_freeze_flag(self, newNum, newidx):
        if (newNum is None): # None일 경우 False
            self.freeze[newidx] = False
            return
        self.freeze[newidx] = newNum >= self.last_popped  # 새로운 값이 그전에 pop한 값보다 크거나 같을 경우 True, 작을 경우 False

        

    def find_min_idex(self):
        min_index = None
        min_value = 100  # 가장 큰 값
        for i in range(len(self.buffer)):
            if self.buffer[i] is not None and self.freeze[i] is not False and self.buffer[i] < min_value:
                min_index = i
                min_value = self.buffer[i]
        return min_index

    def pop_min_values(self):
        while True:
            if any(self.freeze):  # True가 하나라도 있으면
                min_index = self.find_min_idex()
                self.run.append(self.buffer[min_index]) #버퍼에 있는 Flase가 아닌 최솟값 run파일에 append
                self.last_popped = self.buffer[min_index] #last_popped 업데이트
                self.buffer[min_index] = None #버퍼 비우기
                self.freeze[min_index] = False #freeze 값 업데이트 (None일 때도 False)

                if self.case_values:  # case_values에 숫자가 남아 있는 경우
                    self.buffer[min_index] = self.case_values.pop(0)  # 새로운 숫자 업데이트
                    self.update_freeze_flag(self.buffer[min_index], min_index)  # 새로운 숫자 freeze 업데이트

            else:
                if any(x is not None for x in self.buffer):  # 버퍼에 숫자가 남아있는 경우(전부 freeze됨)
                    self.sorted_runs.append(self.run.copy())  # run의 복사본을 sorted_runs에 추가 (2차원 배열)
                    self.last_popped = 0  # last_popped 초기화
                    for i in range(len(self.freeze)):  # freeze 초기화
                        self.update_freeze_flag(self.buffer[i], i)
                    self.run = []  # run 초기화
                    self.run_count += 1

                else:  # 버퍼에 숫자가 없는 경우
                    self.sorted_runs.append(self.run.copy())  # run의 복사본을 sorted_runs에 추가 (2차원 배열)
                    return self.sorted_runs

    def makebuffer(self):
        for i in range(self.Buffer_size): 
            if i < self.case_size: # case_size가 Buffer_size보다 클 경우 freeze = True
                self.buffer[i] = self.case_values.pop(0) # 버퍼에 순서대로 값 입력
                self.freeze[i] = True
            else: # case_size가 Buffer_size보다 작을 경우 freeze = False
                self.buffer[i] = None 
                self.freeze[i] = False
            
input_path = Path(__file__).parent / 'replacement_input.txt'
output_path = Path(__file__).parent / 'replacement_output.txt'
# input File & output File
input_r = open(input_path, 'r')
output_w = open(output_path, 'w')

# 첫 번째 줄 = Test Case의 개수
each_case = int(input_r.readline())

# each_case의 개수 길이의 리스트 만들기
each_case_size = []  # 각 Case의 길이 저장
each_case_values = []  # 각 Case의 값 리스트 저장

for i in range(each_case):
    # Replacement Selection을 사용하여 정렬할 값의 개수 n (1 <= n <= 100)
    each_case_size.append(int(input_r.readline()))
    # Replacement Selection을 사용하여 정렬할 space로 구분된 길이 n인 정수의 순열(0 <= 정수 <= 100)
    each_case_values.append(input_r.readline().strip().split())


# 각 테스트 케이스에 대해 each_case 객체를 생성
for i in range(each_case):
    case = Eachcase(each_case_size[i], each_case_values[i])  # 올바르게 리스트를 전달
    case.makebuffer()  # 버퍼를 생성
    case.pop_min_values()  # min 값을 pop
    output_w.write(f"{case.run_count}\n")
    for a in case.sorted_runs:
         output_w.write(f"{" ".join(map(str, a))}\n") # sorted_runs의 내용을 출력


# 파일 닫기
input_r.close()
output_w.close()

