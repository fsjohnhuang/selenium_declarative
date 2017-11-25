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
