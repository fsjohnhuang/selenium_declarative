#!/usr/bin/env python
# -*- coding: utf-8 -*-
import special_forms, expressions, operations

class Context:
    def __init__(self, driver):
        self.driver = driver
        self.expr_rets = []
        self.assert_rets = []
        self.collect_expects = {}
        self.expects = {}
        self.parse = None

def _resolve(symbol):
    if symbol.startswith("__"):
        raise SyntaxError("Forbid symbol starts with __.")

    f = None
    is_sf = hasattr(special_forms, "sf_" + symbol)
    is_expr = hasattr(expressions, "expr_" + symbol)
    is_op = hasattr(operations, "op_" + symbol)
    if is_sf:
        f = getattr(special_forms, "sf_" + symbol)
    elif is_expr:
        f = getattr(expressions, "expr_" + symbol)
    elif is_op:
        f = getattr(operations, "op_" + symbol)
        
    return f

def parser(driver, expects = None):
    ctx = Context(driver)
    if isinstance(expects, dict):
        ctx.expects = expects

    def parse(exprs):
        for expr in exprs:
            symbol = expr[0]
            args = expr[1:]
            args = [ctx] + args
            f = _resolve(symbol)
            if f:
                f(*args)
            else:
                raise SyntaxError("No such symbol {0}".format(symbol))

        return {"collect_expects": ctx.collect_expects, "assert_rets": ctx.assert_rets}

    ctx.parse = parse
    return ctx.parse

