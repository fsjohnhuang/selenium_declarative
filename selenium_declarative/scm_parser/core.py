#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, os

class Parser:
    LB = 0
    RB = 1
    Symbol = 2
    String = 3
    Num = 4
    Bool = 5

    def tokenize(self, content):
        tokens = []
        curr_token = None
        in_str_token = False
        for i, c in enumerate(content):
            if in_str_token:
                if "\"" == c:
                    curr_token[1].append(c)
                    if not "\\" == content[i-1]:
                        in_str_token = False
                        tokens.append(curr_token)
                        curr_token = None
                else:
                    if curr_token is not None:
                        curr_token[1].append(c)
                    else:
                        raise SyntaxError()
            else:
                if "(" == c:
                    tokens.append([self.LB, [c]])
                elif " " == c and curr_token is not None:
                    tokens.append(curr_token)
                    curr_token = None
                if ")" == c:
                    if curr_token is not None:
                        tokens.append(curr_token)
                        curr_token = None
                    tokens.append([self.RB, [c]])
                elif "\"" == c:
                    if 0 == i or content[i-1] not in " (\\":
                        raise SyntaxError()
                    else:
                        in_str_token = True
                        curr_token = [self.String, [c]]
                elif "'" == c:
                    if 0 == i or content[i-1] not in " (":
                        raise SyntaxError()
                    else:
                        curr_token = [self.Symbol, [c]]
                elif "#" == c:
                    if 0 == i or content[i-1] not in " (":
                        raise SyntaxError()
                    else:
                        curr_token = [self.Bool, [c]]
                elif c in "tf" and curr_token is not None and curr_token[0] == self.Bool:
                    curr_token[1].append(c)
                elif re.match("[0-9]", c):
                    if curr_token is not None:
                        curr_token[1].append(c)
                    else:
                        curr_token = [self.Num, [c]]
                elif re.match("[a-zA-Z-_]", c):
                    if curr_token is not None:
                        if curr_token[0] != self.Symbol:
                            raise SyntaxError()
                        else:
                            curr_token[1].append(c)
                    else:
                        curr_token = [self.Symbol, [c]]

        return tokens

    def gencode_symbol(self, cs):
        for i, c in enumerate(cs):
            if "-" == c:
                cs[i] = "_"
            elif "'" == c:
                cs[i] = ""
        return ["\""] + cs + ["\""]

    def gencode_bool(self, cs):
        return "True" if "#t" == cs else "False"

    def gencode(self, tokens):
        content = []
        for token in tokens:
            unit = None
            if self.Symbol == token[0]:
                unit = "".join(self.gencode_symbol(token[1]))
            elif self.LB == token[0]:
                unit = "["
            elif self.RB == token[0]:
                unit = "]"
            elif self.Bool == token[0]:
                unit = "".join(self.gencode_bool(token[1]))
            else:
                unit = "".join(token[1])
            if len(content) > 0 and content[-1][-1] != "[" and unit != "]":
                unit = "," + unit
            content.append(unit)
        code = "[" + "".join(content) + "]"
        return code

    def parse(self, file_path):
        code = ""
        with open(file_path) as f:
            content = f.read()
            tokens = self.tokenize(content)
            print(tokens)
            code = self.gencode(tokens)

        target_path = file_path + ".sd"
        with open(target_path, "w") as f:
            f.write(code)

if __name__ == '__main__':
    p = Parser()
    p.parse("/home/john/selenium_declarative/test/setup.scm")
