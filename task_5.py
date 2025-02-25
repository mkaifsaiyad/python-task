user_data = {
    "M112": {
        "name": "kaif",
        "lucky_number": 7,
        "hobbies": [""],
        "books": []
    },
    "M110": {
            "name": "kaif",
            "lucky_number": 7,
            "hobbies": [],
            "books": []
        },
    "M111": {
        "name": "kaif",
        "lucky_number": 7,
        "hobbies": ["hobbie1", "dancing"],
        "books": [{
            "name": "kalidash",
            "author": "mith"
        }]
    }
}

def get_member_id():
    return input("Enter memberId: ")

def add_user():
    m_id = get_member_id()
    if m_id not in user_data:
        print("Provide required details")
        name = input("Name: ")
        lucky_number = int(input("Lucky Number Preference: "))
        hobbies = []
        while True:
            user_input = input("Enter Hobbies [type 'done' to complete]: ").lower()
            if user_input == 'done':
                break
            hobbies.append(user_input)
        books = []
        print("Enter book detail in the format [book_name:author_name]: ")
        print("[type 'done' to complete]: ")
        while True:
            user_input = input("Enter book details: ")
            if user_input == 'done':
                break
            [book_name, author_name] = user_input.split(':')
            books.append({book_name, author_name})
        user_data[m_id] = { "name": name, "lucky_number": lucky_number, "hobbies": hobbies, "books":books }

        return True
    else:
        print(user_data[m_id])
        return False

# def create_user(member_id, name, lucky_number, hobbies, books):
#     user_data[member_id] = { name, lucky_number, hobbies, books}

def delete_user(member_id):
    if member_id in user_data:
        del user_data[member_id]
    else:
        print("Member with specific id don't exist")

def search_user(member_id):
    return user_data.get(member_id)

if __name__ == "__main__":

    while True:
        print("\nSelect your task first: ")
        print("Type 'insert' for inserting a new record")
        print("Type 'delete' for deleting a new record")
        print("Type 'search' for searching a new record")
        print("Type 'done' for searching a new record")
        selection = input("Provide your preferred action: ").lower()
        if selection == 'insert':
            add_user()
        elif selection == 'delete':
            member_id = get_member_id()
            delete_user(member_id)
        elif selection == 'search':
            member_id = get_member_id()
            search_user(member_id)
            print(f"Details of user with id {member_id}\n{search_user(member_id)}")
        elif selection == 'done':
            exit(0)
        else:
            print(f"Provided action {selection} is not defined!, Select action from above")
