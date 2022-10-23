""""
faker模块（作用：构造数据）

一、需求背景
写一个简单的构造数据的小工具，上传到pypi库。

二、实现思路
参照catcher库faker构造数据py文件进行二次改造。
源码不清楚及待实现点：
1、输入字符串型的int、float、list、tuple、dict参数构造的意义，为什么不直接使用函数直接转、ast处理的意义？
2、try_get_object 最外层return无返回值，未返回source，是否是bug
3、函数待重新构造：
- 使用类封装：
- 添加自定义可扩展方法
- 增加locale位置参数控制输出的数据格式

F.e. ::
    from faker.providers import BaseProvider

    class MyProvider(BaseProvider):
        def newfunc(self):
            return "my func"

"""

import hashlib
import json
import random
import sys
import datetime
import time
import pkgutil
import ast

from faker import Faker
from faker.providers import BaseProvider
from pydoc import locate
from types import ModuleType

random.seed()


class MyProvider(Faker, BaseProvider):

    def get_submodules_of(self, package: str):
        """
        Get all submodules and their importers for the package. It is not recursive.
        For recursive see __load_python_package_installed
        Package should be installed in the system.
        """
        modules = locate(package)
        return [(modname, importer) for importer, modname, ispkg
                in pkgutil.iter_modules(path=modules.__path__, prefix=modules.__name__ + '.')]

    @classmethod
    def eval_datetime(cls, astr, glob=None):
        if glob is None:
            glob = globals()
        try:
            tree = ast.parse(astr)
        except SyntaxError:
            raise ValueError(astr)
        print(ast.walk(tree))
        for node in ast.walk(tree):
            print(type(node))
            if isinstance(node, (ast.Module, ast.Expr, ast.Dict, ast.Str,
                                 ast.Attribute, ast.Num, ast.Name, ast.Load, ast.Tuple)): continue
            if (isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == 'datetime'): continue
            pass
        return eval(astr, glob)

    @classmethod
    def try_get_objects(cls, source: str or dict or list):
        got = MyProvider.try_get_object(source)  # "'[1,2,3]'" -> '[1,2,3]' -> [1,2,3]
        got = MyProvider.try_get_object(got)  # '[1,2,3]' -> [1,2,3]
        if isinstance(got, dict):
            return dict([(k, MyProvider.try_get_objects(v)) for k, v in got.items()])
        if isinstance(got, list):
            return [MyProvider.try_get_objects(v) for v in got]
        return got

    @classmethod
    def try_get_object(cls, source: str or dict or list):
        if isinstance(source, str):
            try:  # try python term '{key: "value"}'
                evaled = MyProvider.eval_datetime(source)
                if isinstance(evaled, ModuleType) or callable(evaled):  # for standalone 'string' var or 'id' bif
                    return source
                source = evaled
            except Exception:
                try:  # try json object '{"key" : "value"}'
                    source = json.loads(source)
                except ValueError:
                    return source
        return source

    def filter_astuple(self, param):
        """
        Convert data to tuple
        F.e. ::

            - postgres:
                request:
                  conf: '{{ postgres_conf }}'
                  query: "select status from my_table
                         where id in {{ [1, 2, 3] |astuple }}"

        :param param: data to convert
        """
        return tuple(MyProvider.try_get_objects(param))

    def filter_asint(self, param):
        """
        Convert data to int
        F.e. ::

            - postgres:
                request:
                  conf: '{{ postgres_conf }}'
                  query: "select status from my_table
                         where id == {{ my_str_var |asint }}"

        :param param: data to convert
        """
        return int(MyProvider.try_get_objects(param))

    def filter_asfloat(self, param):
        """
        Convert data to float
        F.e. ::

            - check: {equals: {the: 36.6, is: '{{ "36.6" | asfloat }}'}}

        :param param: data to convert
        """
        return float(MyProvider.try_get_objects(param))

    def filter_aslist(self, param):
        """
        Convert data to list
        F.e. ::

            - loop:
                foreach:
                    in: '{{ my_dictionary |aslist }}'
                    do:
                        echo: {from: '{{ ITEM.value }}', to: '{{ ITEM.key }}.output'}

        :param param: data to convert
        """
        return list(MyProvider.try_get_objects(param))

    def filter_asdict(self, param):
        """
        Convert data to dict
        F.e. ::

            - check: {equals: {the: [1, 2],
                               is: '{{ ([("one", 1), ("two", 2)] | asdict).values() |aslist }}'}}

        :param param: data to convert
        """
        return dict(MyProvider.try_get_objects(param))

    def filter_asstr(self, param):
        """
        Convert data to string
        F.e. ::

            - check: {equals: {the: '17', is: '{{ my_int | asstr }}'}}

        :param param: data to convert
        """
        return str(MyProvider.try_get_objects(param))

    def function_random(self, param_obj, locale=None):
        """
        Call `Faker <https://github.com/joke2k/faker>`_ and return it's result. Is used to generate random data.
        F.e. ::

            - echo: {from: '{{ random("email") }}', to: one.output}

        :param param: Faker's provider name.
        """
        data = {}
        fake = Faker(locale=locale)
        for modname, importer in self.get_submodules_of('faker.providers'):  # add all known providers
            fake.add_provider(importer.find_module(modname).load_module(modname))
        for param in param_obj:
            if hasattr(fake, param):
                data.update({
                    param: getattr(fake, param)()
                })
            else:
                raise ValueError('Unknown param to randomize: ' + param)
        return data

    def filter_hash(self, data, alg='md5'):
        """
        Filter for hashing data.
        F.e. ::

            - echo: {from: '{{ my_var | hash("sha1") }}', to: two.output}

        :param data: data to hash
        :param alg: algorithm to use
        """
        if hasattr(hashlib, alg):
            m = getattr(hashlib, alg)()
            m.update(data.encode())
            return m.hexdigest()
        else:
            raise ValueError('Unknown algorithm: ' + data)

    def function_now(self, date_format='%Y-%m-%d %H:%M:%S.%f'):
        """
        Get current date in a specified format.
        F.e. ::

            - echo: {from: '{{ now("%Y-%m-%d") }}', to: year.output}
        :param date_format: date format
        """
        return datetime.datetime.now().strftime(date_format)

    def function_now_ts(self):
        """
        Get current date time in as a timestamp.
        F.e. ::

            - echo: {from: '{{ now_ts() }}', to: timestamp.output}
        """
        return round(time.time(),
                     6)  # from timestamp uses rounding, so we should also use it here, to make them compatible

    def filter_astimestamp(self, data, date_format='%Y-%m-%d %H:%M:%S.%f'):
        """
        Convert date to timestamp. Date can be either python date object or date string
        F.e. ::

            - echo: {from: '{{ date_time_var | astimestamp }}', to: two.output}

        :param data: date time object (or string representation) to be converted to a timestamp.
        :param date_format: date format (in case it is a string)
        """
        if isinstance(data, str):
            data = datetime.datetime.strptime(data, date_format)
        return datetime.datetime.timestamp(data)

    def filter_asdate(self, data, date_format='%Y-%m-%d %H:%M:%S.%f'):
        """
        Convert timestamp to date
        F.e. ::

            - echo: {from: '{{ timestamp_var | asdate(date_format="%Y-%m-%d") }}', to: two.output}

        :param data: timestamp to be converted to a date
        :param date_format: expected data format.
        """
        if isinstance(data, str):
            if '.' in data:
                data = float(data)
            else:
                data = int(data)
        return datetime.datetime.fromtimestamp(data).strftime(date_format)

    def function_random_int(self, range_from=-sys.maxsize - 1, range_to=sys.maxsize):
        """
        Function for random number return. Output can be controlled by `range_from` and `range_to` attributes.
        F.e. ::

            - echo: {from: '{{ random_int(range_from=1) }}', to: one.output}

        """
        return random.randint(range_from, range_to)

    def function_random_choice(self, sequence):
        """
        Function to make a random choice in a collection.
        F.e. ::

            - echo: {from: '{{ random_choice([1, 2, 3]) }}', to: one.output}

        :param sequence: collection of elements to choose from.
        """
        return random.choice(sequence)


if __name__ == '__main__':
    # 自定义生成数据元祖/列表
    source_name = ['name', 'email', 'address',
                   'ssn', 'company', 'job',
                   'phone_number', 'email'
                   ]
    provider = MyProvider()
    test_data = provider.function_random(source_name, locale='zh_CN')
    print(test_data)
