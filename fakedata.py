# -*- encoding: utf-8 -*-
'''
@File    :   fakedata.py
@Time    :   2021/09/13 15:30:00
@Author  :   Jimmy Yu
@Version :   0.3
@Contact :   haozijimmy@hotmail.com
'''


from faker import Faker
from pandas import DataFrame
import sys
import csv
from openpyxl import Workbook


class CreateFaker:

    #-----内置方法-----#

    def __init__(self, locale='zh_CN') -> None:
        """Init a Faker object.

        Args:
            locale (str, optional): [description]. Defaults to 'zh_CN'.

        self.content:
            {class: (faker1, faker2, faker3, ...),
            class2: (faker1, faker2, faker3, ...),
            ...}
        """

        self.faker = Faker(locale=locale)
        self.content = {}

    def __str__(self) -> str:
        if len(self.content.keys()) == 0:
            return None
        else:
            return str(tuple(self.content.values()))

    #-----生成假数据-----#

    def name(self) -> tuple:
        """Create a series of names.

        Returns:
            tuple: [names]
        """

        _namelist = []
        num = int(input('请输入要生成的名字数量:'))
        # 生成num个name
        for _ in range(num):
            _namelist.append(self.faker.name())

        names = tuple(_namelist)

        # 传入类名和名字元组
        self._add(sys._getframe().f_code.co_name, names)

        return names

    #-----内置操作-----#

    def _add(self, name, data) -> None:
        __name = name
        if self.content.get(name):
            while self.content.get(__name):
                # 如果类别后面带数字，则提取数字，为数字+1
                if name[len(name):]:
                    __num = name[len(name):]
                    __num += 1
                else:
                    __num = 1
                __name = name + str(__num)
        # 将生成的数据添加进字典中
        self.content[__name] = data

    def to_csv(self, path='./fakedata.csv', encoding='utf-8'):
        __fieldnames = list(self.content.keys())
        with open(path, 'w', encoding=encoding) as f:
            __writer = csv.DictWriter(f, fieldnames=__fieldnames)
            __writer.writeheader()
            __writer.writerows(self.content)

    def to_xlsx(self, path='./fakedata.xlsx'):
        __wb = Workbook()
        __ws = __wb.active
        __header = tuple(self.content.keys())
        __data = tuple(self.content.values())
        __ws.append(__header)
        for __row in __data:
            __ws.append(__row)
        __wb.save(path)


    def save(self, type='csv', path='', encoding='utf-8'):
        # csv/xlsx/txt/df
        if path:
            __path = path
        else:
            # 如果要生成df，不需要路径
            if type == 'df':
                pass
            __path = '{}fakedata.{}'.format()
        if type=='csv':
            self.to_csv(path=__path, encoding=encoding)
        if type=='xlsx':
            self.to_xlsx(path=__path)
        if type=='txt':
            pass
        if type=='df':
            pass



if __name__ == "__main__":
    cf = CreateFaker()
    names = cf.name()
    names = cf.name()
    print(cf.content)
    print(cf)
