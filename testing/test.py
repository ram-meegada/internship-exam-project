#fibonacci series 0,1,1,2,3,5,8,13,21,34
from datetime import datetime as dt
def fibb(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibb(n-1) + fibb(n-2)
n = 10
start_time = dt.now()
print(start_time)
for i in range(n):
    print(fibb(i))
end_time = dt.now()
print(end_time)
print(end_time-start_time)    