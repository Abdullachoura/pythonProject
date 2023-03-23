from enum import Enum

import numpy

class FunctionDerivative(Enum):
    ORIGINAL=1
    DERIVATIVE_1=2
    DERIVATIVE_2=3
    DERIVATIVE_3=4

class TermType(Enum):
    GANZ_RATIONAL = 1
    SCHNITTPUNKT = 2

class Function:

    def __init__(self, functype: TermType, *args):
        if functype == TermType.GANZ_RATIONAL:
            self.term = GanzrationaleTerm(*args)
        elif functype == TermType.SCHNITTPUNKT:
            self.term = SchnittpunktTerm(*args)

    def calc_original(self, x):
        return self.term.calc_original(x)
    def calc_deriv1(self, x):
        return self.term.calc_deriv1(x)

    def calc_deriv2(self, x):
        return self.term.calc_deriv2(x)

    def calc_deriv3(self, x):
        return self.term.calc_deriv3(x)

    def calc_for_range(self, fun_type: FunctionDerivative, min, max, inc):
        return self.term.calc_for_range(fun_type, min, max, inc)

    def arr_calc(self, x_arr, func_type: FunctionDerivative):
        return self.term.arr_calc(x_arr, func_type)

    def __str__(self):
        return str(self.term)



class GanzrationaleTerm:
    def __init__(self, *args):
        print("ganzrationale", args)
        self.original = []
        self.deriv_1 = []
        self.deriv_2 = []
        self.deriv_3 = []
        for val in args:
            self.original.append(val)

        for i in range(len(self.original)):
            if i == len(self.original)-1: continue
            self.deriv_1.append(float(i+1) * self.original[i+1])

        for i in range(len(self.deriv_1)):
            if i == len(self.deriv_1)-1: continue
            self.deriv_2.append(float(i+1) * self.deriv_1[i+1])

        for i in range(len(self.deriv_2)):
            if i == len(self.deriv_2)-1: continue
            self.deriv_3.append(float(i+1) * self.deriv_2[i+1])

    def calc_original(self, x):
        to_return = 0
        for i in range(len(self.original)):
            to_return += self.original[i]* x ** float(i)
        return to_return

    def calc_deriv1(self, x):
        to_return = 0
        for i in range(len(self.deriv_1)):
            to_return += self.deriv_1[i] * x ** float(i)
        return to_return

    def calc_deriv2(self, x):
        to_return = 0
        for i in range(len(self.deriv_2)):
            to_return += self.deriv_2[i] * x ** float(i)
        return to_return

    def calc_deriv3(self, x):
        to_return = 0
        for i in range(len(self.deriv_3)):
            to_return = self.deriv_3 * x ** float(i)
        return to_return

    def calc_for_range(self, fun_type: FunctionDerivative, min, max, inc):
        '''
        gibt ergebnisse als array zurück
        :param: fun: calc funktion von classe Funktion
         min: untere grenze\n
         max: obere grenze\n
         inc: schritt größe\n
        :return: array der ergebnisse
        '''
        to_return_arr = []
        for x in range(min, max, inc):
            if fun_type == FunctionDerivative.ORIGINAL:
                to_return_arr.append(self.calc_original(x))
            elif fun_type == FunctionDerivative.DERIVATIVE_1:
                to_return_arr.append(self.calc_deriv1(x))
            elif fun_type == FunctionDerivative.DERIVATIVE_2:
                to_return_arr.append(self.calc_deriv2(x))
            elif fun_type == FunctionDerivative.DERIVATIVE_3:
                to_return_arr.append(self.calc_deriv3(x))
        return to_return_arr

    def arr_calc(self, x_arr, func_type: FunctionDerivative):
        to_return = []
        for x in x_arr:
            if func_type == FunctionDerivative.ORIGINAL:
                to_return.append(self.calc_original(x))
            elif func_type == FunctionDerivative.DERIVATIVE_1:
                to_return.append(self.calc_deriv1(x))
            elif func_type == FunctionDerivative.DERIVATIVE_2:
                to_return.append(self.calc_deriv2(x))
            elif func_type == FunctionDerivative.DERIVATIVE_3:
                to_return.append(self.calc_deriv3(x))
        return to_return

    def __str__(self):
        toReturn = ""
        for i in range(len(self.original)-1, -1, -1):
            if i == 0:
                print(i, "i == 0")
                if self.original[i] < 0:
                    toReturn += f"{self.original[i]}"
                else:
                    toReturn += f"+{self.original[i]}"
            elif i == 1:
                if len(self.original)-1 == i or self.original[i] < 0:
                    toReturn += f"{self.original[i]}x"
                else:
                    toReturn += f"+{self.original[i]}x"
            elif len(self.original)-1 == i:
                toReturn += f"{self.original[i]}x^{i}"
            elif self.original[i] < 0:
                toReturn += f"{self.original[i]}x^{i}"
            else:
                toReturn += f"+{self.original[i]}x^{i}"
        return toReturn


class SchnittpunktTerm:

    def __init__(self, *args):
        self.original = []
        for val in args:
            self.original.append(val)
        self.deriv1 = [self.original[0]*2, self.original[1]*self.original[0]*2]
        self.deriv2 = [self.deriv1[0]]


    def calc_original(self, x):
        return self.original[0] * (x - self.original[1])**2 + self.original[2]

    def calc_deriv1(self, x):
        return self.deriv1[0] * x + self.deriv1[1]

    def calc_deriv2(self, x):
        return self.deriv2[0] * x

    def calc_deriv3(self, x):
        return 0

    def calc_for_range(self, functionDeriv: FunctionDerivative, start, end, inc):
        to_return = []
        for x in range(start, end, inc):
            if functionDeriv == FunctionDerivative.ORIGINAL:
                to_return.append(self.calc_original(x))
            elif functionDeriv == FunctionDerivative.DERIVATIVE_1:
                to_return.append(self.calc_deriv1(x))
            elif functionDeriv == FunctionDerivative.DERIVATIVE_2:
                to_return.append(self.calc_deriv2(x))
            elif functionDeriv == FunctionDerivative.DERIVATIVE_3:
                to_return.append(self.calc_deriv3(x))
        return to_return

    def arr_calc(self, x_arr, func_type : FunctionDerivative):
        to_return = []
        for x in x_arr:
            if func_type == FunctionDerivative.ORIGINAL:
                to_return.append(self.calc_original(x))
            elif func_type == FunctionDerivative.DERIVATIVE_1:
                to_return.append(self.calc_deriv1(x))
            elif func_type == FunctionDerivative.DERIVATIVE_2:
                to_return.append(self.calc_deriv2(x))
            elif func_type == FunctionDerivative.DERIVATIVE_3:
                to_return.append(self.calc_deriv3(x))
        return to_return

    def __str__(self):
        toReturn = f"{self.original[0]}(x "
        if self.original[1] < 0:
            toReturn += f"+ {self.original[1]})²"
        else:
            toReturn += f"- {self.original[1]})²"

        if self.original[2] < 0:
            toReturn += f"- {self.original[2]}"
        else:
            toReturn += f"+ {self.original[2]}"
        return toReturn

