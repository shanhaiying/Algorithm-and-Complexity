import numpy as np 
import pdb
penalty_matrix = np.array([[0,1,2,1,3],
                             [1,0,1,5,1],
                             [2,1,0,9,1],
                             [1,5,9,0,1],
                             [3,1,1,1,0]])
Path = list()
def char2num(sequence: str):
    """
    Turn the four characters {A,T,G,C} into {1,2,3,4} 
    Args: 
        sequence (str):the input DNA sequence
    Return:
        (list): list consists of {1,2,3,4}
    """
    c2n_dict = {'A':1,'T':2,'G':3,'C':4}
    num_seq = list()
    for i, s_i in enumerate(sequence):
        num_seq.append(c2n_dict[s_i])
    return num_seq

def Aligment(X:str, Y: str):
    """
     Create a zero matrix and fills it by the recurrence relation
     Args:
        X (str):DNA sequence
        Y (str):DNA sequence
     Returns:
        M (np.ndarray)
        new_x (str)
        new_y (str)
    """
    m = len(X)
    n = len(Y)
    x = [0]
    y = [0]
    x = x + char2num(X)
    y = y + char2num(Y)
    M = np.zeros((m+1,n+1))

    gap_p = 0
    for i in range(m+1):
        gap_p += penalty_matrix[x[i]][0]
        M[i][0] = gap_p
    gap_p = 0
    for j in range(n+1):
        gap_p += penalty_matrix[0][y[j]]
        M[0][j] = gap_p
    for j in range(1,n+1):
        for i in range(1,m+1):
            ch1 = penalty_matrix[x[i]][y[j]] + M[i-1][j-1]
            ch2 = penalty_matrix[x[i]][0] + M[i-1][j]
            ch3 = penalty_matrix[0][y[j]] + M[i][j-1]
            M[i][j] = min(ch1, ch2, ch3)
    
    new_x = ''
    new_y = ''
    i, j = m, n
    while i and j:
        curr, diag, up, left = M[i][j], M[i-1][j-1], M[i-1][j], M[i][j-1]
        if curr == diag + penalty_matrix[x[i]][y[j]]:
            new_x = X[i-1] + new_x
            new_y = Y[j-1] + new_y
            i -= 1
            j -= 1
        elif curr == up + penalty_matrix[x[i]][0]:
            new_x = X[i-1] + new_x
            new_y = '-' + new_y
            i -= 1
        elif curr == left + penalty_matrix[0][y[j]]:
            new_x = '-' + new_x
            new_y = Y[j-1] + new_y
            j -= 1
    while i:
        new_x = X[i-1] + new_x
        new_y = '-' + new_y
        i -= 1
    while j:
        new_x = '-' + new_x
        new_y = Y[j-1] + new_y
        j -= 1
    return new_x,new_y,M

def Space_Efficient_Alignment(X:str, Y:str):
    m = len(X)
    n = len(Y)
    x = [0]
    y = [0]
    x = x + char2num(X)
    y = y + char2num(Y)
    B = np.zeros((m+1,2))
    gap_p = 0
    for i in range(m+1):
        gap_p += penalty_matrix[x[i]][0]
        B[i][0] = gap_p
    gap_p = 0
    for j in range(1,n+1):
        gap_p += penalty_matrix[0][y[j]]
        B[0][1] = gap_p
        for i in range(1,m+1):
            ch1 = penalty_matrix[x[i]][y[j]] + B[i-1][0]
            ch2 = penalty_matrix[x[i]][0] + B[i-1][1]
            ch3 = penalty_matrix[0][y[j]] + B[i][0]
            B[i][1] = min(ch1, ch2, ch3)
        B[:,0] = B[:,1]
    return B

def Backward_Space_Efficient_Alignment(X:str, Y:str):
    m = len(X)
    n = len(Y)
    x = [0]
    y = [0]
    x = char2num(X) + x
    y = char2num(Y) + y
    B = np.zeros((m+1,2))
    gap_p = 0
    for i in range(m+1):
        gap_p += penalty_matrix[x[m-i]][0]
        B[m - i][1] = gap_p
    gap_p = 0
    for j in range(1,n+1):
        gap_p += penalty_matrix[0][y[n-j]]
        B[m][0] = gap_p
        for i in range(1,m+1):
            ch1 = penalty_matrix[x[m-i+1]][y[n-j+1]] + B[m-i+1][1]
            ch2 = penalty_matrix[x[m - i]][0] + B[m-i+1][0]
            ch3 = penalty_matrix[0][y[n-j]] + B[m-i][1]
            B[m - i][0] = min(ch1, ch2, ch3)
        B[:,1] = B[:,0]
    return B

def Divide_and_Conquer_Alignment(X:str, Y:str):
    m = len(X)
    n = len(Y)
    #pdb.set_trace()
    if m <= 2 or n <= 2:
        return Aligment(X, Y)
    if n % 2 == 0:
        B1 = Space_Efficient_Alignment(X,Y[:n//2])
        B2 = Backward_Space_Efficient_Alignment(X,Y[n//2:])
        mid = Y[n//2]
    else:
        B1 = Space_Efficient_Alignment(X,Y[:(n+1)//2])
        B2 = Backward_Space_Efficient_Alignment(X,Y[(n+1)//2:])
        mid = Y[(n+1)//2]
    s = 100000000
    for q in range(m+1):
        if s > B1[q][1] + B2[q][0]:
            s = B1[q][1] + B2[q][0]
            index = q
    
    if n % 2 ==0:
        left = Divide_and_Conquer_Alignment(X[:index], Y[:n//2])
        right = Divide_and_Conquer_Alignment(X[index+1:], Y[n//2+1:])
    else:
        left = Divide_and_Conquer_Alignment(X[:index], Y[:(n+1)//2])
        right = Divide_and_Conquer_Alignment(X[index+1:], Y[(n+1)//2+1:])
    return left[0] + X[index] + right[0], left[1] + mid + right[1]

if __name__ == "__main__":
    X = 'ACGTGCTA'
    Y = 'ACGTACATA'
    x,y= Divide_and_Conquer_Alignment(X, Y)
    print(x)
    print(y)

 #   with open('Data-P2a.txt','r') as f:
 #       X = f.readline().strip('\n')
 #   with open('Data-P2b.txt','r') as f:
 #       Y = f.readline().strip('\n')
 #   
 #   m = len(X)
 #   n = len(Y)
 #   new_x, new_y, M = Aligment(X, Y)
 #   with open('Ali_Data-P2a.txt','w') as f:
 #       f.write(new_x)
 #   with open('Ali_Data-P2b.txt','w') as f:
 #       f.write(new_y)
 #   print(M[m][n])