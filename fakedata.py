from faker import Faker


class CreateFaker:
    def __init__(self, locale='zh_CN') -> None:
        self.faker = Faker(locale=locale)

    def name(self):
        namelist = []
        num = int(input('请输入要生成的名字数量:'))
        for _ in range(num):
            namelist.append(self.faker.name())
        return tuple(namelist)


def output(path='./', type='csv'):
    pass


if __name__ == "__main__":
    cf = CreateFaker()
    names = cf.name()
    print(names)
