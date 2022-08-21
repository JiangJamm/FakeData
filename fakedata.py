# -*- encoding: utf-8 -*-
'''
@File    :   fakedata.py
@Time    :   2022/08/21 21:00:00
@Author  :   Jimmy Yu
@Version :   0.6
@Contact :   haozijimmy@hotmail.com
'''


from typing import List, Optional
from warnings import warn
from faker import Faker
from pandas import DataFrame
import sys
import os


class CreateFaker:

    #-----内置方法-----#

    def __init__(self, locale='zh_CN') -> None:
        """
        Init a Faker object.

        ### Paraments:
            locale (str, optional): [description]. Defaults to 'zh_CN'.

        self.content:
            {class1: (faker1, faker2, faker3, ...), 
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

    def name(self, num: int) -> tuple:
        """
        Create a series of names.

        ### Paramers:
            num (int): 要生成的数量

        ### Returns:
            tuple ([names]): 返回num个名字组成的元组
        """

        _namelist = []
        # 生成num个name
        for _ in range(num):
            _namelist.append(self.faker.name())

        names = tuple(_namelist)

        # 传入类名和名字元组
        self._add_col(sys._getframe().f_code.co_name, names)

        return names

    #-----内置操作-----#

    def _add_col(self, name, data) -> None:
        '''
        添加一列数据
        '''
        # # 如果已经有数据，需要判断数据长度是否一致
        # if self.content:
        #     if self.is_same_len(data, self.content):
        #         pass
        #     else:
        #         msg = f'第{len(self.content)+1}列的长度与其他不一致，注意无法导出为DataFrame。'
        #         warn(message=msg)

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

    def is_same_len(self, addition: list, content: dict) -> bool:
        '''
        比较addition与content的长度。
        '''
        if len(content[list(content.keys())[0]]) == len(addition):
            return True
        return False

    def are_same_length(self, content: dict) -> bool:
        __check = set()
        for c in content:
            __check.add(len(content[c]))
        # 判断字典中每个值的列表长度是否相等，相等则返回True
        if len(__check) != 1:
            return False
        return True

    #-----保存方法-----#

    def to_csv(self, path='./fakedata.csv', encoding='utf-8'):
        '''
        Output to csv file. 逗号为分隔符。

        ### Paraments:
            path (str, optional): 文件路径，需要写清楚文件名和后缀. Defaults to './fakedata.csv'.
            encoding (str, optional): encoding. Defaults to 'utf-8'.
        '''
        __df = DataFrame(self.content)
        __df.to_csv(path, index=False, encoding=encoding)

    def to_xlsx(self, path='./fakedata.xlsx'):
        '''
        Output to Excel file.

        ### Paraments:
            path (str, optional): 文件路径，需要写清楚文件名和后缀. Defaults to './fakedata.xlsx'.
        '''
        __df = DataFrame(self.content)
        __df.to_excel(path, index=False)

    def to_txt(self, path='./fakedata.txt', encoding='utf-8'):
        """
        保存为txt，以逗号为分隔符。依赖于to_csv()。

        ### Paraments:
            path (str, optional): 文件路径，需要写清楚文件名和后缀. Defaults to './fakedata.txt'.
            encoding (str, optional): encoding. Defaults to 'utf-8'.
        """
        # 先保存为csv，然后再转为txt
        self.to_csv(path=path, encoding=encoding)
        os.rename(path, path[:-4]+'.txt')

    def to_DataFrame(self, header: List[str]) -> DataFrame:
        '''
        返回一个 DataFrame 对象。

        ### Paraments:
            header (List[str], must): 传入表头，必需。

        ### Return:
            DataFrame
        '''
        # feature: (P2)可以自己修改表头
        if self.are_same_length(self.content):
            pass
        else:
            raise FakerError('各列长度不同，无法导出为DataFrame格式。')

        # 判断header有效性
        if header:
            _header = header
            # 判断传入表头的长度是否与原数据相同
            if not len(_header) == len(self.content):
                raise FakerError('Header Length Error')
            else:
                _df = DataFrame(self.content)
                _df.columns = _header
        else:
            # 转换为DataFrame
            _df = DataFrame(self.content)

        return _df

    def save(self, filetype: str='csv', path: Optional[str]='', encoding: Optional[str]='utf-8'):
        '''
        保存为文件类型，默认为csv

        ### Paraments:
            filetype (str, optional): 文件类型，默认为csv。可选：csv/xlsx/txt。
            path (str, optional): 文件路径，需要写清楚文件名和后缀. Defaults to './fakedata.csv'.
            encoding (str, optional): encoding. Defaults to 'utf-8'.
        '''
        # csv/xlsx/txt
        if path:
            path = path
        else:
            path = '{}fakedata.{}'.format('./', filetype)

        if filetype == 'csv':
            self.to_csv(path=path, encoding=encoding)
        if filetype == 'xlsx':
            self.to_xlsx(path=path)
        if filetype == 'txt':
            self.to_txt(path=path)


# 报错控制
class FakerError(ValueError):
    pass


if __name__ == "__main__":
    cf = CreateFaker()
    names = cf.name(3)
    names = cf.name(5)
    # names = cf.name(7)
    print(cf.content)
    print(cf)
    header = ['name1', 'name2']
    df = cf.to_DataFrame(header=header)
    print(df)
