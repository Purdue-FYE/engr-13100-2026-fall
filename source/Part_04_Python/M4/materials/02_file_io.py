"""
FILE INPUT/OUTPUT

File Input
- open() function - opens a file and returns a file object
    Syntax: open(file, mode)
    Example: f = open("hail_purdue.txt", "r")
    - read mode (default) - "r"
    - write mode - "w"
    - append mode - "a"
    - binary mode - "b"
    - read/write mode - "r+"
    - read/write binary mode - "rb+"
    - read/write append mode - "a+"
    - read/write append binary mode - "ab+"

- close() function - closes the file. Must be called after the file is opened.
    Syntax: f.close()

- with statement - automatically closes the file
    Syntax: with open(file, mode) as f:
                # code block

- read() method - reads the entire file
- readline() method - reads a single line from the file
- readlines() method - reads all the lines from the file

File Output
- write() method - writes a string to the file
- writelines() method - writes a list of strings to the file
"""

# File Input
# read mode (default)
# f = open("scripts_py4/hail_purdue.txt", "r")
# print(f)
# f.close()

# # write mode - creates a new file if it does not exist
# f = open("scripts_py4/hail_purdue.txt", "w")
# g = "ENGR 133"
# f.write(g)
# print(f)
# f.close()

# # append mode
# f = open("scripts_py4/hail_purdue.txt", "a")
# g = "- Srinivas Dustker"
# f.write(g)
# print(f)
# f.close()

# # with statement - read mode
# with open("scripts_py4/hail_purdue.txt", "r") as f:
# h = f.read()
# print(h)

# i = f.readline()
# i2 = f.readline()
# print(i)
# print(i2)

# j = f.readlines()
# print(j)

# k = f.read().strip().split()
# print(k)

# # with statement - append mode
# with open("scripts_py4/hail_purdue.txt", "a") as f:
#     g = "- Welcome to ENGR 133"
#     f.write(g)
#     print(g)
