# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 10:22:03 2022

@author: grace_elizabeth
"""

from gurobipy import *

try:
    
    #Parameters
    lu = [27, 27, 37, 34, 37]
    ll = [22, 22, 32, 28, 32]
    wu = [22, 22, 32, 23, 23]
    wl = [18, 18, 28, 18, 18]
    pu = [98, 98, 138, 104, 120]
    pl = [80, 80, 120, 92, 100]
    f = [
        [0, 10, 15, 20, 0],
        [10, 0, 30, 35, 10],
        [15, 30, 0, 10, 20],
        [20, 35, 10, 0, 15],
        [0, 10, 20, 15, 0]
        ]
    c = [
        [0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1],
        [1, 1, 1, 1, 0]
        ]
    
    #Indices
    n = len(f)
    
    #Create model
    m = Model("Example 11.5")
    
    #Declare decision variables
    x = m.addVars(n, lb = 0, vtype = GRB.CONTINUOUS, name = "x-coordinate")
    y = m.addVars(n, lb = 0, vtype = GRB.CONTINUOUS, name = "y-coordinate")
    xu = m.addVars(n, lb = 0, vtype = GRB.CONTINUOUS, name = "x-upper")
    xl = m.addVars(n, lb = 0, vtype = GRB.CONTINUOUS, name = "x-lower")
    yu = m.addVars(n, lb = 0, vtype = GRB.CONTINUOUS, name = "y-upper")
    yl = m.addVars(n, lb = 0, vtype = GRB.CONTINUOUS, name = "y-lower")
    xp = m.addVars(n, n, lb = 0, vtype = GRB.CONTINUOUS, name = "x-positive")
    xn = m.addVars(n, n, lb = 0, vtype = GRB.CONTINUOUS, name = "x-negative")
    yp = m.addVars(n, n, lb = 0, vtype = GRB.CONTINUOUS, name = "y-positive")
    yn = m.addVars(n, n, lb = 0, vtype = GRB.CONTINUOUS, name = "y-negative")
    
    #Set objective fuction
    m.setObjective(quicksum(c[i][j] * f[i][j] * (xp[i,j] + xn[i,j] + yp[i,j] + yn[i,j]) for i in range(n-1) for j in range(i+1, n)), GRB.MINIMIZE)
    
    #Write constraints
    for i in range(n-1):
        for j in range(i+1, n):
            m.addConstr(x[i] - x[j] == xp[i,j] - xn[i,j], name = "Constraint 11.39")
            m.addConstr(y[i] - y[j] == yp[i,j] - yn[i,j], name = "Constraint 11.40")
   
    for i in range(n):
        m.addConstr(ll[i] <= xu[i] - xl[i], name = "Constraint 11.41.a")
        m.addConstr(xu[i] - xl[i] <= lu[i], name = "Constraint 11.41.b")
        m.addConstr(wl[i] <= yu[i] - yl[i], name = "Constraint 11.42.a")
        m.addConstr(yu[i] - yl[i] <= wu[i], name = "Constraint 11.42.b")
        m.addConstr(pl[i] <= 2*(xu[i] - xl[i] + yu[i] - yl[i]), name = "Constraint 11.43.a")
        m.addConstr(2*(xu[i] - xl[i] + yu[i] - yl[i]) <= pu[i], name = "Constraint 11.43.b")
        m.addConstr(xl[i] <= x[i], name = "Constraint 11.44.a")
        m.addConstr(x[i] <= xu[i], name = "Constraint 11.44.b")
        m.addConstr(yl[i] <= y[i], name = "Constraint 11.45.a")
        m.addConstr(y[i] <= yu[i], name = "Constraint 11.45.b")
    
    m.addConstr(x[4] - x[0] >= xu[4] - xl[4] - (xu[0] - xl[0]), name = "Constraint 11.46 (5,1)")
    m.addConstr(x[2] - x[1] >= xu[2] - xl[2] - (xu[1] - xl[1]), name = "Constraint 11.46 (3,2)")
    m.addConstr(x[3] - x[2] >= xu[3] - xl[3] - (xu[2] - xl[2]), name = "Constraint 11.46 (4,3)")
    m.addConstr(x[3] - x[1] >= xu[3] - xl[3] - (xu[1] - xl[1]), name = "Constraint 11.46 (4,2)")
    m.addConstr(y[1] - y[0] >= yu[1] - yl[1] - (yu[0] - yl[0]), name = "Constraint 11.47 (2,1)")
    m.addConstr(y[2] - y[0] >= yu[2] - yl[2] - (yu[0] - yl[0]), name = "Constraint 11.47 (3,1)")
    m.addConstr(y[3] - y[0] >= yu[3] - yl[3] - (yu[0] - yl[0]), name = "Constraint 11.47 (4,1)")
    m.addConstr(y[1] - y[4] >= yu[1] - yl[1] - (yu[4] - yl[4]), name = "Constraint 11.47 (2,5)")
    m.addConstr(y[2] - y[4] >= yu[2] - yl[2] - (yu[4] - yl[4]), name = "Constraint 11.47 (3,5)")
    m.addConstr(y[3] - y[4] >= yu[3] - yl[3] - (yu[4] - yl[4]), name = "Constraint 11.47 (4,5)")
    m.addConstr(xl[4] >= xu[0], name = "Constraint 11.48 (5,1)")
    m.addConstr(xl[2] >= xu[1], name = "Constraint 11.48 (3,2)")
    m.addConstr(xl[3] >= xu[2], name = "Constraint 11.48 (4,3)")
    m.addConstr(xl[3] >= xu[1], name = "Constraint 11.48 (4,2)")
    m.addConstr(yl[1] >= yu[0] + 5, name = "Constraint 11.49 (2,1)")
    m.addConstr(yl[2] >= yu[0] + 5, name = "Constraint 11.49 (3,1)")
    m.addConstr(yl[3] >= yu[0] + 5, name = "Constraint 11.49 (4,1)")
    m.addConstr(yl[1] >= yu[4] + 5, name = "Constraint 11.49 (2,5)")
    m.addConstr(yl[2] >= yu[4] + 5, name = "Constraint 11.49 (3,5)")
    m.addConstr(yl[3] >= yu[4] + 5, name = "Constraint 11.49 (4,5)")


    #Call Gurobi Optimizer
    m.optimize()
    if m.status == GRB.OPTIMAL:
       for v in m.getVars():
           print('%s = %g' % (v.varName, v.x)) 
       print('Obj = %f' % m.objVal)
    elif m.status == GRB.INFEASIBLE:
       print('LP is infeasible.')
    elif m.status == GRB.UNBOUNDED:
       print('LP is unbounded.')
except GurobiError:
    print('Error reported')