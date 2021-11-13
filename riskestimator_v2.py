import pickle
import copy
import dictsort
from probability import pb, pbx, conditional_pb_rv

MAT = []

# format the output in a visually appealing way. 
def mklen(s, k, c):
    l = len(s);
    return s + ': ' if l >= k else s + ': ' + (k - l) * c + ' '


# obtain the list of possible rows (each representing a failure mode), and combine into a matrix
def get_possible_matrix(mat, phase, error_list):
    possibles = []
    for row in mat:
        if phase == row[2] and phase in row[5] and search_err(error_list, row[5]): 
            possibles.append(row)
    return possibles


# search if the string contains anything in err_list 
def search_err(err_list, string):
    for err in err_list: 
        if err in string:
            return True
    return False


def initialize(path):
    with open(path, 'rb') as f:
        global MAT
        MAT = pickle.load(f)


def analyze(stage, err_list):
    pos = get_possible_matrix(MAT, stage, err_list)

    total = sum(map(lambda row: row[3], pos))

    Omega, Sight, Harm, Response = {}, {}, {}, {} # Omega is also used as the probability function, and Sight is an abstract RV

    for row in pos:
        if row[1] not in Omega:
            Omega[row[1]] = (row[3] / total)
        else:
            Omega[row[1]] += (row[3] / total)
        Sight[row[1]] = row[5]
        Harm[row[1]] = row[4]
        Response[row[1]] = row[6]

    probs = {}
    errs = set(err_list)
    for fmode in Omega:
        probs[fmode] = Bayes(Omega, Sight, errs, fmode)
    print_eval(dictsort.dsort(probs))


    # suggestion part
    suggest = {}
    for fmode in probs:
        if Response[fmode] not in suggest:
            suggest[Response[fmode]] = probs[fmode] * Harm[fmode]
        else:
            suggest[Response[fmode]] += probs[fmode] * Harm[fmode]

    print_eval(dictsort.dsort(suggest))


# Bayes law used to compute P(fmode | sight)
# formula: P(f|s) = P(s|f)P(f)/P(s)
def Bayes(Omega, Sight, errs, fmode):
    if pbx(Omega, Sight, errs) == 0:
        return 0
    return conditional_pb_rv(Omega, Sight, errs, fmode) * pb(Omega, {fmode}) / pbx(Omega, Sight, errs)


# helper function to print out the results
def print_eval(arr):
    print("\n")
    for item in arr: 
        if  item != '-None':
            print(item, arr[item])
    print("\n")

