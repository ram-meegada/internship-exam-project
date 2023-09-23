def find(paths):
    d = {}
    for i,j in paths:
        d[i] = j
    for i,j in d.items():
        try:
            if d[j]:
                pass
        except:
            pass    
paths = [["London","New York"],["New York","Lima"],["Lima","Sao Paulo"]]
print(find(paths))