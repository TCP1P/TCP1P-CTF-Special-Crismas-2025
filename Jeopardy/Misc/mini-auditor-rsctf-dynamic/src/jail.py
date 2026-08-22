#!/usr/local/bin/python3 -S
from sys import addaudithook
from os import _exit

def safe_eval(exit, code):
    def hook(*args):
        exit(0)

    fun = lambda: None
    fun.__code__ = compile(code, "<code>", "eval")
    addaudithook(hook)
    f, exit = fun(), lambda*_: None
    return f

if __name__ == "__main__":
    allowed = 'abcdefghijklmnopqrstuvwxyz()*,:=_'
    payload = ''.join(_ for _ in input("Payload: ") if _ in allowed)

    if len(payload) <= 70:
        safe_eval(_exit, payload)
    else:
        print('Payload too long')
