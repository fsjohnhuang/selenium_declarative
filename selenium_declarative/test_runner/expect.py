#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

class NoExpectException(Exception):
    def __init__(self):
        super(NoExpectException, self).__init__()

class Expect:

    __delimitation = " ------- "
    __format = "{0} ------- {1}"

    def __init__(self, path):
        self.path = path
        self.expects = {}
        self.new_expects = {}

    def __read(self):
        if os.path.exists(self.path):
            if os.path.isfile(self.path):
                raise Exception("Set dir path pls.")
        else:
            os.mkdir(path)

        names = os.listdir(path)
        names.sort()
        for name in names:
            abs_path = os.path.join(path, name)
            if os.path.isfile(abs_path):
                with open(abs_path) as f:
                    for line in f.readlines:
                        # id - value
                        line = line.strip()
                        kvs = line.split(self.__delimitation)
                        self[kvs[0].strip()] = kvs[1].strip()

    def get(self, id):
        self.expects.get(id)

    def save(self, id, value):
        self.new_expects[id] = value

    def close(self):
        name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(self.dir, name)
        with open(file_path) as f:
            for expect in self.new_expects.items():
                f.write(self.__format.format(expect[0], expect[1]) + "\n")
