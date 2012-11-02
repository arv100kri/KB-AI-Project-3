'''
Created on 24-Oct-2012

@author: koolkid
'''
from Source.com.miller.utils.FileReader import FileDirectory
from Source.com.miller.utils.Math import SimpleMathUtils
from Source.com.miller.utils.Transform import SimpleTransforms
from PIL import Image
import math
import numpy

class Solver(object):
    '''
    Given a single problem this class finds the solution to it by applying the algorithm
    '''
    __dimensions = 0
    __problem = 0
    
    __BASEURL = "Representations"
    __REFERENCE = "/Reference"
    __FRAME = "/Frame"
    __FORMAT= ".jpg"
    __PROBLEM = "/"
    
    def __init__(self, problem_number):
        self.__dimensions = FileDirectory(problem_number).getDimensions()
        self.__problem = problem_number
        
    def getTransform(self, image1, image2):
        diff = 200
        Transform = None
        selfCorelationValue = SimpleMathUtils.selfCorrelation(image2)
        #Checking Identity
        identityArray = SimpleTransforms.identity(image1)
        crossCorelationForIdentity = SimpleMathUtils.corelationImage1Image2(identityArray, image2)
        newdiff = math.fabs(crossCorelationForIdentity - selfCorelationValue)
        if newdiff < diff:
            diff = newdiff
            Transform = SimpleTransforms.IDENTITY
        
        #checking reflection
        reflectionArray = SimpleTransforms.reflection(image1)
        crossCorelationForReflection = SimpleMathUtils.corelationImage1Image2(reflectionArray, image2)
        newdiff = math.fabs(crossCorelationForReflection - selfCorelationValue)
        if newdiff < diff:
            diff = newdiff
            Transform = SimpleTransforms.REFLECTION
            
        #checking flip
        flipArray = SimpleTransforms.flip(image1)
        crossCorelationForFlip = SimpleMathUtils.corelationImage1Image2(flipArray, image2)
        newdiff = math.fabs(crossCorelationForFlip - selfCorelationValue)
        if newdiff < diff:
            diff = newdiff
            Transform = SimpleTransforms.FLIP
            
        #checking rotation90
        rotation90Array = SimpleTransforms.rotation90(image1)
        crossCorelationForRotation90 = SimpleMathUtils.corelationImage1Image2(rotation90Array, image2)
        newdiff = math.fabs(crossCorelationForRotation90 - selfCorelationValue)
        if newdiff < diff:
            diff = newdiff
            Transform = SimpleTransforms.ROTATION90
        
        #checking rotation180
        rotation180Array = SimpleTransforms.rotation180(image1)
        crossCorelationForRotation180 = SimpleMathUtils.corelationImage1Image2(rotation180Array, image2)
        newdiff = math.fabs(crossCorelationForRotation180 - selfCorelationValue)
        if newdiff < diff:
            diff = newdiff
            Transform = SimpleTransforms.ROTATION180
            
        #checking rotation270
        rotation270Array = SimpleTransforms.rotation270(image1)
        crossCorelationForRotation270 = SimpleMathUtils.corelationImage1Image2(rotation270Array, image2)
        newdiff = math.fabs(crossCorelationForRotation270 - selfCorelationValue)
        if newdiff < diff:
            diff = newdiff
            Transform = SimpleTransforms.ROTATION270
        
        return Transform
    
    def solveProblem(self):
        if self.__dimensions == 0:
            return None
        
        elif self.__dimensions == 2:
            image1_1 = self.__BASEURL+self.__PROBLEM+str(self.__problem)+self.__REFERENCE+self.__FRAME+"1-1"+self.__FORMAT
            image1_1 = Image.open(image1_1)
            
            image1_2 = self.__BASEURL+self.__PROBLEM+str(self.__problem)+self.__REFERENCE+self.__FRAME+"1-2"+self.__FORMAT
            image1_2 = Image.open(image1_2)
            
            image2_1 = self.__BASEURL+self.__PROBLEM+str(self.__problem)+self.__REFERENCE+self.__FRAME+"2-1"+self.__FORMAT
            image2_1 = Image.open(image2_1)
            
            transform = self.getTransform(image1_1, image1_2)
            answerPath = self.__BASEURL+self.__PROBLEM+str(self.__problem)
            print "Examining the answer choices from the path: ", answerPath
            numberOfAnswerChoices = FileDirectory(self.__problem)
            numberOfAnswerChoices.setPath(answerPath)
            numberOfAnswerChoices = numberOfAnswerChoices.getSizeOfPath()
            
            if transform is not None:
                print "The answer should have the transform: ", transform, "with respect to frame 2-1"
                expected_answer = SimpleTransforms.performTransform(image2_1, transform)
                diff = 200
                Answer = None
                for i in range(1, numberOfAnswerChoices):
                    answerChoiceFileName = answerPath+self.__FRAME+str(i)+self.__FORMAT
                    print "Checking the image ", answerChoiceFileName
                    choice = Image.open(answerChoiceFileName)
                    selfCorelationOfExpectedAnswer = SimpleMathUtils.selfCorrelation(expected_answer)
                    corelationExpectedAnswerWithAnswerChoice = SimpleMathUtils.corelationImage1Image2(choice, expected_answer)
                    newdiff = math.fabs(corelationExpectedAnswerWithAnswerChoice - selfCorelationOfExpectedAnswer)
                    if newdiff < diff:
                        diff = newdiff
                        Answer = i
                
                return Answer
            
            else:
                #Applying ratio 1_1/1_2 : 2_1/ans
                print "Checking for ratio in number of pixels"
                potentialAnswerChoices = []
                ratioArray1 = []
                i1_1 = numpy.asarray(image1_1)
                i1_2 = numpy.asarray(image1_2)
                i2_1 = numpy.asarray(image2_1)
                
                ratioArray1.append(sum(sum(i1_1/i1_2)))
                referenceSum = SimpleMathUtils.findSumArrays(ratioArray1)
                
                for i in range(1, numberOfAnswerChoices):
                    answerChoiceFileName = answerPath+self.__FRAME+str(i)+self.__FORMAT
                    print "Checking the image ", answerChoiceFileName
                    choice = Image.open(answerChoiceFileName)
                    choice = numpy.asarray(choice)
                    ratioArray2 = []
                    ratioArray2.append(sum(sum(i2_1/choice)))
                    choiceSum = SimpleMathUtils.findSumArrays(ratioArray2)
                    if math.fabs(referenceSum - choiceSum) <=30:
                        potentialAnswerChoices.append(i)
                
                if len(potentialAnswerChoices) == 1:
                    return potentialAnswerChoices[0]
                else:
                    diffArray1 = []
                    diffArray1.append(sum(sum(i1_1-i1_2)))
                    referenceSum = SimpleMathUtils.findSumArrays(diffArray1)
                    print "Checking for some approximate match"
                    diff = float('inf')
                    Answer = None
                    if len(potentialAnswerChoices) == 0:    #Consider all the answer choices, else just consider the ones in the potential
                        for j in range(1,numberOfAnswerChoices):
                            potentialAnswerChoices.append(j)
                    for ans in potentialAnswerChoices:
                        answerChoiceFileName = answerPath+self.__FRAME+str(ans)+self.__FORMAT
                        print "Checking the image ", answerChoiceFileName
                        choice = Image.open(answerChoiceFileName)
                        choice = numpy.asarray(choice)
                        diffArray2 = []
                        diffArray2.append(sum(sum(i2_1-choice)))
                        choiceSum = SimpleMathUtils.findSumArrays(diffArray2)
                        newdiff = math.fabs(referenceSum - choiceSum)
                        if newdiff < diff:
                            diff = newdiff
                            Answer = ans
                    return Answer
        
        elif self.__dimensions == 3:
            image1_1 = self.__BASEURL+self.__PROBLEM+str(self.__problem)+self.__REFERENCE+self.__FRAME+"1-1"+self.__FORMAT
            image1_1 = Image.open(image1_1)
            
            image1_2 = self.__BASEURL+self.__PROBLEM+str(self.__problem)+self.__REFERENCE+self.__FRAME+"1-2"+self.__FORMAT
            image1_2 = Image.open(image1_2)
            
            image1_3 = self.__BASEURL+self.__PROBLEM+str(self.__problem)+self.__REFERENCE+self.__FRAME+"1-3"+self.__FORMAT
            image1_3 = Image.open(image1_3)
            
            image3_1 = self.__BASEURL+self.__PROBLEM+str(self.__problem)+self.__REFERENCE+self.__FRAME+"3-1"+self.__FORMAT
            image3_1 = Image.open(image3_1)
            
            image3_2 = self.__BASEURL+self.__PROBLEM+str(self.__problem)+self.__REFERENCE+self.__FRAME+"3-2"+self.__FORMAT
            image3_2 = Image.open(image3_2)
            
            i1_1 = numpy.asarray(image1_1)
            i1_2 = numpy.asarray(image1_2)
            i1_3 = numpy.asarray(image1_3)
            
            i3_1 = numpy.asarray(image3_1)
            i3_2 = numpy.asarray(image3_2)


            diffArray1 = []
            diffArray1.append(sum(sum(i1_2-i1_3)))
            referenceSum = SimpleMathUtils.findSumArrays(diffArray1)
            
            answerPath = self.__BASEURL+self.__PROBLEM+str(self.__problem)
            print "Examining the answer choices from the path: ", answerPath
            numberOfAnswerChoices = FileDirectory(self.__problem)
            numberOfAnswerChoices.setPath(answerPath)
            numberOfAnswerChoices = numberOfAnswerChoices.getSizeOfPath()
            print "Number of choices: ", str(numberOfAnswerChoices)
            diff = 650
            potentialAnswers = []
            print "---------Diff Pixel Stage-------------"
            for i in range(1, numberOfAnswerChoices):
                answerChoiceFileName = answerPath+self.__FRAME+str(i)+self.__FORMAT
                print "Checking the image ", answerChoiceFileName
                choice = Image.open(answerChoiceFileName)
                choice = numpy.asarray(choice)
                diffArray2 = []
                diffArray2.append(sum(sum(i3_2-choice)))
                choiceSum = SimpleMathUtils.findSumArrays(diffArray2)   
                print "Checking for an exact! match"
                if math.fabs(referenceSum - choiceSum) == 0:    #Exact match
                    return i
                print "Checking for a good match"
                if math.fabs(referenceSum - choiceSum) < diff:
                    potentialAnswers.append(i)
            
            if len(potentialAnswers) == 1:
                return potentialAnswers[0]
            else:
                if len(potentialAnswers) == 0:    #Consider all the answer choices, else just consider the ones in the potential
                    for j in range(1,numberOfAnswerChoices):
                        potentialAnswers.append(j)
                ratioArray1 = []
                ratioArray1.append(sum(sum(i1_2/i1_3)))
                referenceSum = SimpleMathUtils.findSumArrays(ratioArray1)
                
                potentialChoices = []
                diff = 50
                print "-------------Ratio Stage------------------"
                for ans in potentialAnswers:
                    answerChoiceFileName = answerPath+self.__FRAME+str(ans)+self.__FORMAT
                    print "Checking the image ", answerChoiceFileName
                    choice = Image.open(answerChoiceFileName)
                    choice = numpy.asarray(choice)
                    ratioArray2 = []
                    ratioArray2.append(sum(sum(i3_2/choice)))
                    choiceSum = SimpleMathUtils.findSumArrays(ratioArray2)
                    print "Checking for an exact! match"
                    if math.fabs(referenceSum - choiceSum) == 0:    #Exact match
                        return ans
                    print "Checking for a good match"
                    if math.fabs(referenceSum - choiceSum) < diff:
                        potentialChoices.append(ans)
                
                if len(potentialChoices) == 1:
                    return potentialChoices[0]
                else:
                    if len(potentialChoices) == 0:
                        for k in range(1, numberOfAnswerChoices):
                            potentialChoices.append(k)
                    properDiffArray1 = []
                    properDiffArray1.append(sum(sum(i1_1-i1_2)))
                    properDiffArray1.append(sum(sum(i1_2-i1_3)))
                    properDiffArray1.append(sum(sum(i1_1-i1_3)))
                    referenceSum = SimpleMathUtils.findSumArrays(properDiffArray1)
                    print "ReferenceSum is ", str(referenceSum)
                    Answer = None
                    diff = float('inf')
                    print "----------Good enough stage-----------"
                    for a in potentialChoices:
                        answerChoiceFileName = answerPath+self.__FRAME+str(a)+self.__FORMAT
                        print "Checking the image ", answerChoiceFileName
                        choice = Image.open(answerChoiceFileName)
                        choice = numpy.asarray(choice)
                        properDiffArray2 = []
                        properDiffArray2.append(sum(sum(i3_1-i3_2)))
                        properDiffArray2.append(sum(sum(i3_2-choice)))
                        properDiffArray2.append(sum(sum(i3_1-choice)))
                        choiceSum = SimpleMathUtils.findSumArrays(properDiffArray2)
                        print "ChoiceSum for ", str(a)," is ", str(choiceSum)
                        newdiff = math.fabs(referenceSum - choiceSum) 
                        print "DIFF: ", diff
                        print "NEWDIFF: ", newdiff
                        if newdiff < diff:
                            diff = newdiff
                            Answer = a 
                    return Answer
        else:
            print "Cannot solve anything other than 2x2 or 3x3"
            return None
