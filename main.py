import json
import random
import requests
from faker import Faker
from halo import *

fake = Faker()


def to_json(arr: list, flag: str):
    with open("./data/" + flag + ".json", "w", encoding='utf8') as j:
        json.dump(arr, j, ensure_ascii=False, indent=4)


def create_video_items(n, ch):
    arr = []

    for i in range(n):
        arr.append( {
            "vid_title": fake.job(),
            "chapter": ch,
            "url": fake.url()
        })
    to_json(arr, "videoitems")
    return arr


def create_chapters(n):
    arr = []
    for i in range(n):
        arr.append( {
            "title": f"Chapter {i + 1}",
            "estimatedHour": str(random.randint(10, 80)) + "hrs",
            "items": create_video_items(10, str(i + 1)),
        })
    to_json(arr, "chapters")
    return arr


def create_courses(n):
    arr = []
    for i in range(n):
        c = {
            "title": fake.job(),
            "estimatedHours": str(random.randint(10, 80)) + "hrs",
            "backDropPictureUrl": fake.file_path(extension='png'),
            "coverPictureUrl": fake.file_path(extension='png'),
            "instructor": fake.name(),
            "chapters": create_chapters(5),
            "price": str(random.randint(0, 500))
        }

        try:
            res = requests.post('http://localhost:5000/api/courses_instructor/', c)
        except:
            print('smt went wrong check express log')

        arr.append(c)
    to_json(arr, "courses")
    return arr


def create_users(n):
    arr = []
    for i in range(n):
        arr.append({
            "name": fake.name(),
            "sirname": fake.prefix(),
            "profilePictureUrl": fake.file_path(extension='png'),
            "password": fake.password(),
        })
    to_json(arr, "users")
    return arr


def create_instructors(n):
    arr = []
    for i in range(n):
        arr.append({
            "name": fake.name(),
            "sirname": fake.prefix(),
            "title": fake.job(),
            "profilePictureUrl": fake.file_path(extension='png'),
            "password": fake.password(),
        })
    to_json(arr, "instructors")
    return arr


def push_user():
    count = 0
    with open("./data/users.json", "r") as j:
        users = json.load(j)
        for user in users:
            try:
                requests.post('http://localhost:5000/api/user_signup', user)
                count += 1
            except:
                print('smt went wrong check express log')
    print("\n" + str(count) + ' users has been added')


def push_instructor():
    count = 0
    with open("./data/instructors.json", "r") as j:
        instructors = json.load(j)
        for instructor in instructors:
            try:
                res = requests.post('http://localhost:5000/api/instructor_signup', instructor)
                count += 1
            except:
                print('smt went wrong check express log')
    print("\n" + str(count) + ' instructors has been added')


def push_course():
    count = 0
    with open("./data/courses.json", "r") as j:
        courses = json.load(j)
        for course in courses:
            try:
                res = requests.post('http://localhost:5000/api/courses_instructor/', course)
                print(res.json())
                count += 1
            except:
                print('smt went wrong check express log')
    print("\n" + str(count) + ' courses has been added')


def push_chapter():
    count = 0
    with open("./data/chapters.json", "r") as j:
        chapters = json.load(j)
        for chapter in chapters:
            try:
                res = requests.post('http://localhost:5000/api/add_chapter', chapter)
                print(res.json())
                count += 1
            except:
                print('smt went wrong check express log')
    print("\n" + str(count) + ' chapters has been added')



def push_item():
    count = 0
    with open("./data/videoitems.json", "r") as j:
        items = json.load(j)
        for item in items:
            try:
                res = requests.post('http://localhost:5000/api/add_item', item)
                print(res.json())
                count += 1
            except:
                print('smt went wrong check express log')
    print("\n" + str(count) + ' items has been added')


if __name__ == "__main__":

    spinner = Halo(text='Generating dummy data :)', spinner='dots')
    spinner.start()
    create_instructors(5)
    create_users(5)
    create_courses(5)
    spinner.stop()

    spinner = Halo(text='Adding users', spinner='dots')
    spinner.start()
    push_user()
    spinner.stop()

    spinner = Halo(text='Adding instructors', spinner='dots')
    spinner.start()
    push_instructor()
    spinner.stop()

    spinner = Halo(text='Adding courses', spinner='dots')
    spinner.start()
    push_course()
    spinner.stop()

    spinner = Halo(text='Adding chapters', spinner='dots')
    spinner.start()
    push_chapter()
    spinner.stop()

    spinner = Halo(text='Adding video items', spinner='dots')
    spinner.start()
    push_item()
    spinner.stop()




