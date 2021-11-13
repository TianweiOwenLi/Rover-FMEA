from math import prod


# indep_pb: ((fmode * real) dict) * fmode set -> real
# assuming all fmodes are independently distributed, calculates the probability of event s
def pb(Omega, s):
    return 1-prod(map(lambda w: 1 - Omega[w], s))


# inv: ((fmode * real) dict) * ((fmode * 'a) dict) * 'a -> fmode set
# calculates X^{-1}(x) for some random variable X on an element x
def inv(Omega, X, x):
        s = set()
        for w in Omega:
            if X[w].find(x) >= 0: # if the keyword x is contained somewhere in the long string of X[w]
                s.add(w)
        return s


# inv: ((fmode * real) dict) * ((fmode * 'a) dict) * 'a set -> real
# calculates the probability that X(a) is a superset of s, where a is the set of all failure modes currently occurring
def pbx(Omega, X, s):
    return prod(map(lambda x: pb(Omega, inv(Omega, X, x)), s))


# conditional_pb_rv(Omega, X, s, w): ((fmode * real) dict) & ((fmode * 'a) dict) * 'a set * fmode -> real
# calculates the probability of X(a) \in s, provided that w \in a. 
def conditional_pb_rv(Omega, X, s, w):
    return pbx(Omega, X, s - {X[w]})


# fmode = {'f1': 0.3, 'f2': 0.2, 'f3': 0.25, 'f4': 0.25}
# sight = {'f1': 'o1', 'f2': 'o1', 'f3': 'o2', 'f4': 'o3'}
