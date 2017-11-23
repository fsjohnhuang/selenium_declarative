#!/usr/bin/env python
# -*- coding: utf-8 -*-

def print_assert_summary(assert_rets):
    total = len(assert_rets)
    failure = 0
    success = 0
    for ret in assert_rets:
        if ret.get("result"):
            success += 1
        else:
            failure += 1
    print("Tests ran {total}, \033[1;44m Successes {success} \033[0m, \033[1;41m Failures {failure} \033[0m".format(total=total, success=success, failure=failure))
