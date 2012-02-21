#N = 9

# Linear interpolation between two numbers
def interpolate(x, y, N):
    return [(x + float(i*(y-x))/(N+1)) for i in range(N+1)]

# Linear interpolation within a list
def interpolate_list(list, N):
    ans = []
    for ele in list:
        try:
            for x in interpolate(prev, ele, N):
                ans.append(x)
        except:
            prev = ele
        prev = ele
    ans.append(list[-1])
    return ans

# Linear interpolation between two lists
def interpolate_2lists(x, y, N):
    return [[interpolate(x[i], y[i], N)[j] for i in range(len(x))] for j in range(N+1)]

# Linear interpolation in a 2d array
def interpolate_array(a, N):
    ans = []
    expanded_rows = []
    for row in a:
        expanded_rows.append(interpolate_list(row, N))
    for row in expanded_rows:
        try:
            for ele in interpolate_2lists(prev, row, N):
                ans.append(ele)
        except:
            prev = row
        prev = row
    ans.append(interpolate_list(a[-1], N))
    return ans

#print interpolate(1, 2, N)
#print interpolate_list([0.5, 0.7, 1.0], N)
#print interpolate_2lists([0.5, 0.7, 1.0], [0.6, 0.8, 1.1], N)
#a = interpolate_array([(0.5, 0.7, 1.0), (0.6, 0.8, 1.1), (0.8, 0.9, 1.2)], N)
#for row in a:
#    print row
