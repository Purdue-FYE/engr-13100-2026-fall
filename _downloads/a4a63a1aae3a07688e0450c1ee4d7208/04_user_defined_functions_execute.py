# # template
# def main():
#     # some code here

# if __name__ == "__main__":
#     main()  # call the main function

# Write a function that calculates how long an object will take to
# fall to the ground from a certain height.
# The formula to calculate the time taken for an object to fall is:
# time = sqrt(2 * height / g)
# where:
#       time - time taken for the object to fall
#       height - height from which the object is dropped
#       g - acceleration due to gravity (9.81 m/s^2)

# import math

# g = 9.81


# def calculate_time(height):  # parameter
#     time = math.sqrt(2 * height / g)
#     return time


# time = calculate_time(10)  # argument
# print(f"The object will take {time:.2f} seconds to fall to the ground")

# Write a function that calculates how long an object will take to
# fall to the ground from a certain height with a given initial speed.
# The formula to calculate the time taken for an object to fall is:
# time = -speed +- sqrt(speed^2 - 4 * (g/2) * height) / g
# where:
#       time - time taken for the object to fall
#       height - height from which the object is dropped
#       speed - initial speed of the object
#       g - acceleration due to gravity (9.81 m/s^2)


# def calculate_time(height, speed, g=9.81):  # multiple parameters
#     if g > 0:
#         g = -g

#     time1 = -speed + math.sqrt(speed**2 - 4 * (g / 2) * height) / g
#     time2 = -speed - math.sqrt(speed**2 - 4 * (g / 2) * height) / g

#     if time1 > 0:
#         time = time1
#     elif time2 > 0:
#         time = time2
#     else:
#         time = time1
#     return time


# h = 10
# s = 0
# x = calculate_time(h, s, g)  # multiple arguments
# print(f"The object will take {x:.2f} seconds to fall to the ground")


# Write a function that calculates how long an object will take to fall to the
# ground from a certain height.
# The formula to calculate the time taken for an object to fall is:
# time = sqrt(2 * height / g)
# where:
#       time - time taken for the object to fall
#       height - height from which the object is dropped
#       g - acceleration due to gravity (9.81 m/s^2)

# import math

# g = 9.81
# def calculate_time(height): # parameter
#     time = math.sqrt(2 * height / g)
#     return time

# time = calculate_time(10) # argument
# print(f"The object will take {time:.2f} seconds to fall to the ground")

# Write a function that calculates how long an object will take to fall to the
# ground from a certain height with a given initial speed.
# The formula to calculate the time taken for an object to fall is:
# time = -speed +- sqrt(speed^2 - 4 * (g/2) * height) / g
# where:
#       time - time taken for the object to fall
#       height - height from which the object is dropped
#       speed - initial speed of the object
#       g - acceleration due to gravity (9.81 m/s^2)

# import math

# def calculate_time(height, speed, g): # multiple parameters
#     if g > 0:
#         g = -g

#     time1 = -speed + math.sqrt(speed**2 - 4*(g/2) * height) / g
#     time2 = -speed - math.sqrt(speed**2 - 4*(g/2) * height) / g

#     if time1 > 0:
#         time = time1
#     elif time2 > 0:
#         time = time2
#     else:
#         time = time1
#     return time

# time = calculate_time(10, 0, 9.81) # multiple arguments
# print(f"The object will take {time:.2f} seconds to fall to the ground")
