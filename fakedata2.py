from faker import Faker


class CreateFaker:
    def __init__(self, locale='zh_CN') -> None:
        """Init a Faker module.

        Args:
            locale (str, optional): [description]. Defaults to 'zh_CN'.
        """

        self.faker = Faker(locale=locale)
        self.content = {}

    def __str__(self) -> str:
        if self.content.values():
            pass

    def name(self) -> tuple:
        """Create a series of names.

        Returns:
            tuple: [names]
        """

        namelist = []
        num = int(input('请输入要生成的名字数量:'))
        for _ in range(num):
            namelist.append(self.faker.name())

        
        return tuple(namelist)



if __name__ == "__main__":
    cf = CreateFaker()
    names = cf.name()
    print(names)

