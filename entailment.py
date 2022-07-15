from sympy.logic.boolalg import Or, And, to_cnf
from itertools import combinations



def entailment(belief_base, prop):
    """
    Description: 
        Checks for entailment between the beliefs in the belief base and the proposition to 
        introduce to the system.
    Input:
        belief_base <list>: list of objects corresponding to the Belief class in the belief base
        prop <str/SympyExpression>: (both types work and are supported) proposition to check
            for entailment with the belief base
    Returns:
        <bool>: the output is True in case of entailment and False otherwise 

    *Note*: the comented lines are from a different type of implemtation with lists instead of sets
        which didn't perform as expected and had to discard but we decided to show the work done anyways.
        Hope it is not an inconvenience
    """
    clauses = []
    prop = to_cnf(prop)
    for belief in belief_base:
        b_cnf = to_cnf(belief.proposition)
        if isinstance(b_cnf, And):
            clauses += list(b_cnf.args)
        else:
            clauses.append(b_cnf)
   
    clauses += dissociate(to_cnf(~prop))

    if False in clauses:
        return True

    result = set()
    #result = []
    while True:
        pairs = list(combinations(clauses,2))

        #res_new = []
        for i,j in pairs:
            temp = pl_resolve(i,j)
            if False in temp:
                return True
            # if len(temp) != 0:
            #     res_new.append(temp)
            result = result.union(set(temp))

        # result = [item for sublist in res_new for item in sublist]
        # result = list(set(result))

        if result.issubset(set(clauses)):
            return False
        # if all(x in clauses for x in result):
        #     return False

        for element in result:
            if element not in clauses:
                clauses.append(element)


def pl_resolve(left, right):
    """
    Description:
        Checks the pair of clauses and compare its elements one by one. In the case complementaries
        show it removes them and creates a new clause. Corresponds to the Full-Resolution Rule
        explained in class.
    Input:
        left <SympyExpression>: left clause in the pair, elements separated by '|'
        right <SympyExpression>: right clause in the pair, elements separated by '|'
    Returns:
        result <list>: contains all the new clauses generated from comparison, in case the empty clause
            is reached, one of those values will be False
    """
    result = []
    
    left_syms = dissociate(left)
    right_syms = dissociate(right)

    resultant = []
    for ls in left_syms:
        for rs in right_syms:
            if ls == ~rs or ~ls == rs:
                resultant = _remove_sym(ls, left_syms) + _remove_sym(rs, right_syms)

                resultant = list(set(resultant))

                if len(resultant) == 0:
                    result.append(False)
                elif len(resultant) == 1:
                    result.append(resultant[0])
                else:
                    result.append(Or(*resultant))

    return result
    

def dissociate(x):
    """
    Description:
        Checks the expression and returns the elements separated for the Full-Resolution Rule implementation
    Input:
        x <SympyExpression>: expression to dissociate
    Returns:
        out <list>: elements separated
    """
    if len(list(x.args)) < 2:
        out = [x]
    else:
        out = list(x.args)
    return out


def _remove_sym(sym, clause):
    """
    Description:
        Removes the element desired from the clause
    Input:
        sym <SympyExpression>: element to remove
        clause <list>: list containing all elements from a clause
    Returns:
        <list>: returns the input clause without the element wanted to be removed
    """
    return [s for s in clause if s != sym]
