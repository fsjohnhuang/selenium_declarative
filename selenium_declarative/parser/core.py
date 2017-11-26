#!/usr/bin/env python
# -*- coding: utf-8 -*-
from inspect import getargspec, isfunction
import special_forms, expressions

def reflect_builtins(module):
    members = dir(module)
    pub_members = filter(lambda m: not m.startswith("_"), members)
    fns = {}
    for pub_member in pub_members:
        fns["_".join(pub_member.split("_")[1:])] = getattr(module, pub_member)
    return fns

class Context:
    def __init__(self, context=None):
        self.context = context
        self.__stack = []      # local variables, append only

    def peek(self, index=0):
        """0 means the top item of stack
        """
        length_stack = len(self.__stack)
        idx = index - length_stack
        if 0 <= idx:
            # raise an error when index is greater than the length of the whole stack
            return self.context.peek(idx)
        else:
            return self.__stack[-index-1]

    def peek_locals(self, index=0):
        length_stack = len(self.__stack)
        idx = length_stack + (-index-1)
        return self.__stack[idx] if 0 <= idx < length_stack else None

    def push(self, value):
        self.__stack.append(value)

class Parser:
    def __init__(self, driver, fns=None):
        self.driver = driver
        self.sfs = reflect_builtins(special_forms)         # special forms
        self.fns = reflect_builtins(expressions)           # global functions
        if isinstance(fns, dict):
            for kv in fns.items():
                self.fns.setdefault(kv[0], kv[1])
        self.globals = {}                                  # global variables
        self.context = Context()

    def __resolve(self, symbol):
        if symbol.startswith("__"):
            raise SyntaxError("Forbid symbol starts with __.")

        ret = self.sfs.get(symbol)
        if ret is None:
            ret = self.fns.get(symbol)

        return ret

    def __invoke(self, func, args):
        signature = getargspec(func)[0]
        builtins = []
        for arg in signature:
            if "__parser__" == arg:
                builtins.append(self)
            elif "__driver__" == arg:
                builtins.append(self.driver)
            elif "__globals__" == arg:
                builtins.append(self.globals)
            elif "__peek__" == arg:
                builtins.append(lambda index=0: self.context.peek(index))

        ret = apply(func, builtins + args)
        return ret

    def parse_with_sub_context(self, exprs):
        if exprs is None:
            return None

        self.context = Context(self.context)
        self.parse(exprs)
        ret = self.context.peek_locals()
        # recover
        self.context = self.context.context

        return ret

    def parse(self, exprs):
        # exprs should be 2 dimensions array as least.
        if not isinstance(exprs[0], list):
            exprs = [exprs]

        for expr in exprs:
            symbol = expr[0]
            args = expr[1:]

            ret = None
            if isfunction(symbol):
                ret = self.__invoke(symbol, args)
            else:
                fn = self.__resolve(symbol)
                if fn:
                    ret = self.__invoke(fn, args)
                else:
                    raise SyntaxError("Can't resolve symbol {0}.".format(symbol))

            # if fn is an expression, stores the return value of it into stack
            if not ret is None:
                self.context.push(ret)
