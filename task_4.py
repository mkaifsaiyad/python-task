input_numbers = [ num for num in range(1, 1001) ]

list1 = [ num for num in input_numbers if num%2 == 0 ]

list2 = [ num for num in input_numbers if num%17 == 0]

user_num = int(input("Would you please provide number for filtering: "))

list3 = [ num for num in input_numbers if num > user_num ]

print(list1)
print(list2)
print(list3)
