"""
    Take input from the user in the format [name:age], Then
    display oldest and youngest person and group by 18-35, 36-50, 51-65, and 66-90
"""

def get_person():
    print("Provide name and age in the format [name:age] age in the range 18-90: ")
    input_person_dic = {}

    user_input = input("Enter name and age (type 'exit' for stop): ")

    while user_input.lower() != 'exit':
        [name, age] = user_input.split(":")
        age = int(age)
        if 18 <= age <= 90:
            input_person_dic[name] = int(age)
        else:
            print("Invalid age!, Enter age in the range 18-90")
        user_input = input("Enter another name and age (type 'exit' for stop): ")


    return input_person_dic

# def sort_person_by_age(dic):
#     return dict(sorted(dic.items(), key = lambda person : person[1]))

def get_youngest_oldest_person_by_group (dic):
    grouped_dic = {"18-35":[], "36-50":[], "51-65":[], "66-90":[]}
    for person in dic.items():
        person_age = person[1]
        if 18 <= person_age <= 35:
            grouped_dic["18-35"].append(person)
        elif 36 <= person_age <= 50:
            grouped_dic["36-50"].append(person)
        elif 51 <= person_age <= 65:
            grouped_dic["51-65"].append(person)
        elif 66 <= person_age <=90:
            grouped_dic["66-90"].append(person)
        else:
            print(f"Age {person_age} is out of the range")
    youngest_oldest_group_wise = {}

    for age_group in grouped_dic.items():
        youngest_oldest_group_wise[age_group[0]] = {
            "youngest": min(age_group[1], key=lambda g : g[1]),
            "oldest": max(age_group[1], key=lambda g: g[1])
        }

    return youngest_oldest_group_wise

if __name__ == "__main__":
    person_dic = {
        "kaif": 21,
        "kaif23": 23,
        "kaif56": 56,
        "kaif48": 48,
        "kaif65": 65,
        "kaif90": 90,
        "kaif51": 51,
        "kaif66": 66,
        "kaif91": 91,
        "kaif17": 17
    }
    # sorted_person_dic = sort_person_by_age(person_dic)
    grouped_person_dic = get_youngest_oldest_person_by_group(person_dic)
    print("Group\tYoungest\t\tOldest")
    for group in grouped_person_dic.items():
        print(f"{group[0]}\t{group[1]["youngest"]}\t{group[1]["oldest"]}")