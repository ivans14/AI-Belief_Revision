from sympy.logic.boolalg import to_cnf

def _to_cnf(proposition):
    """
    Description:
        Removal of a bi-implication from a proposition (1st step), to convert to CNF-form
    Input:
        proposition <str>: proposition to check if it has a bi-implication (<=>)
    Returns:
        <SympyExpression>: input propositon in CNF-form
    """
    if isinstance(proposition,str):
        if '<=>' in proposition:
            proposition = remove_bimplication(proposition)
    return to_cnf(proposition)


def remove_bimplication(proposition):
    """
    Description:
        Removes bi-implication from a proposition
    Input:
        proposition <str>: proposition to remove bi-implication (<=>)
    Returns:
        new_proposition <str>: input propositon with its equivalence without the bi-implication (<=>) 
    """
    if proposition.count('<=>') > 1: raise Exception('Maximum allowed bi-implications reached per proposition')

    [left, right] = proposition.split('<=>')
    new_proposition = f'({left}>>{right})&({right}>>{left})'
    return new_proposition
