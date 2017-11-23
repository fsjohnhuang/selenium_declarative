#!/usr/bin/env python
# -*- coding: utf-8 -*-
from inspect import isfunction, getargspec

def sf_when(ctx, cond, *exprs):
    """
    Usage:
    [when cond
        [expr1]
        [expr2]]
    """
    cond_ret = cond
    if isfunction(cond):
        argc = len(getargspec(cond)[0])
        if argc == 0:
            cond_ret = cond()
        else:
            cond_ret = cond(ctx)
    if cond_ret:
        ctx.parse(exprs)

def sf_if(ctx, cond, true_exprs, false_exprs):
    """
    Usage:
    [if cond
        [[expr1]
         [expr2]]
        [[expr3]
         [expr4]]]
    """
    cond_ret = cond
    if isfunction(cond):
        argc = len(getargspec(cond)[0])
        if argc == 0:
            cond_ret = cond()
        else:
            cond_ret = cond(ctx)
    exprs = true_exprs if cond_ret else false_exprs
    for expr in exprs:
        ctx.parse(expr)
