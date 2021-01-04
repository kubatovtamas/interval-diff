# Interval and Auto-Diff calculator
Python script for interval arithmetic problems, and auto-differentiating equations, with detailed steps shown.

## Usage
main.py has the two modules imported. Example usage can be seen in main().

### Intervals
Create new Interval objects, evaluating can be done using standard operators.
Interval objects are min - max interval pairs.
```Python
# [1, 4] + [-1, 2] / [-5, -1] - [-2, 1]
i1 = Interval([1, 4])
i2 = Interval([-1, 2])
i3 = Interval([-5, -1])
i4 = Interval([-2, 1])

i1 + i2 / i3 - i4
```


### Differentials
Create new Differential objects, evaluating can be done using standard operators.
Differential objects are function value - derivative value pairs.
```Python
# log(x) * (x^2 + 2x + 4), x = 3
x = Differential([3, 1]) # Variable
c = Differential([4, 0]) # Constant

x.log() * (x**2 + 2*x + c)
```
