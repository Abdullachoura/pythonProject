from enum import Enum
import numpy as np

class FunctionDerivative(Enum):
    ORIGINAL=1
    DERIVATIVE_1=2
    DERIVATIVE_2=3
    DERIVATIVE_3=4

class TermType(Enum):
    GANZ_RATIONAL = 1
    SCHNITTPUNKT = 2
    TRIGONOMETRISCH = 3

class TrigonometrischerOperator:
    COS = 1
    SIN = 2


def exponent_of(i: int) -> str:
    val = i
    to_return = ""
    while True:
        if val == 0: break
        exponent = val % 10
        if exponent == 0:
            to_return = chr(0x2070) + to_return
        elif exponent == 1:
            to_return = chr(0x00B9) + to_return
        elif exponent == 2:
            to_return = chr(0x00B2) + to_return
        elif exponent == 3:
            to_return = chr(0x00B3) + to_return
        elif exponent == 4:
            to_return = chr(0x2074) + to_return
        elif exponent == 5:
            to_return = chr(0x2075) + to_return
        elif exponent == 6:
            to_return = chr(0x2076) + to_return
        elif exponent == 7:
            to_return = chr(0x2077) + to_return
        elif exponent == 8:
            to_return = chr(0x2078) + to_return
        elif exponent == 9:
            to_return = chr(0x2079) + to_return
        else:
            raise ValueError("exponent not right value", exponent)
        val = round(val / 10, 0)
    return str(to_return)


class Function:

    def __init__(self, functype: TermType, *args):
        if functype == TermType.GANZ_RATIONAL:
            self.term = GanzrationaleTerm(*args)
        elif functype == TermType.SCHNITTPUNKT:
            self.term = SchnittpunktTerm(*args)
        elif functype == TermType.TRIGONOMETRISCH:
            self.term = TrigonomischerTerm(args[0], *args[1:])

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

    def deriv1_as_str(self):
        return self.term.deriv1_as_str()

    def deriv2_as_str(self):
        return self.term.deriv2_as_str()

    def deriv3_as_str(self):
        return self.term.deriv3_as_str()

    def __str__(self):
        return str(self.term)





class GanzrationaleTerm:
    def __init__(self, *args):
        print("ganzrationale", args)
        self.original = []
        self.deriv1 = []
        self.deriv2 = []
        self.deriv3 = []
        for val in args:
            self.original.append(val)

        for i in range(len(self.original)):
            if i == len(self.original)-1: continue
            self.deriv1.append(float(i+1) * self.original[i+1])

        for i in range(len(self.deriv1)):
            if i == len(self.deriv1)-1: continue
            self.deriv2.append(float(i+1) * self.deriv1[i+1])

        for i in range(len(self.deriv2)):
            if i == len(self.deriv2)-1: continue
            self.deriv3.append(float(i+1) * self.deriv2[i+1])

    def calc_original(self, x):
        to_return = 0
        for i in range(len(self.original)):
            to_return += self.original[i]* x ** float(i)
        return to_return

    def calc_deriv1(self, x):
        to_return = 0
        for i in range(len(self.deriv1)):
            to_return += self.deriv1[i] * x ** float(i)
        return to_return

    def calc_deriv2(self, x):
        to_return = 0
        for i in range(len(self.deriv2)):
            to_return += self.deriv2[i] * x ** float(i)
        return to_return

    def calc_deriv3(self, x):
        to_return = 0
        for i in range(len(self.deriv3)):
            to_return = self.deriv3 * x ** float(i)
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

    def deriv1_as_str(self):
        toReturn = ""
        for i in range(len(self.deriv1) - 1, -1, -1):
            if i == 0:
                if self.deriv1[i] < 0:
                    toReturn += f"-{abs(self.deriv1[i])}"
                else:
                    toReturn += f"+{self.deriv1[i]}"
            elif i == 1:
                if len(self.deriv1) - 1 == i or self.deriv1[i] < 0:
                    toReturn += f"{self.deriv1[i]}x"
                else:
                    toReturn += f"+{self.deriv1[i]}x"
            elif len(self.deriv1) - 1 == i:
                toReturn += f"{self.deriv1[i]}x{exponent_of(i)}"
            elif self.deriv1[i] < 0:
                toReturn += f"-{abs(self.deriv1[i])}x^{exponent_of(i)}"
            else:
                toReturn += f"+{self.deriv1[i]}x^{exponent_of(i)}"
        return toReturn
    def deriv2_as_str(self):
        toReturn = ""
        for i in range(len(self.deriv2) - 1, -1, -1):
            if i == 0:
                if self.deriv2[i] < 0:
                    toReturn += f"-{abs(self.deriv2[i])}"
                else:
                    toReturn += f"+{self.deriv2[i]}"
            elif i == 1:
                if len(self.deriv2) - 1 == i or self.deriv2[i] < 0:
                    toReturn += f"{self.deriv2[i]}x"
                else:
                    toReturn += f"+{self.deriv2[i]}x"
            elif len(self.deriv2) - 1 == i:
                toReturn += f"{self.deriv2[i]}x{exponent_of(i)}"
            elif self.deriv2[i] < 0:
                toReturn += f"-{abs(self.deriv2[i])}x^{exponent_of(i)}"
            else:
                toReturn += f"+{self.deriv2[i]}x^{exponent_of(i)}"
        return toReturn
    def deriv3_as_str(self):
        toReturn = ""
        for i in range(len(self.deriv3) - 1, -1, -1):
            if i == 0:
                if self.deriv3[i] < 0:
                    toReturn += f"-{abs(self.deriv3[i])}"
                else:
                    toReturn += f"+{self.deriv3[i]}"
            elif i == 1:
                if len(self.deriv3) - 1 == i or self.deriv3[i] < 0:
                    toReturn += f"{self.deriv3[i]}x"
                else:
                    toReturn += f"+{self.deriv3[i]}x"
            elif len(self.deriv3) - 1 == i:
                toReturn += f"{self.deriv3[i]}x{exponent_of(i)}"
            elif self.deriv3[i] < 0:
                toReturn += f"-{abs(self.deriv3[i])}x^{exponent_of(i)}"
            else:
                toReturn += f"+{self.deriv3[i]}x^{exponent_of(i)}"
        return toReturn

    def __str__(self):
        toReturn = ""
        for i in range(len(self.original)-1, -1, -1):
            if i == 0:
                if self.original[i] < 0:
                    toReturn += f"-{abs(self.original[i])}"
                else:
                    toReturn += f"+{self.original[i]}"
            elif i == 1:
                if len(self.original)-1 == i or self.original[i] < 0:
                    toReturn += f"{self.original[i]}x"
                else:
                    toReturn += f"+{self.original[i]}x"
            elif len(self.original)-1 == i:
                toReturn += f"{self.original[i]}x{exponent_of(i)}"
            elif self.original[i] < 0:
                toReturn += f"-{abs(self.original[i])}x^{exponent_of(i)}"
            else:
                toReturn += f"+{self.original[i]}x^{exponent_of(i)}"
        return toReturn


class SchnittpunktTerm:

    def __init__(self, *args):
        self.original = []
        print(args)
        for val in args:
            self.original.append(val)
        self.deriv1 = [self.original[0]*2, self.original[1]*self.original[0]*2]
        self.deriv2 = [self.deriv1[0]]


    def calc_original(self, x):
        return self.original[0] * (x + self.original[1])**2 + self.original[2]

    def calc_deriv1(self, x):
        return self.deriv1[0] * x + self.deriv1[1]

    def calc_deriv2(self, x):
        return self.deriv2[0]

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

    def deriv1_as_str(self):
        toReturn = f"{self.deriv1[0]}x "
        if self.deriv1[1] < 0:
            toReturn += f"-{abs(self.deriv1[1])}"
        else:
            toReturn += f"+{self.deriv1[1]}"
        return toReturn

    def deriv2_as_str(self):
        return str(self.deriv2[0])

    def deriv3_as_str(self):
        return "0"

    def __str__(self):
        toReturn = f"{self.original[0]}(x "
        if self.original[1] < 0:
            toReturn += f"-{abs(self.original[1])})²"
        else:
            toReturn += f"+{self.original[1]})²"

        if self.original[2] < 0:
            toReturn += f"-{abs(self.original[2])}"
        else:
            toReturn += f"+{self.original[2]}"
        return toReturn


class TrigonomischerTerm:

    def __init__(self, trigop : TrigonometrischerOperator, *args):
        self.trigOp = trigop
        self.original = []
        for val in args:
            self.original.append(val)
        self.deriv1 = self.original.copy()
        self.deriv2 = self.original.copy()
        self.deriv3 = self.original.copy()



    def calc_original(self, x):
        to_return = 0
        if self.trigOp == TrigonometrischerOperator.SIN:
            to_return = self.original[0] * np.sin(((np.pi * 2) / self.original[2]) * x + self.original[1])
        elif self.trigOp == TrigonometrischerOperator.COS:
            to_return = self.original[0] * np.cos(((np.pi * 2) / self.original[2]) * x + self.original[1])
        return to_return

    def calc_deriv1(self, x):
        to_return = 0
        if self.trigOp == TrigonometrischerOperator.SIN:
            to_return = self.deriv1[0] * np.cos((np.pi * 2) / self.deriv1[2] * x + self.deriv1[1])
        elif self.trigOp == TrigonometrischerOperator.COS:
            to_return = self.deriv1[0] * -1 * np.sin((np.pi * 2) / self.deriv1[2] * x + self.deriv1[1])
        return to_return

    def calc_deriv2(self, x):
        to_return = 0
        if self.trigOp == TrigonometrischerOperator.SIN:
            to_return = self.deriv2[0] * -1 * np.sin((np.pi * 2) / self.deriv2[2] * x + self.deriv2[1])
        elif self.trigOp == TrigonometrischerOperator.COS:
            to_return = self.deriv2[0] * -1 * np.cos((np.pi * 2) / self.deriv2[2] * x + self.deriv2[1])
        return to_return

    def calc_deriv3(self, x):
        to_return = 0
        if self.trigOp == TrigonometrischerOperator.SIN:
            to_return = self.deriv2[0] * -1 * np.cos((np.pi * 2) / self.deriv2[2] * x + self.deriv2[1])
        elif self.trigOp == TrigonometrischerOperator.Cos:
            to_return = self.deriv2[0] * np.sin((np.pi * 2) / self.deriv2[2] * x + self.deriv2[1])
        return  to_return

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

    def deriv1_as_str(self):
        toReturn = ""
        if self.trigOp == TrigonometrischerOperator.SIN:
            f"{self.deriv1[0]}*"
            toReturn += 'cos'
        elif self.trigOp == TrigonometrischerOperator.COS:
            f"{-1 * self.deriv1[0]}*"
            toReturn += 'sin'

        toReturn += f'({chr(0x03c9)}t'
        if self.deriv1[1] < 0:
            toReturn += f"-{abs(self.deriv1[1])})"
        else:
            toReturn += f"+{self.deriv1[1]})"
        toReturn += f' | T={self.deriv1[2]}'
        return toReturn

    def deriv2_as_str(self):
        toReturn = ""
        if self.trigOp == TrigonometrischerOperator.SIN:
            toReturn += f"{-1 * self.deriv2[0]}*"
            toReturn += 'sin'
        elif self.trigOp == TrigonometrischerOperator.COS:
            toReturn += f"{-1 * self.deriv2[0]}"
            toReturn += 'cos'

        toReturn += f'({chr(0x03c9)}t'
        if self.deriv2[1] < 0:
            toReturn += f"-{abs(self.deriv2[1])})"
        else:
            toReturn += f"+{self.deriv2[1]})"
        toReturn += f' | T={self.deriv2[2]}'
        return toReturn

    def deriv3_as_str(self):
        toReturn = ""
        if self.trigOp == TrigonometrischerOperator.SIN:
            toReturn += f"{-1 * self.deriv3[0]}*"
            toReturn += 'cos'
        elif self.trigOp == TrigonometrischerOperator.COS:
            toReturn += f"{self.deriv3[0]}"
            toReturn += 'sin'

        toReturn += f'({chr(0x03c9)}t'
        if self.deriv3[1] < 0:
            toReturn += f"-{abs(self.deriv3[1])})"
        else:
            toReturn += f"+{self.deriv3[1]})"
        toReturn += f' | T={self.deriv3[2]}'
        return toReturn

    def __str__(self):
        toReturn = f"{self.original[0]}*"
        if self.trigOp == TrigonometrischerOperator.SIN:
            toReturn += 'sin'
        elif self.trigOp == TrigonometrischerOperator.COS:
            toReturn += 'cos'

        toReturn += f'({chr(0x03c9)}t'
        if self.original[1] < 0:
            toReturn += f"-{abs(self.original[1])})"
        else:
            toReturn += f"+{self.original[1]})"
        toReturn += f' | T={self.original[2]}'
        return toReturn
