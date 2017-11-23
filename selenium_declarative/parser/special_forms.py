#!/usr/bin/env python
# -*- coding: utf-8 -*-
from inspect import isfunction, getargspec
import core

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
    elif type(cond) == list:
        if not type(cond[0]) == list:
            cond = [cond]
        parse = core.parser(ctx.driver, ctx.expects, ctx.expr_rets)
        cond_ret = parse(cond).expr_rets[-1]
    else:
        cond_ret = False

    if cond_ret:
        ctx.parse(exprs)

def sf_not(ctx, expr):
    expr_ret = expr
    if isfunction(expr):
        argc = len(getargspec(expr)[0])
        if argc == 0:
            expr_ret = expr()
        else:
            expr_ret = expr(ctx)
    elif type(expr) == list:
        if not type(expr[0]) == list:
            expr = [expr]
        parse = core.parser(ctx.driver, ctx.expects, ctx.expr_rets)
        expr_ret = parse(expr).expr_rets[-1]
    ctx.expr_rets.append(not expr_ret)

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
