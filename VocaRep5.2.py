#! English learning (vocabulary) v.1 by Denys Tantsiura
# alt+3 / alt+4 = comment / uncomment
import os
from random import shuffle

startOne = True
varWords1 = []  # English
varWords2 = []  # Ukainian
varScores1 = []  # num tests
varScores2 = []  # num corect answer
varRemLim = 10


def main():
    print('Welcome to the simple program to vocabulary replenishment of English words...\n')
    SelProgram()


def SelProgram():
    global varRemLim
    global startOne
    startOne = True
# varWords1=[]
# varWords2=[]
# varScores1=[]
# varScores2=[]
    while startOne:
        print('\nMenu: \n    1 - generate last results; \n    2 - continue learning; \n    3 - set reminder limit; \n    4 - exit;\n')
        varAnsware1 = int(input('Enter your choice: '))
        if varAnsware1 == 1:
            FunProg1()
        elif varAnsware1 == 2:
            FunProg2()
        elif varAnsware1 == 3:
            varRemLim = int(
                input('Enter new reminder limit from 1 to 100 (10 is default):\n'))
            if varRemLim < 1 or varRemLim > 100 or not varRemLim or type(varRemLim) != type(10):
                print('Incorrectrd input\n')
                varRemLim = 10
                print('The established limit: ', varRemLim)
        elif varAnsware1 == 4:
            print(' bye. See you next time')  # end() # None # continue # break
            startOne = False
# elif varAnsware1==5:
##            print('Incorrect command entry. Please try again.')
        else:
            print('Incorrect command entry. Please try again.')
# main()


def FunP1_tryOpenFile(varPathFile):
    if os.path.isfile(varPathFile):
        None
    else:
        print('Unable to find ', varPathFile, ' file')
        print('Free-fill file will be created')
        varAnsAFile = open(varPathFile, 'w', encoding="utf-8")
        varAnsAFile.close()


def FunExpansion(len_varWords, varScores1, varScores2):
    count = len_varWords-len(varScores1)
    while count > 0:
        varScores1.append(int(0))
        varScores2.append(int(0))
        count -= 1


def FunProg1(varCorrected=True):
    if varCorrected:
        print('Ok, let`s do it now:\n')
    FunP1_tryOpenFile('EnWords.txt')
    varWordsFile = open('EnWords.txt', encoding="utf-8")
    global varWords1
    global varWords2
#    varWords1=[]
    varWords1.clear()
#    varWords2=[]
    varWords2.clear()
    for i in varWordsFile:
        if len(i) > 2:
            varLineWordsFile = str(i)
            varLineWordsFile = varLineWordsFile.rstrip()  # remove '\n' in line
            varLineWordsFile = varLineWordsFile.split(' - ')
            varWords1.append(varLineWordsFile[0])
            varWords2.append(varLineWordsFile[1])
    varWordsFile.close()
    #############################################################################################
    FunP1_tryOpenFile('EnWScores.txt')
    varScoresFile = open('EnWScores.txt', encoding="utf-8")
    global varScores1
    global varScores2
#    varScores1=[]
    varScores1.clear()
#    varScores2=[]
    varScores2.clear()
    for i in varScoresFile:
        varLineScoresFile = str(i)
        if len(varLineScoresFile) > 1:
            varLineScoresFile = varLineScoresFile.rstrip()  # remove '\n' in line
            varScores1.append(int(varLineScoresFile.split()[0]))
            varScores2.append(int(varLineScoresFile.split()[1]))
    varScoresFile.close()
    FunExpansion(len(varWords1), varScores1, varScores2)
    if varCorrected:
        varResultFile = open('Summary result.txt', 'w', encoding="utf-8")
        varLastRezults = []
        var_iCount = 0
        for i in varWords1:
            varLastRezults.append((str(i)+' - '+str(varWords2[var_iCount])+' =attempts: '+str(
                varScores1[var_iCount])+', successfully: '+str(varScores2[var_iCount])))
            varResultFile.write(varLastRezults[var_iCount]+'\n')
            var_iCount += 1
        varResultFile.close()
        print('file "Summary result.txt" generated successfully')


def FunRandomSortDic(varWords1, varWords2, varScores1, varScores2):
    varMaxCountWords = int(len(varWords1))  # varMaxCountWords=len(varScores1)
    varShuffleDict = [[i for i in range(0, len(varWords2))], [i for i in range(0, len(varWords2))], [
        i for i in range(0, len(varWords2))], [i for i in range(0, len(varWords2))]]
    varShuffleDict = list(map(list, zip(*varShuffleDict)))  # transpon
    #print("E1: ",varShuffleDict)#################
    varCountSum = 0
    while varCountSum < varMaxCountWords:
        varShuffleDict[varCountSum][0] = varWords1[varCountSum]
        varShuffleDict[varCountSum][1] = varWords2[varCountSum]
        varShuffleDict[varCountSum][2] = varScores1[varCountSum]
        varShuffleDict[varCountSum][3] = varScores2[varCountSum]
        varCountSum += 1
    varShuffleWords1 = varWords1.copy()
    shuffle(varShuffleWords1)
    shuffle(varShuffleWords1)
# shuffle(varShuffleWords1)
# shuffle(varShuffleWords1)
    # count=0
    # print(varMaxCountWords)
    varMaxCountWords
    for i in range(varMaxCountWords):
        varNextSA = int(varWords1.index(varShuffleWords1[i]))
        varShuffleDict[i][0] = varWords1[varNextSA]
        varShuffleDict[i][1] = varWords2[varNextSA]
        varShuffleDict[i][2] = varScores1[varNextSA]
        varShuffleDict[i][3] = varScores2[varNextSA]
    # print(varShuffleDict)
    return varShuffleDict


def miniFunFixLocalRez(vAns, varF=False):
    varFindForeRezFix = int(varWords1.index(vAns))
    if varF:
        varScores2[varFindForeRezFix] += 1
    else:
        varScores1[varFindForeRezFix] += 1
    #print(varFindForeRezFix)#############################################################################


def FuncTEST1(varScores1, varScores2, varLineNow):  # inProgress
    global varRemLim
    varMaxCountWords = len(varScores1)
    varC = 0
    for i in range(varMaxCountWords):
        # !not i - int(varWords1.index(vAns)) varLineNow[i][0]  if varScores2[i]<=varRemLim:
        if varLineNow[i][3] <= varRemLim:
            print('\n', varLineNow[i][1], ':')
            uAns = input()
            if uAns == '3' or uAns == 'exit' or uAns == 'end':
                break
            elif uAns == varLineNow[i][0]:
                varLineNow[i][3] += 1
                # varScores2!!!!!!!!!!!!!!!!!!!right
                miniFunFixLocalRez(uAns, True)
            else:
                varMemFix = 0
                while varMemFix != 1:
                    print('incorrect!, correct:\n', varLineNow[i][0], '\n')
                    print('Try!:\n')
                    uAns = input()
                    if uAns == varLineNow[i][0]:
                        print('Ok\n')
                        varMemFix = 1
                    if uAns == '3' or uAns == 'exit' or uAns == 'end':
                        print('I see it`s hard for you...\n')
                        varMemFix = 1
            varLineNow[i][2] += 1
            # varScores2[][]+=1#varScores1!!!!!!!!!!!!!!!!!!!!!!!wrong
            miniFunFixLocalRez(varLineNow[i][0])
        else:
            varC += 1  # continue
    if varC == varMaxCountWords:
        print('Oh so you all know...')
    return varScores1, varScores2


def FunProg2():
    global varWords1
    global varWords2
    global varScores1
    global varScores2
    print('Let`s start the our lesson:\n')
    if not varWords1:
        FunProg1(False)
    if len(varWords1) > len(varScores1):
        FunProg1(False)
##    varLineNow=[[i for i in range(0,len(varWords2))],[i for i in range(0,len(varWords2))],[i for i in range(0,len(varWords2))],[i for i in range(0,len(varWords2))]]
# varLineNow=list(map(list, zip(*varLineNow)))#transpon!!!?????????????????????????????????????????????????
    #################################################################################
    # shuffle dict###########################################################################
    varLineNow = FunRandomSortDic(varWords1, varWords2, varScores1, varScores2)
    FuncTEST1(varScores1, varScores2, varLineNow)  # !!!!!
    #################################################################################
    varSaveProgress = open('EnWScores.txt', 'w', encoding="utf-8")
    var_iCount = 0
    for i in varScores1:
        varSaveProgress.write(
            str(varScores1[var_iCount])+' '+str(varScores2[var_iCount])+'\n')
        var_iCount += 1
    varSaveProgress.close()


if __name__ == "__main__":
    main()
