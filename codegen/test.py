from classes import *
from z3 import Int, Solver, sat
solver = Solver()
x = Int('x')
o = [1,2,3,4]
print(o[::-1])
solver.add(x == 7)
solver.add(x + 6 > 10, x<20)
if solver.check() != sat:
     print("nok")
else:
    print("ok")

if solver.check() != sat:
     print("nok")
else:
    print("ok")
