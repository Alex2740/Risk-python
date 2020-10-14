import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from time import time
import os
os.chdir("G:\TIPE")

g11 = 5/12
g21 = 125/216
ga1 = 95/144
g32 = 1445/3888
g12 = 55/216
g22 = 295/1296

p22 = 581/1296
p32 = 2275/7776

def inv(n):
    return 1-n
        
def buildProb(n):
    res = np.zeros((n+1,n+1))
    
    for i in range(1,n+1):
        res[i,0] = 1
        
    res[1,1] = g11
    
    if (n > 1):
        res[2,1] = g21 + inv(g21)*res[1,1]
    
    for a in range(3,n+1):
        res[a,1] = ga1 + inv(ga1)*res[a-1,1]
        
    for d in range(2,n+1):
        res[1,d] = g12*res[1,d-1]
        res[2,d] = g22*res[2,d-2]+inv(g22+p22)*res[1,d-1]
    
    for a in range(3,n+1):
        print("builb:",a)
        for d in range(2,n+1):
            res[a,d] = g32*res[a,d-2]+inv(g32+p32)*res[a-1,d-1]+p32*res[a-2,d]
    
    return res
    
def saveProb():
    n = 500
    probs = buildProb(n)
    
    name = "probabilité de gagner une attaque.txt"
    fl = open(name,'w')

    for i in range(n+1):
        print("write: ",i)
        ligne = str(probs[i,0])
        for j in range(1,n+1):
            ligne += "|" + str(probs[i,j])
        fl.write(ligne + "\n")
    fl.close()
    
    
def showProb(n):
    fl = open('probabilité de gagner une attaque.txt','r')
    res = np.zeros((n+1,n+1))
    for i in range(n+1):
        ligne = fl.readline().strip().split('|')
        lg = np.array([float(each) for each in ligne][0:n+1])
        res[i] = lg
    fl.close()
    
    plt.close()
    plt.figure(figsize = (7,7))
    plt.imshow(res[1:,1:],extent=[0,n,0,n],origin="lower",interpolation='nearest',cmap=cm.jet)
    plt.colorbar()
    #plt.title("Probabilité de gagner", fontsize=20)
    plt.xlabel("Nombre de troupes qui défendent", fontsize=15)
    plt.ylabel("Nombre de troupes qui attaquent", fontsize=15)
    #plt.plot([0,n], [0,852*n/1000], 'b--')
    plt.savefig("probabilité de gagner une attaque.png")
    #plt.show()