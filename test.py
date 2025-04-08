city_map = {}
city_map['A'] = ['B','C','D']
print(city_map)
'D' in city_map['A'] and city_map['A'].remove('D')
print(city_map)
city_map['A'].append('D')
print(city_map)

for i in range(10):
    if i % 2 == 0:  
        continue   # skip to the next iterations
    print(i, end=" ")
print()     