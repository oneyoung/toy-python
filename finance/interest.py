#!/usr/bin/env python2
from __future__ import division
from sympy import *


def simple_loan(con_dict):
    """
    solve the function: PV = CF/((i + i)**n)
    where:
        PV -- Present value
        CF -- current flow to pay off the debut
        i  -- interest rate
        n  -- num of year
    the function takes exactly 3 of them to form a dict,
    and find out the value of unknow.
    for example:
        in order to get the PV, you call call like this:
            simple_loan({"CF":1000, "i":0.05, "n":3})
    """
    PV = Symbol("PV")  # present value
    CF = Symbol("CF")  # current flow
    i = Symbol("i")  # interest rate
    n = Symbol("n")  # num of years
    formula = CF / ((1 + i) ** n) - PV
    target = set(["PV", "CF", "i", "n"]).difference(con_dict.keys()).pop()
    tmp = solve(formula, target).pop()
    return tmp.subs(con_dict)


def SUM(func, seq):
    ''' func -- the function that take one argument from seq
        seq -- the seq that applied to func
    '''
    return sum(map(func, seq))


def fixed_pay_loan(con_dict, n):
    """
    solve the function: LV = FP/(1+i) + FP/(1+i)**2 + ... + FP/(1+i)**n
    where:
        LV -- Loan value
        FP -- fixed payment each year
        i  -- interest rate
        n  -- num of year
    parameter:
        con_dict -- a dict that consists of 2 member of ["LV", "FP", "i"]
        n  -- num of year
    """
    LV = Symbol("LV")
    FP = Symbol("FP")
    i = Symbol("i")

    def gen(num):
        return FP / ((i + 1) ** num)

    formula = SUM(gen, xrange(1, n + 1)) - LV
    target = set(["LV", "FP", "i"]).difference(con_dict.keys()).pop()
    if target == "i":
        Fi = formula.subs(con_dict)

        def func(x):
            return Fi.subs({"i": x})

        return bisection(func, 0, 1)
    else:
        tmp = solve(formula, target).pop()
        return tmp.subs(con_dict)


def coupon_bond(con_dict, n):
    P = Symbol("P")
    C = Symbol("C")
    F = Symbol("F")

    def gen(num):
        return C / ((i + 1) ** num)

    formula = SUM(gen, xrange(1, n + 1)) + F / ((i + 1) ** n) - P

    pass


def bisection(F, s, e, precision=1E-6):
    """ bisection: use bisection method to slove function
    parameters:
        F -- function that takes one var makes F(x) = 0
        s -- start of bisection interval
        e -- end of bisection interval
        precision -- optional, to decide when to stop, default is 1E-6
    return value:
        the solution approaching to F(x) = 0
    """
    m = (s + e) / 2
    f_s = F(s)
    f_e = F(e)
    f_m = F(m)

    def diff_sign(num1, num2):
        return (num1 > 0 and num2 < 0) or (num1 < 0 and num2 > 0)

    if abs(f_m) < precision:  # solution found
        return m

    if not diff_sign(f_s, f_e):
        raise ArithmeticError("Function has NO zero point in [%f, %f]" % (s, e))

    if diff_sign(f_s, f_m):
        e = m
    else:
        s = m
    return bisection(F, s, e, precision)


if __name__ == "__main__":
    # just a test
    def func(x):
        return x ** 3 + 3 * x ** 5 - 50

    result = bisection(func, 0, 10)
    print result
    print func(result)
