import csv
import random
import time

# Load the problems

problem_list = []

number_of_problems = int(input("Number of problems to test: "))

with open("Data/problems.csv", "r") as csv_file:
    file_contents = csv.reader(csv_file)
    
    for problem in file_contents:
        problem_list.append(problem)

file = open("Data/progress.txt", "r")
start = int(file.read())
file.close()

# random.shuffle(problem_list)
problem_list = problem_list[start:start+number_of_problems]

file = open("Data/progress.txt", "w")
file.write(str(start+number_of_problems))
file.close()

correct = 0
wrong = 0

for problem in problem_list:
    sentence = problem[0]
    options = problem[1:5]
    answer = problem[5]
    answer_idx = options.index(answer) + 1

    print(sentence)
    for i in range(0, 4):
        print((i+1), ". ", options[i])

    response = int(input())
        
    if(response == answer_idx):
        correct += 1
        print("Correct Answer - ", answer_idx, ". ", answer)
    else:
        wrong += 1
        print("Wrong Answer (", response, ")")
        print("Correct Answer is: ", answer_idx, ". ", answer)
    
    print()

print("Correct: ", correct)
print("Wrong: ", wrong)
    
time.sleep(180)