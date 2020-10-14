from sympy import *

def PrYj(y):
    if (1<=y<=6):
        return Rational(1,6)
    else:
        return 0
        
def PrY12(y1,y2):
    if (y1 == y2):
        return Rational(3*y1-2,216)
    if (y1 > y2):
        return Rational(6*y2-3,216)
    else:
        return 0
        
def PrY1(y1):
    if (1<=y1<=6):
        return Rational(1-3*y1+3*(y1**2),216)
    else:
        return 0

def PrZ12(z1,z2):
    if (z1 == z2):
        return Rational(1,36)
    if (z1 > z2):
        return Rational(2,36)
    else:
        return 0
        
def PrZ1(z1):
    if (1<=z1<=6):
        return Rational(2*z1-1,36)
    else:
        return 0
        
def PrW12(w1,w2):
    return PrZ12(w1,w2)
    
def PrW1(w1):
    return PrZ1(w1)
    
## Calcul des probas
# Victoire 1-1 : 111
res = 0
for z in range(1,5 +1):
    for y in range(z+1,6 +1):
                res += PrYj(y)*PrYj(z)
                
print('Victoire 1-1 :',res,'-',res.evalf())

# Victoire 2-1 : 211
res = 0
for z in range(1,5 +1):
    for y in range(z+1,6 +1):
                res += PrW1(y)*PrYj(z)
                
print('Victoire 2-1 :',res,'-',res.evalf())

# Victoire 3-1 : 311
res = 0
for z in range(1,5 +1):
    for y in range(z+1,6 +1):
                res += PrY1(y)*PrYj(z)
                
print('Victoire 3-1 :',res,'-',res.evalf())

# Victoire 1-2 : 121
res = 0
for z in range(1,5 +1):
    for y in range(z+1,6 +1):
                res += PrYj(y)*PrW1(z)
                
print('Victoire 1-2 :',res,'-',res.evalf())

# Victoire 2-2 : 222
res = 0
for z1 in range(1,5 +1):
    for z2 in range(1,z1 +1):
        for w1 in range(z1+1,6+1):
            for w2 in range(z2+1,w1+1):
                res += PrW12(w1,w2)*PrZ12(z1,z2)
                
print('Victoire 2-2 :',res,'-',res.evalf())

# Défaite 2-2 : 220
res = 0
for w1 in range(1,6 +1):
    for w2 in range(1,w1 +1):
        for z1 in range(w1,6+1):
            for z2 in range(w2,z1+1):
                res += PrW12(w1,w2)*PrZ12(z1,z2)
                
print('Défaite 2-2 :',res,'-',res.evalf())

# Victoire 3-2 : 322
res = 0
for z1 in range(1,5 +1):
    for z2 in range(1,z1 +1):
        for y1 in range(z1+1,6+1):
            for y2 in range(z2+1,y1+1):
                res += PrY12(y1,y2)*PrZ12(z1,z2)
                
print('Victoire 3-2 :',res,'-',res.evalf())

# Défaite 3-2 : 320
res = 0
for y1 in range(1,6 +1):
    for y2 in range(1,y1 +1):
        for z1 in range(y1,6+1):
            for z2 in range(y2,z1+1):
                res += PrY12(y1,y2)*PrZ12(z1,z2)
                
print('Défaite 3-2 :',res,'-',res.evalf())