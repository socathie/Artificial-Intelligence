'''basic functions'''
def string(word):
    if word > 1000000:
        return 'Infinity'
    elif word < -1000000:
        return '-Infinity'
    else:
        return str(word)

def coord(N,i,j):
    txt = chr(j+ord('A'))
    txt = txt + str(N-i)
    return txt

def adj(n,i,j):
    if (n==1):
        x = i-1
        y = j-1
    elif (n==2):
        x = i-1
        y = j
    elif (n==3):
        x = i-1
        y = j+1
    elif (n==4):
        x = i
        y = j-1
    elif (n==5):
        x = i
        y = j+1
    elif (n==6):
        x = i+1
        y = j-1
    elif (n==7):
        x = i+1
        y = j
    elif (n==8):
        x = i+1
        y = j+1
    return [x,y]

def nextStep(i,j,N,state):
    absSum = 0
    for n in range (1,9):
        x = adj(n,i,j)[0]
        y = adj(n,i,j)[1]
        if (x>=0) and (x<N) and (y>=0) and (y<N):
            absSum += abs(state[x][y])
    if absSum > 0:
        return 1
    else:
        return 0

'''eval function'''
def evalBoard(ply,N,i,j,tempState):
    score = 0
    if ply == 1: #black
        tempState = [[x*(-1) for x in y] for y in tempState]
    #invert the board to treat ourselves as white

    posSum = []
    negSum = []
    posSum.append(0)
    negSum.append(0)
    #sum up adjacent lines
    for n in range(1,9):
        posSum.append(0)
        negSum.append(0)
        x = adj(n,i,j)[0]
        y = adj(n,i,j)[1]
        while (x>=0) and (y>=0) and (x<N) and (y<N) and (tempState[x][y]>0):
            posSum[n] +=1
            x = adj(n,x,y)[0]
            y = adj(n,x,y)[1]
        x = adj(n,i,j)[0]
        y = adj(n,i,j)[1]
        while (x>=0) and (y>=0) and (x<N) and (y<N) and (tempState[x][y]<0):
            negSum[n] -=1
            x = adj(n,x,y)[0]
            y = adj(n,x,y)[1]

    for n in range(1,9):
        #blockClosedFour
        if (negSum[n]==-4):
            x = adj(n,i,j)[0]
            y = adj(n,i,j)[1]
            for k in range(0,4):
                x = adj(n,x,y)[0]
                y = adj(n,x,y)[1]
            if (x<0) or (y<0) or (x>=N) or (y>=N) or (tempState[x][y]>0):
                score += 10000
        #blockThree
        elif (negSum[n]==-3):
            x = adj(n,i,j)[0]
            y = adj(n,i,j)[1]
            for k in range(0,3):
                x = adj(n,x,y)[0]
                y = adj(n,x,y)[1]
            #blockClosedThree
            if (x<0) or (y<0) or (x>=N) or (y>=N) or (tempState[x][y]>0):
                score += 100
            #blockOpenThree
            else:
                score += 500
    for n in range(1,5):
        temp = posSum[n]+posSum[9-n]+1
        #win
        if (temp==5):
            score += 50000
        elif (temp==4):
            x1 = adj(n,i,j)[0]
            y1 = adj(n,i,j)[1]
            x2 = adj(9-n,i,j)[0]
            y2 = adj(9-n,i,j)[1]
            for k in range(0,posSum[n]):
                x1 = adj(n,x1,y1)[0]
                y1 = adj(n,x1,y1)[1]
            for k in range(0,posSum[9-n]):
                x2 = adj(9-n,x2,y2)[0]
                y2 = adj(9-n,x2,y2)[1]
            #createClosedFour
            if (x1<0) or (y1<0) or (x1>=N) or (y1>=N) or (tempState[x1][y1]<0):
                if (x2<0) or (y2<0) or (x2>=N) or (y1>=N) or (tempState[x2][y2]<0):
                    pass
                else:
                    score += 1000
            elif (x2<0) or (y2<0) or (x2>=N) or (y1>=N) or (tempState[x2][y2]<0):
                score += 1000
            #createOpenFour
            else:
                score += 5000
        elif (temp==3):
            x1 = adj(n,i,j)[0]
            y1 = adj(n,i,j)[1]
            x2 = adj(9-n,i,j)[0]
            y2 = adj(9-n,i,j)[1]
            for k in range(0,posSum[n]):
                x1 = adj(n,x1,y1)[0]
                y1 = adj(n,x1,y1)[1]
            for k in range(0,posSum[9-n]):
                x2 = adj(9-n,x2,y2)[0]
                y2 = adj(9-n,x2,y2)[1]
            #createClosedThree
            if (x1<0) or (y1<0) or (x1>=N) or (y1>=N) or (tempState[x1][y1]<0):
                if (x2<0) or (y2<0) or (x2>=N) or (y1>=N) or (tempState[x2][y2]<0):
                    pass
                else:
                    score += 10
            elif (x2<0) or (y2<0) or (x2>=N) or (y1>=N) or (tempState[x2][y2]<0):
                score += 10
            #createOpenThree
            else:
                score += 50
        elif (temp==2):
            x1 = adj(n,i,j)[0]
            y1 = adj(n,i,j)[1]
            x2 = adj(9-n,i,j)[0]
            y2 = adj(9-n,i,j)[1]
            for k in range(0,posSum[n]):
                x1 = adj(n,x1,y1)[0]
                y1 = adj(n,x1,y1)[1]
            for k in range(0,posSum[9-n]):
                x2 = adj(9-n,x2,y2)[0]
                y2 = adj(9-n,x2,y2)[1]
            #createClosedTwo
            if (x1<0) or (y1<0) or (x1>=N) or (y1>=N) or (tempState[x1][y1]<0):
                if (x2<0) or (y2<0) or (x2>=N) or (y1>=N) or (tempState[x2][y2]<0):
                    pass
                else:
                    score += 1
            elif (x2<0) or (y2<0) or (x2>=N) or (y1>=N) or (tempState[x2][y2]<0):
                score += 1
            #createOpenTwo
            else:
                score += 5
    
    return score

'''greedy'''
def greedy(ply,N,state):
    score = 0
    tempState = list(state)
    if ply == 1: #black
        move = -1
    elif ply == 2:
        move = 1
    for j in range(0,N):
        for i in range(1,N+1):
            if (state[N-i][j]==0):
                if nextStep(N-i,j,N,state):
                    tempState[N-i][j] = move
                    temp = evalBoard(ply,N,N-i,j,tempState)
                    if temp > score:
                        score = temp
                        imove = N-i
                        jmove = j
                    tempState[N-i][j] = 0
    nextState = list(state)
    nextState[imove][jmove] = move
    with open('next_state.txt','w') as output:
        for i in range(0,N):
            line = ''
            for j in range(0,N):
                if (nextState[i][j]==0):
                    txt = '.'
                elif (nextState[i][j]==1):
                    txt = 'w'
                elif (nextState[i][j]==-1):
                    txt = 'b'
                line = line + txt
            output.write(line+'\n')
    return

'''minimax'''
def maxValue(depth,ply,d,N,i,j,state,log,value):
    lastNode = coord(N,i,j)
    Eval = -evalBoard(ply,N,i,j,state)
    if (d==0) or (Eval<=-50000):
        return value+Eval
    if ply == 1:
        move = 1
        ply = 2
    else:
        move = -1
        ply = 1
    tempState = list(state)
    bestMax = float('-inf')
    for j in range(0,N):
        for i in range(1,N+1):
            if (state[N-i][j]==0):
                 if nextStep(N-i,j,N,state):
                    node = coord(N,N-i,j)
                    tempState[N-i][j] = move
                    log.write(lastNode+','+str(depth-d)+','+string(bestMax)+'\n')
                    v = value+minValue(depth,ply,d-1,N,N-i,j,tempState,log,Eval)
                    bestMax = max(v,bestMax)
                    log.write(node+','+str(depth-d+1)+','+str(v)+'\n')
                    tempState[N-i][j] = 0
    return bestMax

def minValue(depth,ply,d,N,i,j,state,log,value):
    lastNode = coord(N,i,j)
    Eval = evalBoard(ply,N,i,j,state)
    if (d==0) or (Eval>=50000):
        return value+Eval
    if ply == 1:
        move = 1
        ply = 2
    else:
        move = -1
        ply = 1
    tempState = list(state)
    bestMin = float('inf')
    for j in range(0,N):
        for i in range(1,N+1):
            if (state[N-i][j]==0):
                if nextStep(N-i,j,N,state):
                    tempState[N-i][j] = move
                    node = coord(N,N-i,j)
                    line = lastNode+','+str(depth-d)+','+string(bestMin)+'\n'
                    log.write(line)
                    v = value+maxValue(depth,ply,d-1,N,N-i,j,tempState,log,Eval)
                    bestMin = min(v,bestMin)
                    log.write(node+','+str(depth-d+1)+','+str(v)+'\n')
                    tempState[N-i][j] = 0
    return [bestMin,line]
    
def minimax(ply,d,N,state):
    log = open('traverse_log.txt','w')
    log.write('Move,Depth,Value\n')
    log.write('root,0,-Infinity\n')
    depth = d
    best = float('-inf')
    tempState = list(state)
    if ply == 1: #black
        move = -1
    else:
        move = 1
    for j in range(0,N):
        for i in range(1,N+1):
            if (state[N-i][j]==0):
                if nextStep(N-i,j,N,state):
                    node = coord(N,N-i,j)
                    tempState[N-i][j] = move
                    v = minValue(depth,ply,d-1,N,N-i,j,tempState,log,0)
                    line = v[1]
                    v = v[0]
                    if v > best:
                        best = v
                        imove = N-i
                        jmove = j
                    tempState[N-i][j] = 0
                    log.write(line)
                    log.write('root,0,'+str(best)+'\n')
    nextState = list(state)
    nextState[imove][jmove] = move
    with open('next_state.txt','w') as output:
        for i in range(0,N):
            line = ''
            for j in range(0,N):
                if (nextState[i][j]==0):
                    txt = '.'
                elif (nextState[i][j]==1):
                    txt = 'w'
                elif (nextState[i][j]==-1):
                    txt = 'b'
                line = line + txt
            output.write(line+'\n')
    log.close()
    return

'''alpha-beta pruning'''
def alphabeta(ply,d,N,state):
    global a
    a = float('-inf')
    global b
    b = float('inf')
    log = open('traverse_log.txt','w')
    log.write('Move,Depth,Value,Alpha,Beta\n')
    log.write('root,0,-Infinity,-Infinity,Infinity\n')
    depth = d
    best = float('-inf')
    tempState = list(state)
    if ply == 1: #black
        move = -1
    else:
        move = 1
    for j in range(0,N):
        for i in range(1,N+1):
            if (state[N-i][j]==0):
                if nextStep(N-i,j,N,state):
                    node = coord(N,N-i,j)
                    tempState[N-i][j] = move
                    v = beta(depth,ply,d-1,N,N-i,j,tempState,log,0)
                    line = v[1]
                    v = v[0]
                    if v > best:
                        best = v
                        imove = N-i
                        jmove = j
                    tempState[N-i][j] = 0
                    log.write(node+',1,'+str(v)+','+string(a)+','+string(b)+'\n')
                    a = best
                    b = float('inf')
                    log.write('root,0,'+str(best)+','+string(a)+','+string(b)+'\n')
    nextState = list(state)
    nextState[imove][jmove] = move
    with open('next_state.txt','w') as output:
        for i in range(0,N):
            line = ''
            for j in range(0,N):
                if (nextState[i][j]==0):
                    txt = '.'
                elif (nextState[i][j]==1):
                    txt = 'w'
                elif (nextState[i][j]==-1):
                    txt = 'b'
                line = line + txt
            output.write(line+'\n')
    log.close()
    return

def alpha(depth,ply,d,N,i,j,state,log,value):
    global a
    global b
    lastNode = coord(N,i,j)
    Eval = -evalBoard(ply,N,i,j,state)
    if (d==0) or (Eval<=-50000):
        return value+Eval
    if ply == 1:
        move = 1
        ply = 2
    else:
        move = -1
        ply = 1
    tempState = list(state)
    bestMax = float('-inf')
    for j in range(0,N):
        for i in range(1,N+1):
            if (state[N-i][j]==0):
                 if nextStep(N-i,j,N,state):
                    node = coord(N,N-i,j)
                    tempState[N-i][j] = move
                    log.write(lastNode+','+str(depth-d)+','+string(bestMax)+','+string(a)+','+string(b)+'\n')
                    v = value+beta(depth,ply,d-1,N,N-i,j,tempState,log,Eval)
                    bestMax = max(v,bestMax)
                    log.write(node+','+str(depth-d+1)+','+str(v)+','+string(a)+','+string(b)+'\n')
                    tempState[N-i][j] = 0
                    if (bestMax >= b):
                        return bestMax
                    a = max(a,bestMax)
    return bestMax

def beta(depth,ply,d,N,i,j,state,log,value):
    global a
    global b
    lastNode = coord(N,i,j)
    Eval = evalBoard(ply,N,i,j,state)
    if (d==0) or (Eval>=50000):
        return value+Eval
    if ply == 1:
        move = 1
        ply = 2
    else:
        move = -1
        ply = 1
    tempState = list(state)
    bestMin = float('inf')
    for j in range(0,N):
        for i in range(1,N+1):
            if (state[N-i][j]==0):
                if nextStep(N-i,j,N,state):
                    tempState[N-i][j] = move
                    node = coord(N,N-i,j)
                    line = lastNode+','+str(depth-d)+','+string(bestMin)+','+string(a)+','+string(b)+'\n'
                    log.write(line)
                    v = value+alpha(depth,ply,d-1,N,N-i,j,tempState,log,Eval)
                    bestMin = min(v,bestMin)
                    log.write(node+','+str(depth-d+1)+','+str(v)+','+string(a)+','+string(b)+'\n')
                    tempState[N-i][j] = 0
                    if (bestMin<=a):
                        return [bestMin,line]
                    b = min(b, bestMin)
    return [bestMin,line]
    
'''read inputs'''
import sys
state = []
with open(sys.argv[1],'r') as f:
    task = int(f.readline())
    ply = int(f.readline())
    d = int(f.readline())
    N = int(f.readline())
    for i in range(0,N):
        state.append([])
        for j in range(0,N):
            temp = f.read(1)
            if (temp == '.'):
                state[i].append(0)
            elif (temp == 'w'):
                state[i].append(1)
            elif (temp == 'b'):
                state[i].append(-1)
        f.read(1)

'''execute'''
if (task == 1):
    greedy(ply,N,state)
elif (task == 2):
    minimax(ply,d,N,state)
elif (task == 3):
    alphabeta(ply,d,N,state)
