#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

# global value
path = []

def FCCheck(const, var):
    res = 0
    vars = []
    for i in const.get_scope():
    	vars.append(i.get_assigned_value())

    j = 0
    while (j<len(vars)):
    	if (None==vars[j]):
    		break
    	j+=1

    for x in var.cur_domain():
    	vars[j]=x
    	if (not const.check(vars)):
    		if((var,d) not in path):
    			var.prune_value(x)
    			path.append((var,x))

    			if (var.cur_domain_size()!=0):
    				res = 0
    			else:
    				res = 1
    return res
    

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
#IMPLEMENT
    constraints = []
    # all var assigned find certain cons
    if (newVar!=None):
        constraints = csp.get_cons_with_var(newVar);
    else:
        constraints = csp.get_all_cons()
    i = 0
    while (i<len(constraints)):
    	c = constraints[i]
    	i+=1
    	if (c.get_n_unasgn()==1):
    		var = c.get_unasgn_vars()[0]
    		if (FCCheck(c,var)==1):
    			return (False, path)
    return (True,path)


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
#IMPLEMENT
    constraints = csp.get_all_cons()
    queue = []
    modify = []
    if (newVar!=None):
    	constraints = csp.get_cons_with_var(newVar)
    queue = constraints
    while len(queue)>0:
    	con = queue[0]
    	queue = queue[1:]
    	variables = con.get_scope()
    	i = 0
    	while (i<len(variables)):
    		var = variables[i]
    		i+=1
    		j = 0
    		doms = var.cur_domain()
    		while (j<len(doms)):
    			dom = doms[j]
    			j+=1
    			if (not con.has_support(var,dom)):
    				if ((var,dom)not in modify):
    					modify.append((var,dom))
    					var.prune_value(dom)
    				if (var.cur_domain_size()!=0):
    					others = csp.get_cons_with_var(var)
    					k = 0
    					while (k<len(others)):
    						if (others[k]not in queue):
    							queue.append(others[k])
    						k+=1
    				else:
    					queue = []
    					return (False,modify)

    
    return True,res
