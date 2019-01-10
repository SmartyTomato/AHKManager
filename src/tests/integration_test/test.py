class item():
    def __init__(self):
        self.num = 1


class student():
    def __init__(self, name='', age=0):
        self.name = name
        self.age = age
        self.items = [item()]


def change_age(s3):
    s3.age = 1000
    for item in s3.items:
        item.num = 1000


s = student('Tommy', 25)
s2 = student('aaron', 15)

change_age(s)
# for st in s_list:
# change_age(st)

# print(s.age)
# print(s.items[0].num)

i = next((x.num for x in s.items) , None)
