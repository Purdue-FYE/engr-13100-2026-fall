"""
Lists vs. Arrays:
A list is a collection of elements of different types stored in non-contiguous memory locations,
An array is a collection of elements of the same type stored in contiguous memory locations.

List manipulation:
    For a mutable sequence m, index i, iterable object t, and arbitrary object x:
    - m[i] = x replaces the element at index i with x
    - m.append(x) adds x to the end of the list
    - m.insert(i, x) inserts x at index i
    - m.remove(x) removes the first occurrence of x
    - m.pop(i) removes the element at index i
    - m.clear() removes all elements
    - m.extend(t) adds the elements of t to the end of the list
    - m += t adds the elements of t to the end of the list
    - m *= n repeats the list n times
    - m.reverse() reverses the list
    - m.sort() sorts the list
    - m.copy() returns a shallow copy of the list
    - m.index(x) returns the index of the first occurrence of x
    - m.count(x) returns the number of occurrences of x
    - m.clear() removes all elements
    - len(m) returns the number of elements in m
    - min(m) returns the smallest element in m
    - max(m) returns the largest element in m
    - sum(m) returns the sum of elements in m
    - sorted(m) returns a new sorted list

Indexing and Slicing:
    - m[i] returns the element at index i
    - m[i:j] returns the elements from index i to j-1
    - m[i:j:k] returns the elements from index i to j-1 with step k
    - m[-i] returns the element at index -i
    - m[-i:] returns the elements from index -i to the end of the list
    - m[:-i] returns the elements from the beginning of the list to index -i
    - m[::-1] returns the elements in reverse order

Indexing and Slicing excercise:

s = "Hello World, Hail Purdue!"
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13| 14| 15| 16| 17| 18| 19| 20| 21| 22| 23| 24|
| H | e | l | l | o |   | W | o | r | l | d | , |   | H | a | i | l |   | P | u | r | d | u | e | ! |
|-25|-24|-23|-22|-21|-20|-19|-18|-17|-16|-15|-14|-13|-12|-11|-10| -9| -8| -7| -6| -5| -4| -3| -2| -1|

s[0] = 'H'
s[18:24] = 'Purdue' or s[-7:-1] = 'Purdue'
s[0:5] = 'Hello' or s[:5] = 'Hello'
s[-1] = '!' or s[24] = '!' or s[-1:] = '!' or s[24:] = '!' or s[len(s)-1] = '!' or s[-1:len(s)] = '!'
s[:-1] = 'Hello World, Hail Purdue' or s[:24] = 'Hello World, Hail Purdue'
s[::-1] = '!eudruP liaH ,dlroW olleH' or s[-1:-26:-1] = '!eudruP liaH ,dlroW olleH'

Arrays: A collection of elements of the same type stored in contiguous memory locations.

Documentation: https://numpy.org/doc/stable/reference/index.html

1. One-dimensional array: A collection of elements of the same type stored in a single row.
Syntax:
    array_name = [element1, element2, element3, ..., elementN]

2. Two-dimensional array: A collection of elements of the same type stored in multiple rows and columns.
Syntax:
    array_name = [[element1, element2, element3, ..., elementN],
                  [element1, element2, element3, ..., elementN],
                  [element1, element2, element3, ..., elementN]]

3. Multi-dimensional array: A collection of elements of the same type stored in multiple rows, columns, and depth.
Syntax:
    array_name = [[[element1, element2, element3, ..., elementN],
                   [element1, element2, element3, ..., elementN],
                   [element1, element2, element3, ..., elementN]],
                  [[element1, element2, element3, ..., elementN],
                   [element1, element2, element3, ..., elementN],
                   [element1, element2, element3, ..., elementN]]]

4. Accessing elements in an array:
    - One-dimensional array: array_name[index]
    - Two-dimensional array: array_name[row][column]
    - Multi-dimensional array: array_name[depth][row][column]

Arrays using NumPy:
1. Creating an array using NumPy:
    - Import the NumPy library as np.
    - Create an array using the np.array() function.
    - Access elements in the array using indexing.
    Syntax:
        import numpy as np
        array_name = np.array([element1, element2, element3, ..., elementN])

2. Accessing elements in a NumPy array:
    - array_name[index]
    - array_name[row][column]
    - array_name[depth][row][column]

3. NumPy array attributes:
    - shape: Returns the dimensions of the array.
    - size: Returns the total number of elements in the array.
    - ndim: Returns the number of dimensions of the array.
    - dtype: Returns the data type of the elements in the array.

4. NumPy array functions:
    - np.zeros(shape): Creates an array of zeros with the specified shape.
    - np.ones(shape): Creates an array of ones with the specified shape.
    - np.full(shape, value): Creates an array of the specified shape filled with
      the specified value.
    - np.arange(start, stop, step): Creates an array with a range of values from
      start to stop with the specified step.
    - np.linspace(start, stop, num): Creates an array with a range of values
      from start to stop with the specified number of elements.
    - np.random.rand(shape): Creates an array of random values with the
      specified shape.
    - np.reshape(array, new_shape): Reshapes the array to the specified new
      shape.
    - np.transpose(array): Transposes the array.
    - np.concatenate((array1, array2), axis): Concatenates two arrays along the
      specified axis.
    - np.vstack((array1, array2)): Stacks arrays vertically.
    - np.hstack((array1, array2)): Stacks arrays horizontally.
    - np.split(array, indices_or_sections): Splits the array into multiple
      sub-arrays.
    - np.max(array): Returns the maximum value in the array.
    - np.min(array): Returns the minimum value in the array.
    - np.mean(array): Returns the mean of the values in the array.
    - np.median(array): Returns the median of the values in the array.

5. NumPy array operations:
    - Element-wise operations: Perform operations on corresponding elements of two arrays.
    - Broadcasting: Perform operations on arrays of different shapes by
      broadcasting the smaller array to match the larger array's shape.
    - Dot product: Perform matrix multiplication using the dot() function.

"""

"""

# List manipulation
m = [1, 2, 3, 4, 5]
m[0] = 0
print(m)  # Output: [0, 2, 3, 4, 5]

m.append(6)
print(m)  # Output: [0, 2, 3, 4, 5, 6]

m.insert(1, 1)
print(m)  # Output: [0, 1, 2, 3, 4, 5, 6]

m.remove(1)
print(m)  # Output: [0, 2, 3, 4, 5, 6]

m.pop(1)
print(m)  # Output: [0, 3, 4, 5, 6]

m.clear()
print(m)  # Output: []

m.extend([1, 2, 3, 4, 5])
print(m)  # Output: [1, 2, 3, 4, 5]

m += [6, 7, 8, 9, 10]
print(m)  # Output: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

m *= 2
print(m)  # Output: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

m.reverse()
print(m)  # Output: [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

m.sort()
print(m)  # Output: [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]

n = m.copy()
print(n)  # Output: [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]

print(m.index(5))  # Output: 8

print(m.count(5))  # Output: 2

m.clear()
print(m)  # Output: []

# len(m) returns the number of elements in m
m = [1, 2, 3, 4, 5]
print(len(m))  # Output: 5

# min(m) returns the smallest element in m
print(min(m))  # Output: 1

# max(m) returns the largest element in m
print(max(m))  # Output: 5

# sum(m) returns the sum of elements in m
print(sum(m))  # Output: 15

# sorted(m) returns a new sorted list
print(sorted(m))  # Output: [1, 2, 3, 4, 5]

# List Indexing and Slicing
m = [1, 2, 3, 4, 5]
print(m[0])  # Output: 1
print(m[1:3])  # Output: [2, 3]
print(m[1:4:2])  # Output: [2, 4]
print(m[-1])  # Output: 5
print(m[-2:])  # Output: [4, 5]
print(m[:-2])  # Output: [1, 2, 3]
print(m[::-1])  # Output: [5, 4, 3, 2, 1]

# Arrays using NumPy
import numpy as np

# One-dimensional array
array1 = np.array([1, 2, 3, 4, 5])
print(array1[0])  # Output: 1

# Multi-dimensional array (Two-dimensional array)
array2 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(array2[0][0])  # Output: 1

# Multi-dimensional array (Three-dimensional array)
array3 = np.array(
    [
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
        [[19, 20, 21], [22, 23, 24], [25, 26, 27]],
    ]
)

print(array3[0][0][0])  # Output: 1
print(array3[1][1][1])  # Output: 14
print(array3[1][2][2])  # Output: 18
print(array3[2][2][2])  # Output: 27
print(array3[0][1][2])  # Output: 6

# NumPy array functions
array_zeros = np.zeros((2, 3))
print(array_zeros)  # Output: [[0. 0. 0.]    [0. 0. 0.]]

array_ones = np.ones((3, 2))
print(array_ones)  # Output: [[1. 1.]    [1. 1.]    [1. 1.]]

array_full = np.full((2, 2), 5)
print(array_full)  # Output: [[5 5]  [5 5]]

array_arange = np.arange(0, 10, 2)
print(array_arange)  # Output: [0 2 4 6 8]

array_linspace = np.linspace(0, 10, 5)
print(array_linspace)  # Output: [ 0.   2.5  5.   7.5 10. ]

array_rand = np.random.rand(2, 3)
print(
    array_rand
)  # Output: [[0.12345678 0.23456789 0.3456789 ]    [0.45678901 0.56789012 0.67890123]]

array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(np.reshape(array, (1, 9)))  # Output: [[1 2 3 4 5 6 7 8 9]]
print(np.transpose(array))  # Output: [[1 4 7]    [2 5 8]    [3 6 9]]

array1 = np.array([[1, 2], [3, 4]])
array2 = np.array([[5, 6], [7, 8]])
print(
    np.concatenate((array1, array2), axis=0)
)  # Output: [[1 2]    [3 4]    [5 6]    [7 8]]
print(np.concatenate((array1, array2), axis=1))  # Output: [[1 2 5 6]    [3 4 7 8]]
print(np.vstack((array1, array2)))  # Output: [[1 2]    [3 4]    [5 6]    [7 8]]
print(np.hstack((array1, array2)))  # Output: [[1 2 5 6]    [3 4 7 8]]

array = np.array([1, 2, 3, 4, 5, 6])
print(np.split(array, 3))  # Output: [array([1, 2]), array([3, 4]), array([5, 6])]
print(np.split(array, [2, 4]))  # Output: [array([1, 2]), array([3, 4]), array([5, 6])]
print(
    np.split(array, [2, 3, 5])
)  # Output: [array([1, 2]), array([3]), array([4, 5]), array([6])]
print(
    np.split(array, [1, 3, 5])
)  # Output: [array([1]), array([2, 3]), array([4, 5]), array([6])]

array = np.array([1, 2, 3, 4, 5])
print(np.max(array))  # Output: 5
print(np.min(array))  # Output: 1
print(np.mean(array))  # Output: 3.0
print(np.median(array))  # Output: 3.0

# NumPy array attributes
array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(array.shape)  # Output: (3, 3)
print(array.size)  # Output: 9
print(array.ndim)  # Output: 2
print(array.dtype)  # Output: int64

# Element-wise operations, Broadcasting, and Dot product
array1 = np.array([1, 2, 3])
array2 = np.array([4, 5, 6])

# Element-wise operations
print(array1 + array2)  # Output: [5 7 9]

# Broadcasting
array3 = np.array([[1, 2, 3], [4, 5, 6]])
array4 = np.array([1, 2, 3])
print(array3 + array4)  # Output: [[2 4 6]    [5 7 9]]

# Dot product (Matrix multiplication)
array5 = np.array([[1, 2], [3, 4]])
array6 = np.array([[5, 6], [7, 8]])
print(np.dot(array5, array6))  # Output: [[19 22]    [43 50]]
"""
