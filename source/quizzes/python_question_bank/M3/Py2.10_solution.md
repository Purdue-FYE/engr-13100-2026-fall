## Py2.10 Loop Debugging (Solution)

### Part A – While Loop

You are given this piece of MATLAB code, which is meant to display numbers counting down from 10 to 1. As written, the loop will run indefinitely.

```python
n = 10

while n > 0:
    print(n)
end
```

1. Explain what causes this code to run forever.

        The loop runs forever because the condition is n > 0 and n is always greater than zero.

2. Write one line of code that should be added inside the loop to make it stop correctly.

    ```python
    n = n - 1
    ```

### Part B – For Loop

You are given the following MATLAB code, which produces an error when executed. The intended result of the program is 100, produced by iteratively adding each element of nums to result.

```python
nums = [10, 20, 30, 40]
result = 0

for n in nums:
    result = result + nums[n]
    print(result)
```

3. Explain why this code generates an error.

        Since nums only has 4 elements, nums(10) (and 20, 30, 40) the list index is out of range.

4. Modify the for loop initiation line so that the program executes correctly and computes the intended result.

    ```python
    for n in range(len(nums)):
    ```
