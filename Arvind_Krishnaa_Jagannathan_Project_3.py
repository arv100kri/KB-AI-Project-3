'''
Created on 24-Oct-2012

@author: koolkid
'''
from Source.com.miller.utils.AnalogySolverHelper import Solver

answers = []
numberOfProblems = 8
for i in range(1,(numberOfProblems+1)):
    answer = Solver(i).solveProblem()
    print "Answer to the problem ", i," is ", str(answer)
    answers.append(answer)

print "------------Summary--------------------"
for i in range(0, numberOfProblems):
    print "Solution for Problem(",str(i+1),") is ", answers[i]
print "----------------------------------------"
