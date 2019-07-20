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
       if (curr.domain_size()<min):
            res = curr
            minV = curr.domain_size()
       i+=1
    return res

def val_lcv(csp,var):
    #IMPLEMENT
    res = {}
    dom = var.curr_domain()
    i = 0
    while(i<len(dom)):
        var.assign(dom[i])
        remain = 0
        cons = csp.get_cons_with_var(var)
        j = 0

        while (j< len(cons)):
            k = 0
            varss = cons[j].get_all_unasgn_vars()
            
            while (k<len(values)):
                currVar = varss[k]
                currDom = currVar.curr_domain()
                l = 0

                while (l<len(currDom)):
                    if (cons[j].has_support(currVar,currDom[l])):
                        remain = remain+1
                    l+=1
                k+=1
            j+=1
        res[dom[i]] = remain
        var.unassign()
        i+=1
    if (len(res)==0):
        return None
    sorted_res = sorted(res.items(),key=operator.itemgetter(1))
    return sorted_res
