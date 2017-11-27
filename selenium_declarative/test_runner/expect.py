#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, datetime

class NoExpectException(Exception):
    def __init__(self):
        super(NoExpectException, self).__init__()

class Expect:
    def __init__(self, path):
        self.path = path
        self.expects = {}
        self.new_expects = {}
        self.__read()

    def __read(self):
        if os.path.exists(self.path):
            if os.path.isfile(self.path):
                raise Exception("Set dir path pls.")
        else:
            print(self.path)
            os.makedirs(self.path)

        names = os.listdir(self.path)
        names.sort()
        for name in names:
            abs_path = os.path.join(self.path, name)
            if os.path.isfile(abs_path):
                with open(abs_path) as f:
                    e = eval(f.read().strip())
                    for kv in e.items():
                        self.expects[kv[0]] = kv[1]

    def get(self, id):
        return self.expects.get(id)

    def save(self, id, value):
        self.new_expects[id] = value

    def close(self):
        name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(self.path, name)
        with open(file_path, "w") as f:
            f.write(repr(self.new_expects))
