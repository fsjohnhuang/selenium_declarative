#!/usr/bin/env python
# -*- coding: utf-8 -*-

def print_assert_ret(ctx):
    assert_ret = ctx.assert_rets[-1]
    if assert_ret["result"] is None:
        print("\033[1;44m OK \033[0m {0}: collected expected value {1}.".format(assert_ret["id"], assert_ret["expect"]))
    elif assert_ret["result"]:
        print("\033[1;44m OK \033[0m {0}".format(assert_ret["id"]))
    else:
        print("\033[1;41m Fail \033[0m {0}: expect {1}, but acutal value is {2}".format(assert_ret["id"], assert_ret["expect"], assert_ret["actual"]))
