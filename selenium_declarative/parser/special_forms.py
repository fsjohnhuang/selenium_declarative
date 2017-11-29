#!/usr/bin/env python
# -*- coding: utf-8 -*-
from inspect import isfunction, getargspec

def sf_when(__parser__, cond_expr, *exprs):
    cond_ret = __parser__.parse_with_sub_context(cond_expr)
    if cond_ret:
        __parser__.parse_with_sub_context(exprs)

def sf_not(__parser__, exprs):
    ret = not __parser__.parse_with_sub_context(exprs)
    return ret

def sf_try(__parser__, *exprs):
    body_exprs = []
    catch_exprs = []
    finally_exprs = []

    for expr in exprs:
        if expr[0] == "catch":
            catch_exprs.append(expr)
        elif expr[0] == "finally":
            finally_exprs.append(expr)
        else:
            body_exprs.append(expr)

    if len(finally_exprs) > 1:
        raise SyntaxError("more than one finally expression.")

    try:
        __parser__.parse_with_sub_context(body_exprs)
    except Exception, e:
        if len(catch_exprs) > 0:
            __parser__.parse_with_sub_context(catch_exprs, [e])
        else:
            raise e
    finally:
        __parser__.parse_with_sub_context(finally_exprs)

def sf_catch(__peek__, __parser__, exception_type, *exprs):
    e = __peek__()
    if isinstance(e, exception_type):
        __parser__.parse_with_sub_context(exprs)

def sf_finally(__parser__, *exprs):
    __parser__.parse_with_sub_context(exprs)
