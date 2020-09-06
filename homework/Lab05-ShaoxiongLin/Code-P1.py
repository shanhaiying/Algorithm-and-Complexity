import numpy as np

def DP():
    lines = list() #存储txt文件每一行内容
    thick = list() #存储每本书的厚度
    width = list() #存储每本书的宽度
    sum_t = 0 #累加所有书的厚度
    MIN = 100000000 #一个大的常量
    #读取文件内容
    with open('Data-P1.txt','r') as f:
        for line in f.readlines():
            lines.append(line.strip('\n'))
    #获取书本数目，每本书的厚度和宽度
    for i,book_i in enumerate(lines):
        if i == 0: #第一行是是书本数目
            num_books = int(book_i)
            thick.append(0)
            width.append(0)
        else: #接下来是每本书的厚度和宽度
            t_i, w_i = book_i.split(' ')
            thick.append(int(t_i))
            width.append(int(w_i))
            sum_t += int(t_i)

    M = np.ones((num_books+1,sum_t+1),dtype=int) #备忘录矩阵
    M *= MIN
    M[0][0] = 0

    total = 0
    for i in range(1,num_books+1): #填写M矩阵
        total += thick[i] #放i本书最大的可能厚度
        for j in range(total+1): #j应该小于这个最大可能厚度
            M[i][j] = M[i-1][j] + width[i] #表示第i本书横着放
            if j >= thick[i]: #如果可以竖着放
                M[i][j] = min(M[i][j],M[i-1][j-thick[i]])

    for i in range(sum_t+1): #寻找最小的能够使得竖着放厚度(根据OPT(i,j)定义即i)
        if i >= M[num_books][i]: #大于等于横着放宽度(即M[num_books][i])的厚度(i)
            print(i)
            break

if __name__ == "__main__":
    DP()