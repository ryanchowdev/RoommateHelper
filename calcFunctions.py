import math
import random
import ast
import parser
import inspect

VALID = 0
NOINPUT = -1
HASLETTERS = -2

def checkValidInput(equation):
    checkInputFlag = VALID
    if equation == "":
        checkInputFlag = NOINPUT
    else:
        if len(equation) == 0:
            checkInputFlag = NOINPUT

        for i in equation:
            if (i >= 'a' and i <= 'z') or (i >= 'A' and i <= 'Z'):
                checkInputFlag = HASLETTERS

    return checkInputFlag

def calculate(equation):
    try:
        code = eval(equation)
    except:
        code = None
    return code
    