

def str_arr_to_dic(str_arr):
    dic = {}
    for index,name in enumerate(str_arr):
        dic[index] = name
    return dic

if __name__ == "__main__" :
    data = ["Kaif", "Vineet", "Dipali", "Krunal", "Pranjal","Kishan", "Jainil", "User"]
    result = str_arr_to_dic(data)
    print(f"converted output: \n{result}")