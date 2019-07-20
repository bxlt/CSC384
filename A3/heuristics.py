#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random
import operator
'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''

def ord_mrv(csp):
    #IMPLEMENT
    all_vars = csp.get_all_unasgn_vars()
    minV = 999999
    res = None
    i = 0
    while (i<len(all_vars)):
       curr = all_vars[i]
       if (curr.domain_size()<minV):
            res = curr
            minV = curr.domain_size()
       i+=1
    return res

def val_lcv(csp,var):
    #IMPLEMENT
    res = {}
    dom = var.cur_domain()
    i = 0
    while(i<len(dom)):
        currValue = dom[i]
        var.assign(currValue)
        remain = 0
        cons = csp.get_cons_with_var(var)
        j = 0
        while (j< len(cons)):
            k = 0
            con = cons[j]
            unsign = con.get_unasgn_vars()
            while (k<len(unsign)):
                currVar = unsign[k]
                resDom = currVar.cur_domain()
                l = 0
                while (l<len(resDom)):
                    if (con.has_support(currVar,resDom[l]) is False):
                        remain = remain+1
                    l+=1
                k+=1
            j+=1
        res[currValue] = remain
        var.unassign()
        i+=1
    #print(res)
    sorted_res = sorted(res,key=res.get)
    #print(sorted_res)
    return sorted_res
