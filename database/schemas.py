def student_specific_data(students):
    return {
        "name": str(students["name"]),
        "age": int(students["age"])
    }

def student_all_data(students):
    return {
        "name": str(students["name"]),
        "age": int(students["age"]),
        "address": {
            "city": str(students["address"]["city"]),
            "country": str(students["address"]["country"])
        }
    }