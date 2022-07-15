from sympy.logic.boolalg import to_cnf
from entailment import *


def _check_order(n):
    """
    Description:
        Checks the order of the proposition is withing range (0=<n<=1)
    Input:
        n <int>: order of the proposition
    Returns:
        raise Exception to handle out of bounds for the order
    """
    if not((0 <= n) and (n <= 1)):
        raise Exception('The order of a belief must be between 0 and 1')


class Belief:
    """
    Descrition:
        Class containing the information of a belief (proposition and order). Order is used to
        organize the pausivility of the belief in the Belief Base.

        Some operators have being overloaded for operating with the class
    """
    def __init__(self, proposition=None, order=None):
        self.proposition = proposition
        self.order = order

    def __eq__(self, other):
        return self.proposition == other.proposition and self.order == other.order

    def __ne__(self, other):
        return not self == other

    def __ge__(self, other):
        return self.order >= other.order

    def __gt__(self,other):
        return self.order > other.order

    def __repr__(self):
        """
        Prints the belief in the form: Belief: p || Order: 0.1
        """
        return f'Belief: {self.proposition} || Order: {self.order}'



class BeliefBase:
    """
    Description:
        Class defined for the Belief base which contains the different beliefs<object>. The class possess
        the operations from any Belief base: revision, contraction and expansion.

        The different beliefs are ordered by descending order of plausivility.
    """
    def __init__(self):
        self.beliefs = []

    def add_belief(self, other):
        """
        Add a belief to the belief base sorted by order, the highest order first.
        In case the belief is already in the belief base it is ignored.
        """
        # Checks if the order is within range
        _check_order(other.order)

        # Update in case belief already exists
        self.delete_belief(other)
        
        if len(self.beliefs) == 0 or self.beliefs[-1] >= other:
            self.beliefs.append(other)
        else:
            for idx, b in enumerate(self.beliefs):
                if other >= b:
                    self.beliefs.insert(idx, other)
                    break

    def delete_belief(self, other):
        """
        Delete a beliefs equal to 'other'
        """
        self.beliefs = [belief for belief in self.beliefs if belief.proposition != other.proposition]                

    def delete_belief_idx(self, idx):
        """
        Deletes a belief by index.
        """
        self.beliefs.pop(idx)


    def revise(self, other):
        """
        Revises the belief base with the new belief. In case of inconsistency the belief base is
        modified to remain consistent with the new belief. The new belief system should contain as much
        information as possible
        """
        try:
            prop_cnf = to_cnf(other.proposition)
        except SyntaxError:
            print('Proposition not accepted by the system, check the README.md for more information')

        _check_order(other.order)

        # If too many arguments the negation will crash the program therefore we simplify 
        # just for the contradiction step using Quine-McCluskey algorithm
        if len(list(prop_cnf.args)) > 3:
            prop_cnf = to_cnf(prop_cnf, True, True)

        # Check for contradiction in proposition
        if not entailment([], ~prop_cnf):
            prop_cnf = to_cnf(other.proposition)
            # If tautology change order to maximum (always true)
            if entailment([], prop_cnf):
                other.order = 1
            elif not entailment(self.beliefs, prop_cnf):
                    # Levi Identity for revision
                    self.contract(Belief(~to_cnf(other.proposition), other.order))
            else:
                    self.contract(other)
            self.expand(other)

    def contract(self, other):
        """
        Removes any belief from the belief base needed so there are no contradictions
        """
        # Set of maximal subset of KB that not imply other
        prop_cnf = to_cnf(other.proposition)
        _check_order(other.order)

        _to_delete = []
        clauses_pre = self.get_clauses()
        for i, belief in enumerate(self.beliefs):
            if entailment(self.beliefs[0:i+1], prop_cnf) and other > belief:
                _to_delete.append(belief)

        self.beliefs = [belief for belief in self.beliefs if belief not in _to_delete]
        clauses = self.get_clauses()
        if not clauses.issubset(clauses_pre):
            # Contracted set B' is a subset of B (Success)
            raise Exception('An error arise in contraction and Belief base changed')

    def expand(self, other):
        """
        Adds a new belief in the system by expanding it
        """
        prop_cnf = other.proposition
        _check_order(other.order)

        for i, belief in enumerate(self.beliefs):
            if entailment(self.beliefs[0:i+1], prop_cnf):
                if other >= belief:
                    self.add_belief(other)
                else:
                    break

    def get_clauses(self):
        """
        Obtaines the set of all clauses in all the beliefs in the belief base
        
        Returns:
            <set>: union of all the clauses in the belief system
        """
        clauses = []
        for belief in self.beliefs:
            b_cnf = to_cnf(belief.proposition)
            if isinstance(b_cnf, And):
                clauses += list(b_cnf.args)
            else:
                clauses.append(b_cnf)

        result = set()
        while True:
            pairs = list(combinations(clauses,2))
            for i,j in pairs:
                temp = pl_resolve(i,j)
                if False in temp:
                    temp = [item for item in temp if item != False]
                result = result.union(set(temp))

            if result.issubset(set(clauses)):
                # Return a set of all possible clauses
                return set(clauses) 

            for element in result:
                if element not in clauses:
                    clauses.append(element)

    def clear(self):
        """
        Empty the Belief base
        """
        self.beliefs.clear()

    def __repr__(self):
        """
        Overhaul of the print method for the Belief base so it would show empty without beliefs and
        print all the beliefs in series when required. The printing method would correspond to the
        overload of the Belief class
        """
        if len(self.beliefs) == 0:
            return '\nBelief base: Empty'
        return '\n'.join(str(belief) for belief in self.beliefs)

    def __len__(self):
        return len(self.beliefs)
