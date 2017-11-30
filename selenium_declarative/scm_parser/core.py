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
    LF = 6

    def tokenize(self, content):
        tokens = []
        curr_token = None
        in_str_token = False
        for i, c in enumerate(content):
            if "\n" == c:
                if curr_token is not None:
                    tokens.append(curr_token)
                    curr_token = None
                tokens.append([self.LF, c])
            else:
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
                    elif re.match("[a-zA-Z-_>=<!+%]", c):
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
            if len(content) > 0 and content[-1][-1] != "[" and unit not in "\n]" :
                unit = "," + unit
            content.append(unit)
        return ["["] + content + ["]"]

    def __parse(self, file_path, is_pretty, output_dir):
        codes = []
        code_str = ""
        with open(file_path) as f:
            content = f.read()
            tokens = self.tokenize(content)
            codes = self.gencode(tokens)
        code_str = "".join(filter(lambda code: "\n" != code, codes))

        if output_dir is not None:
            common_prefix = os.path.commonprefix([file_path, output_dir])
            if common_prefix[-1] != "/":
                common_prefix = os.path.dirname(common_prefix)
            file_path = file_path.replace(common_prefix, "")

            abs_path = os.path.join(output_dir, file_path)
            dirname = os.path.dirname(abs_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            target_path = abs_path + ".sd"
            with open(target_path, "w") as f:
                if is_pretty:
                    f.write("".join(codes))
                else:
                    f.write(code_str)


        return code_str

    def parse(self, path, **kws):
        codes = []
        pattern = kws.get("pattern", "\.scm$")
        is_pretty = kws.get("is_pretty", True)

        is_dir = os.path.isdir(path)
        output_dir = kws.get("output", path if is_dir else os.path.dirname(path))
        if output_dir[-1] != "/":
            output_dir += "/"

        if is_dir:
            for name in os.listdir(path):
                codes.append(self.parse(os.path.join(path, name), is_pretty=is_pretty, output_dir=output_dir))
        elif re.search(pattern, path):
            codes.append(self.__parse(path, is_pretty, output_dir))

        return  "".join(codes)

if __name__ == '__main__':
    p = Parser()
    dd = p.parse("/home/john/selenium_declarative/test/testsuit1/testcase1.scm")
    print(dd)
