def enumerationAsk(X,tf,var,e,value,pindex):
    prod = 1
    valueT = e[:]
    valueF = e[:]
    if isinstance(X,list) and X:
        valueT[var.index(X[0])] = [1]
        valueF[var.index(X[0])] = [0]
        distT = enumerateAll(var,var,valueT,value,pindex)
        distF = enumerateAll(var,var,valueF,value,pindex)
        norm = distT+distF
        distT = distT/norm
        distF = distF/norm
        if tf[0] == '+':
            prod = prod*distT*enumerationAsk(X[1:],tf[1:],var,valueT,value,pindex)
        else:
            prod = prod*distF*enumerationAsk(X[1:],tf[1:],var,valueF,value,pindex)
    elif X:
        valueT[var.index(X)] = [1]
        valueF[var.index(X)] = [0]
        distT = enumerateAll(var,var,valueT,value,pindex)
        distF = enumerateAll(var,var,valueF,value,pindex)
        if tf == '+':
            temp = distT/(distT+distF)
            prod = temp
        else:
            temp = distF/(distT+distF)
            prod = temp

    return prod

def enumerateAll(cvar,var,e,value,pindex):
    if not cvar:
        return 1.0
    Y = cvar[0]
    cvar = cvar[1:]
    index = var.index(Y)
    if e[index] == [1]:
        return condP('+',index,e,value,pindex)*enumerateAll(cvar,var,e,value,pindex)
    elif e[index]==[0]:
        return condP('-',index,e,value,pindex)*enumerateAll(cvar,var,e,value,pindex)
    else:
        vT = e[:]
        vT[index] = [1]
        vF = e[:]
        vF[index] = [0]
        condPT = condP('+',index,e,value,pindex)
        condPF = condP('-',index,e,value,pindex)
        return condPT*enumerateAll(cvar,var,vT,value,pindex)+condPF*enumerateAll(cvar,var,vF,value,pindex)

def condP(tf,index,e,value,pindex):
    temp = []
    if len(value[index])<2:
        if tf == '+':
            return value[index][0]
        else:
            return 1-value[index][0]
    for k in range(0,len(pindex[index])):
        temp.append(e[pindex[index][k]])
    dec = 0
    for k in range(0,len(temp)):
        dec = dec+temp[len(temp)-k-1][0]*pow(2,k)
    dec = pow(2,len(temp))-1-dec
    if tf == '+':
        return value[index][dec]
    else:
        return 1-value[index][dec]
    
    
'''read inputs'''
import sys
with open(sys.argv[1],'r') as f:
    num = int(f.readline())
    var = []
    value = [[] for k in range(10)]
    query = []
    pindex = [[] for k in range(10)]
    for k in range(0,num):
        q = f.readline()
        q = q.split('(')[1]
        q = q.split(')')[0]
        query.append(q)
    line = f.readline()
    while line:
        if '|' not in line:
            line = line.split('\n')[0]
            var.append(line)
            value[var.index(line)]= [float(f.readline())]
        else:
            temp = line.split(' | ')
            parents = temp[1].split(' ')
            child = temp[0]
            var.append(child)
            j = var.index(child)
            for k in range(0,len(parents)):
                parent = parents[k]
                parent = parent.split('\n')[0]
                i = var.index(parent)
                pindex[j].append(i)
            for k in range(0,pow(2,len(pindex[j]))):
                temp = f.readline()
                val = temp.split(' ')[0]
                value[j].append(float(val))
        line = f.readline()
        line = f.readline()

e = value[:]

output = open('output.txt','w')

for k in range(0,num):
    q = query[k]
    if '|' in q:
        temp = q.split(' | ')
        X = temp[0].split(' = ')[0]
        tf = temp[0].split(' = ')[1]
        cond = temp[1].split(', ')
        for j in range(0,len(cond)):
            cvar = cond[j].split(' = ')[0]
            sign = cond[j].split(' = ')[1]
            if sign == '+' :           
                e[var.index(cvar)] = [1]
            else:
                e[var.index(cvar)] = [0]
    else:
        if ',' in q:
            temp = q.split(', ')
            tf = []
            X = []
            for j in range(0,len(temp)):
                X.append(temp[j].split(' = ')[0])
                tf.append(temp[j].split(' = ')[1])
        else:
            X = q.split(' = ')[0]
            tf = q.split(' = ')[1]
    result = enumerationAsk(X,tf,var,e,value,pindex)
    string = str(round(result,2))
    output.write(string+'\n')
    print(string)

output.close()
