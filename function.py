from enum import Enum

import numpy

class FunctionType(Enum):
    ORIGINAL=1
    DERIVATIVE_1=2
    DERIVATIVE_2=3
    DERIVATIVE_3=4

class Function:

    original: []
    deriv_1: []
    deriv_2: []
    deriv_3: []

    def __init__(self, *args):
        print(args)
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

    def calc_for_range(self, fun_type: FunctionType, min, max, inc):
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
            if fun_type == FunctionType.ORIGINAL:
                to_return_arr.append(self.calc_original(x))
            elif fun_type == FunctionType.DERIVATIVE_1:
                to_return_arr.append(self.calc_deriv1(x))
            elif fun_type == FunctionType.DERIVATIVE_2:
                to_return_arr.append(self.calc_deriv2(x))
            elif fun_type == FunctionType.DERIVATIVE_3:
                to_return_arr.append(self.calc_deriv3(x))
        return to_return_arr

    def arr_calc(self, x_arr, func_type: FunctionType):
        to_return = []
        for x in x_arr:
            if func_type == FunctionType.ORIGINAL:
                to_return.append(self.calc_original(x))
            elif func_type == FunctionType.DERIVATIVE_1:
                to_return.append(self.calc_deriv1(x))
            elif func_type == FunctionType.DERIVATIVE_2:
                to_return.append(self.calc_deriv2(x))
            elif func_type == FunctionType.DERIVATIVE_3:
                to_return.append(self.calc_deriv3(x))
        return to_return

    def __str__(self):
        toReturn = ""
        for i in range(len(self.original)-1, -1, -1):
            if i == 0:
                if self.original[i] < 0:
                    toReturn += f"-{self.original[i]}"
                else:
                    toReturn += f"+{self.original[i]}"
                continue

            if i == len(self.original)-1 and self.original[i] > 0:
                toReturn += f"{self.original[i]}x^{i}"
                continue

            if self.original[i] < 0:
                toReturn += f"-{self.original[i]}x^{i}"
            else:
                toReturn += f"+{self.original[i]}x^{i}"






