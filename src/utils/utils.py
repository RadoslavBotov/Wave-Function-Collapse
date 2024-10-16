import math

def nsa(number):
    n = math.floor(math.sqrt(number))

    if (math.sqrt(number) - n == 0):
        return number
    
    return (n+1)*(n+1)

def nsba(number):
    n = math.floor(math.sqrt(number))

    if (math.sqrt(number) - n == 0):
        return n
    
    return n+1

#for i in range(20):
#    print(i,' => ',nearest_square_base_above(i))