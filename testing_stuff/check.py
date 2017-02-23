from random import randint

rmax = randint(0,9)
print("This is the random number: %s" %rmax)




def is_bigger(eval,max):
    if (eval > max):
        return True
    else:
        return False

def is_smaller(eval,min):
    if (eval < min):
        return True
    else:
        return False

def is_bigger_random(eval):
    if (eval > rmax):
        return True
    else:
        return False
