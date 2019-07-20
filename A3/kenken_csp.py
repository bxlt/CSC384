#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
from cspbase import *
import itertools
import operator

def binary_ne_grid(kenken_grid):
    ##IMPLEMENT
    # find size
    n = kenken_grid[0][0]
    field = []
    for i in range(1,n+1):
        field.append(i)
    # create grid
    variables = []
    legal = []
    i = 0
    while (i<len(field)):
        level = []
        j = 0
        while(j<len(field)):
            level.append(Variable("C"+str(i+1)+str(j+1), domain))
            legal.append((i+1,j+1))
            j = j+1
        variables.append(level)
        i = i+1

    csp = CSP('KenKen')
    for row in variables:
        for col in row:
            csp.add_var(col)
    # Create binary constraints
    a = 0
    while a<n:
        b = 0
        while b<n:
            c = b+1
            while c<n:
                right = Constraint(str(a)+str(b)+'-'+str(a)+str(c),[variables[a][b], variables[a][c]])
                left = Constraint(str(b)+str(a)+'-'+str(c)+str(a),[variables[b][a], variables[c][a]])
                csp.add_constraint(right.add_satisfying_tuples(legal))
                csp.add_constraint(left.add_satisfying_tuples(legal))
                c= c+1
            b =b+1
        a = a+1

    return csp, variables


def nary_ad_grid(kenken_grid):
    ##IMPLEMENT
    n = kenken_grid[0][0]
    field = []
    for i in range(1, n + 1):
        field.append(i)
    # create board
    variables = []
    legal = list(permutations(field,n))
    i = 0
    while i < len(field):
        level = []
        j = 0
        while j < len(field):
            level.append(Variable("C" + str(i + 1) + str(j + 1), domain))
            j = j + 1
        variables.append(level)
        i = i + 1

    csp = CSP('kenken')
    for row in variables:
        for col in row:
            csp.add_var(col)

    for a in range(0,n):
        row_c = Constraint('r' + str(a), vars[a])
        cols = []
        for r in variables:
            cols.append(r[a])
        col_c = Constraint('c' + str(a), cols)
        csp.add_constraint(row_c.add_satisfying_tuples(legal))
        csp.add_constraint(col_c.add_satisfying_tuples(legal))
    return csp, variables

def kenken_csp_model(kenken_grid):
    ##IMPLEMENT
    pass