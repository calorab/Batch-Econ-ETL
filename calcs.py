import numpy as np

# Array Creation:
#  Creating an array from a standard python list:
a = np.array([1,2,3,4,5,6])
# array() transforms sequences into arrays ie the below is the same as the above
b = np.array(1,2,3,4,5,6)
#  The type can be explicitly specified at the time of creation by passing ain a possible 2nd arg
c = np.array([[1, 2], [3, 4]], dtype=complex)
#  growing an array is costly so it is better to use zeros(), ones() or empty() when creating an array since you know the (total)"size"
d = np.zeros((3,4)) # this shape has a "length" of 3 with 4 elements in each segment
#  arange() can be used to create a sequence of numbers and can use floats
e = np.arange(1,10,.5) # this will give an array of numbers between 1 and 10 (not including 10) AND WIL INCREMENT BY .5
#  To get a specific number of elememts you should use linspace() which specifies how many elements you want rather than incrementing 
f = np.linspace(0,2,9)
#  other methods used are sum() which sums the elements in an ndarray and min()/max()
fsum = f.sum()
# you can specify the axis to use if you don't want all elements summed
# the below will give a cumulative sum for row (axis=0 would give cumulative for columns)
g = c.cumsum(axis=1)
#  universal functions: sin() cos() exp() sqrt() and they won; element-wise
# arrays can be sliced just like lists when one dimension, and when 2 dimensions they use 1 index per dimension (ie [2,3] row 3 and column 4)
# c[0:5, 1] = rows 1 thru 5, the second column and equals [:,1] IF there are 5 rows ( or a shape of (2 or more,5))
# iterating over the ndarray should be done using the flat attribute:
for element in c.flat:
    print(element)
# iterating over a multidimensional array is done with respect to the first axes:
for row in b:
    print(row)
