# -*- encoding: utf-8 -*-
'''
@File    :   fakedata_rebuild.py
@Time    :   2021/09/09 19:49:43
@Author  :   Jimmy Yu
@Version :   1.0
@Contact :   haozijimmy@hotmail.com
'''


from faker import Faker
from pandas import DataFrame
import sys


class _FakerBase:
    def __init__(self, locale='zh_CN') -> None:
        self.faker = Faker(locale=locale)

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

        self._add(sys._getframe().f_code.co_name, names)

        return names


class _Control:
    def __init__(self) -> None:
        self.content = {}

    #-----内置操作-----#

    def _add(self, name, c) -> None:
        __name = name
        if self.content.get(name):
            # 如果获取得到，则用字符串切片，提取已有后面的数字
            # 为数字+1，当做列名

            while self.content.get(__name):
                # 如果类别后面带数字
                if name[len(name):]:
                    __num = name[len(name):]
                    __num += 1
                else:
                    __num = 1
                __name = name + str(__num)
        # 将生成的数据添加进字典中
        self.content[__name] = c


class CreateFaker(_FakerBase, _Control):

    #-----内置方法-----#

    def __init__(self, locale='zh_CN') -> None:
        _FakerBase.__init__(self, locale)
        _Control.__init__(self)


    def __str__(self) -> str:
        if len(self.content.keys()) == 0:
            return None
        else:
            return str(tuple(self.content.values()))




if __name__ == "__main__":
    cf = CreateFaker()
    names = cf.name()
    names = cf.name()
    print(cf.content)
    print(cf)