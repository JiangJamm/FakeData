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
import os


class CreateFaker:

    #-----内置方法-----#

    def __init__(self, locale='zh_CN') -> None:
        """Init a Faker object.

        Args:
            locale (str, optional): [description]. Defaults to 'zh_CN'.

        self.content:
            {class: (faker1, faker2, faker3, ...), 
            class2: (faker1, faker2, faker3, ...), 
            ...
            }
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
        __df = DataFrame(self.content)
        __df.to_csv(path, index=False, encoding=encoding)

    def to_xlsx(self, path='./fakedata.xlsx'):
        __df = DataFrame(self.content)
        __df.to_excel(path, index=False)

    def to_txt(self, path='./fakedata.xlsx', encoding='utf-8'):
        """保存为txt，以逗号为分隔符

        Args:
            path (str, optional): 文件路径，需要写清楚文件名和后缀. Defaults to './fakedata.xlsx'.
            encoding (str, optional): encoding. Defaults to 'utf-8'.
        """
        # 先保存为csv，然后再转为txt
        self.to_csv(path=path, encoding=encoding)
        os.rename(path, path[:-4]+'.txt')

    def to_DataFrame(self) -> DataFrame:
        # # 判断header有效性
        # if header:
        #     _header = header
        #     # 判断传入表头的长度是否与原数据相同
        #     if not len(_header) == len(self.content):
        #         raise FakerError('Length Error')

        # else:
        #     _header = list(self.content.keys())

        # 转换为DataFrame
        _df = DataFrame(self.content)

        # bug: 每列数据长度不同会报错，需要增加判断

        return _df

    def save(self, type='csv', path='', encoding='utf-8'):
        # csv/xlsx/txt
        if path:
            __path = path
        else:
            __path = '{}fakedata.{}'.format('./', type)

        if type == 'csv':
            self.to_csv(path=__path, encoding=encoding)
        if type == 'xlsx':
            self.to_xlsx(path=__path)
        if type == 'txt':
            self.to_txt(path=__path)

# 报错控制
class FakerError(ValueError):
    pass


if __name__ == "__main__":
    cf = CreateFaker()
    names = cf.name()
    names = cf.name()
    print(cf.content)
    print(cf)
    cf.save(type='txt')
