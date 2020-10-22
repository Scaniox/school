#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      suzie
#
# Created:     23/09/2017
# Copyright:   (c) suzie 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def factorial(n):
    if n == 0:
        return (1)
    else:
        prev = factorial (n-1)
        result = n * prev
        return (result)


n = 5
factorial(n)
print (factorial(n))