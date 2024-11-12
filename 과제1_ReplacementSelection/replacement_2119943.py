from pathlib import Path  # 상대경로 지정

class TestCase:
    
    BUFFER_SIZE = 5  # 버퍼 크기 = 5
    buffer = [None for _ in range(BUFFER_SIZE)]
    freeze_flags = [None for _ in range(BUFFER_SIZE)]
    sorted_runs = []  # 2차원 배열로 결과를 저장
    current_run = []
    run_count = 1
    last_popped = 0
    
    def __init__(self, case_size, case_values):  # case의 크기와 값이 담긴 리스트를 받음
        self.case_size = case_size
        self.case_values = list(map(int, case_values))  # 문자열을 정수로 변환
        
    def update_freeze_flag(self, new_num, index):
        if new_num is None:  # None일 경우 True
            self.freeze_flags[index] = True
            return
        # 새로운 값이 last_popped보다 크거나 같으면 Fasle, 작으면 True
        self.freeze_flags[index] = not new_num >= self.last_popped

    def find_min_index(self):
        min_index = None
        min_value = 100  # 가장 큰 값으로 초기화
        for i in range(len(self.buffer)):
            if self.buffer[i] is not None and not self.freeze_flags[i] and self.buffer[i] < min_value:
                min_index = i
                min_value = self.buffer[i]
        return min_index

    def pop_min_values(self):
        while True:
            if any(self.freeze_flags):  # 하나라도 False가 있으면 실행
                min_index = self.find_min_index()
                if min_index is not None:
                    self.current_run.append(self.buffer[min_index])  # 버퍼의 최소값을 current_run에 추가
                    self.last_popped = self.buffer[min_index]  # last_popped 업데이트
                    self.buffer[min_index] = None  # 버퍼에서 pop된 값 삭제
                    self.freeze_flags[min_index] = True # freeze_flags 값 업데이트 (None일 때도 True)

                    # case_values에 값이 남아 있는 경우 Buffer와 Freeze에 새 값 추가
                    if self.case_values:
                        self.buffer[min_index] = self.case_values.pop(0)
                        self.update_freeze_flag(self.buffer[min_index], min_index)

            else:
                # 버퍼에 숫자가 남아 있는 경우(모두 freeze됨)
                if any(x is not None for x in self.buffer):
                    self.sorted_runs.append(self.current_run.copy())  # current_run 복사본을 sorted_runs에 추가
                    self.last_popped = 0  # last_popped 초기화
                    for i in range(len(self.freeze_flags)):
                        self.update_freeze_flag(self.buffer[i], i)
                    self.current_run = []  # current_run 초기화
                    self.run_count += 1

                else:  # 버퍼에 숫자가 남아 있지 않은 경우
                    self.sorted_runs.append(self.current_run.copy())  # 마지막 current_run을 sorted_runs에 추가
                    return self.sorted_runs

    def initialize_buffer(self):
        for i in range(self.BUFFER_SIZE):
            if i < self.case_size:  # case_size가 BUFFER_SIZE보다 클 경우 freeze_flags = False
                self.buffer[i] = self.case_values.pop(0)  # 버퍼에 순서대로 값 입력
                self.freeze_flags[i] = False
            else:  # case_size가 BUFFER_SIZE보다 작을 경우 freeze_flags = True
                self.buffer[i] = None
                self.freeze_flags[i] = True
            

# 파일 경로 설정
input_path = Path(__file__).parent / 'replacement_input.txt'
output_path = Path(__file__).parent / 'replacement_output.txt'

# input File & output File
input_r = open(input_path, 'r')
output_w = open(output_path, 'w')

# 첫 번째 줄 = Test Case의 개수
test_case_count = int(input_r.readline())

# 테스트 케이스 정보를 담을 리스트
test_case_sizes = []  # 각 Case의 길이 저장
test_case_values = []  # 각 Case의 값 리스트 저장

# 입력 파일에서 테스트 케이스 읽기
for i in range(test_case_count):
    test_case_sizes.append(int(input_r.readline()))
    test_case_values.append(input_r.readline().strip().split())

# 각 테스트 케이스에 대해 TestCase 객체를 생성하고 결과 작성
for i in range(test_case_count):
    case = TestCase(test_case_sizes[i], test_case_values[i])
    case.initialize_buffer()  # 버퍼 생성
    case.pop_min_values()  # 최소값 pop

    # 출력 파일에 run_count와 sorted_runs 내용을 작성
    output_w.write(f"{case.run_count}\n")
    for run in case.sorted_runs:
        output_w.write(" ".join(map(str, run)) + "\n")  # sorted_runs의 내용을 출력

# 파일 닫기
input_r.close()
output_w.close()
