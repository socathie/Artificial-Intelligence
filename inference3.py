'''misc. functions'''
def op(x):
    return x.split('(')[0]

def arg(x):
    y = x.split('(')[1]
    y = y.split(')')[0]
    return y.split(',')

def rest(x):
    y = list(x)
    y.pop(0)
    return y

def first(x):
    return x.pop(0)

'''unifications'''
def unifyVar(var,x,L):
    if var in x:
        return 'failure'
    else:
        return x
    
def unify(x,y,L):
    if L == 'failure':
        return 'failure'
    if x==y:
        return L
    elif x == 'x':
        return unifyVar(x,y,L)
    elif y == 'x':
        return unifyVar(y,x,L)
    elif '(' in x and '(' in y:
        return unify(arg(x),arg(y),unify(op(x),op(y),L))
    elif type(x) is list and type(y) is list:
        return unify(rest(x),rest(y),unify(first(x),first(y),L))
    else:
        return 'failure'

imply = []
fact = []

'''read inputs'''
import sys
with open(sys.argv[1],'r') as f:
    doc = f.read().splitlines()
    query = doc.pop(0)
    m = int(doc.pop(0))
    for i in range(0,m):
        line = doc[i]
        if '=>' in line:
            if '&' in line:
                lhs1 = line.split('&')[0]
                lhs2 = line.split('&')[1]
                lhs2 = lhs2.split('=')[0]
                rhs = line.split('>')[1]
                imply.append([lhs1,lhs2,rhs])
            else:
                lhs1 = line.split('=')[0]
                rhs = line.split('>')[1]
                imply.append([lhs1,rhs])
        else:
            fact.append(line)

def findImply(x):
    q = []
    for i in range(0,len(imply)):
        if imply[i][-1] == x:
            q.append(imply[i][0])
            if imply[i][0] is not imply[i][-2]:
                q.append(imply[i][-2])
    return q

def inferVar(x,output):
    output.write('Query: '+x+'\n')
    f = findImply(x)
    if f:
        if f[0] is not f[-1]:
            output.write('Query: '+f[0]+'&'+f[-1]+'=>'+x+'\n')
        else:
            output.write('Query: '+f[0]+'=>'+x+'\n')
    sol = []
    andSol = []
    if f:
        for i in range(0,len(f)):
            andSol.append(inferVar(f[i],output))
        sol = list(set(andSol[0]) & set(andSol[-1]))
    for i in range(0,len(fact)):
        L = []
        u = unify(x,fact[i],L)
        if (u is not 'failure') and (u not in sol):
            sol.append(u)
    sol.sort()
    if sol:
        output.write(x+': True: '+str(sol)+'\n')
    else:
        output.write(x+': False\n')
    return sol

def checkFact(x,con):
    y = x.replace('x',con)
    if y in fact:
        return 1
    else:
        return 0

def inferCon(x,con,output):
    output.write('Query: '+x+'\n')
    if 'x' not in x:
        if x in fact:
            output.write(x+': True\n')
            return 'x'
        for i in range(0,len(imply)):
            con = unify(x,imply[i][-1],[])
            if con is not 'failure':
                y = x.replace(con,'x')
                f = findImply(y)
                if f:
                    if f[0] is not f[-1]:
                        output.write('Query: '+f[0]+'&'+f[-1]+'=>'+y+'\n')
                    else:
                        output.write('Query: '+f[0]+'=>'+y+'\n')
                sol = []
                andSol = []
                if f:
                    for i in range(0,len(f)):
                        andSol.append(inferCon(f[i],con,output))
                    sol = list(set(andSol[0]) & set(andSol[-1]))
                for i in range(0,len(fact)):
                    L = []
                    u = unify(x,fact[i],L)
                    if (u is not 'failure') and (u not in sol):
                        sol.append(u)
                if 'x' in sol or con in sol:
                    output.write(x+': True\n')
                else:
                    output.write(x+': False\n')
        return sol
    else:
        if checkFact(x,con):
            output.write(x+': True\n')
            return 'x'
        f = findImply(x)
        if f:
            if f[0] is not f[-1]:
                output.write('Query: '+f[0]+'&'+f[-1]+'=>'+x+'\n')
            else:
                output.write('Query: '+f[0]+'=>'+x+'\n')
        sol = []
        andSol = []
        if f:
            for i in range(0,len(f)):
                andSol.append(inferCon(f[i],con,output))
            sol = list(set(andSol[0]) & set(andSol[-1]))
        for i in range(0,len(fact)):
            L = []
            u = unify(x,fact[i],L)
            if (u is not 'failure') and (u not in sol):
                sol.append(u)
        if 'x' in sol or con in sol:
            output.write(x+': True\n')
        else:
            output.write(x+': False\n')
    return sol

'''if compound'''
output = open('output.txt','w')
if '&' in query:
    output.write('Query: '+query+'\n')
    query1 = query.split('&')[0]
    query2 = query.split('&')[1]
    if 'x' in query1:
        sol1 = inferVar(query1,output)
    else:
        sol1 = inferCon(query1,[],output)
    if 'x' in query2:
        sol2 = inferVar(query2,output)
    else:
        sol2 = inferCon(query2,[],output)
    sol = list(set(sol1) and set(sol2))
    if sol and 'x' in query:
        output.write(query+': True:'+str(sol)+'\n')
    elif sol:
        output.write(query+': True\n')
    else:
        output.write(query+': False\n')
else:
    if 'x' in query:
        inferVar(query,output)
    else:
        inferCon(query,[],output)

