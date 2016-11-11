file = open('diodo.dat')
for line in file:
    if '#' in line: continue
    print(line.split(), sep=' & ', end='\\\\ \n')
