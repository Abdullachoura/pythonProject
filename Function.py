import time
import types
from enum import Enum

import kiwisolver
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

class TrigonometrischerOperator(Enum):
    COS = 1
    SIN = 2

def dx(f, val):
    return abs(0-f(val))

def newton_verfahren(f, fd, val, acc):
    delta = dx(f, val)
    steps = 0
    while delta > acc and steps < 200:
        val = val - f(val) / fd(val)
        delta = dx(f, val)
        steps += 1
    if steps >= 200:
        val = None
    return val


def superscript_of(i: int) -> str:
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
        val = np.floor(val / 10)
    return str(to_return)

def subscript_of(i: int) -> str:
    val = i
    to_return = ""
    while True:
        exponent = val % 10
        if exponent == 0:
            to_return = chr(0x2080) + to_return
        elif exponent == 1:
            to_return = chr(0x2081) + to_return
        elif exponent == 2:
            to_return = chr(0x2082) + to_return
        elif exponent == 3:
            to_return = chr(0x2083) + to_return
        elif exponent == 4:
            to_return = chr(0x2084) + to_return
        elif exponent == 5:
            to_return = chr(0x2085) + to_return
        elif exponent == 6:
            to_return = chr(0x2086) + to_return
        elif exponent == 7:
            to_return = chr(0x2087) + to_return
        elif exponent == 8:
            to_return = chr(0x2088) + to_return
        elif exponent == 9:
            to_return = chr(0x2089) + to_return
        else:
            raise ValueError("exponent not right value", exponent)
        val = np.floor(val / 10)
        if val == 0: break
    return str(to_return)

def round(x, prec):
    a = np.abs(x * 10 ** prec)
    b = np.floor(a) + np.floor(2 * (a % 1))
    c = np.sign(x) * b / 10 ** prec
    return c


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

    def calc_nullstellen(self, funcDer: FunctionDerivative, min, max, streckung=None) -> []:
        if funcDer == FunctionDerivative.DERIVATIVE_3:
            raise ValueError("nullstellen von derivative 3 sollten nicht berechnet werden")
        return_arr_length = -1
        if isinstance(self.term, GanzrationaleTerm):
            return_arr_length = len(self.term.original) - 1
        if isinstance(self.term, SchnittpunktTerm):
            return_arr_length = 2
            if np.sign(self.term.original[0]) == np.sign(self.term.original[2]) \
                    and funcDer == FunctionDerivative.ORIGINAL:
                return []
        if isinstance(self.term, TrigonomischerTerm):
            to_use_arr = []
            arr_to_return = []
            w = 2 * np.pi / self.term.original[2]
            val = 0
            i = int(min)
            while val <= max:
                if self.term.trigOp == TrigonometrischerOperator.SIN:
                    if funcDer == FunctionDerivative.ORIGINAL:
                        val = (i * np.pi - self.term.original[1]) / w
                    elif funcDer == FunctionDerivative.DERIVATIVE_1:
                        val = ((np.pi / 2) + i * np.pi - self.term.original[1]) / w
                    elif funcDer == FunctionDerivative.DERIVATIVE_2:
                        val = (i * np.pi - self.term.original[1]) / w
                elif self.term.trigOp == TrigonometrischerOperator.COS:
                    if funcDer == FunctionDerivative.ORIGINAL:
                        val = ((np.pi / 2) + i * np.pi - self.term.original[1]) / w
                    elif funcDer == FunctionDerivative.DERIVATIVE_1:
                        val = (i * np.pi - self.term.original[1]) / w
                    elif funcDer == FunctionDerivative.DERIVATIVE_2:
                        val = ((np.pi / 2) + i * np.pi - self.term.original[1]) / w
                if min < val < max:
                    val = round(val, 3)
                    arr_to_return.append((val, 0))
                i += 1
        else:
            arr_to_return = []
            for x in range(int(min), int(max)):
                val = float(x)
                if val == 0:
                    continue
                try:
                    if funcDer == FunctionDerivative.ORIGINAL:
                        val = newton_verfahren(self.calc_original, self.calc_deriv1, val, 0.001)
                    elif funcDer == FunctionDerivative.DERIVATIVE_1:
                        val = newton_verfahren(self.calc_deriv1, self.calc_deriv2, val, 0.001)
                        print("val", val)
                    elif funcDer == FunctionDerivative.DERIVATIVE_2:
                        val = newton_verfahren(self.calc_deriv2, self.calc_deriv3, val, 0.001)
                except ZeroDivisionError:
                    continue
                if isinstance(val, types.NoneType):
                    continue
                val = round(val, 3)
                if (val, 0) not in arr_to_return:
                    arr_to_return.append((val, 0))
                if len(arr_to_return) == return_arr_length:
                    break
            if return_arr_length == -1:
                raise ValueError("Dickhead")
            elif return_arr_length < len(arr_to_return):
                return None
        #elif return_arr_length > len(arr_to_return):
            #arr_to_return += [None for i in range(return_arr_length - len(arr_to_return))]
        return arr_to_return

    def calc_extrempunkte(self, min, max):
        if isinstance(self.term, GanzrationaleTerm) and len(self.term.original) < 3:
            raise ValueError("term ist linear und hat keine Extrempunkte")
        ableitung1_nullstellen = self.calc_nullstellen(FunctionDerivative.DERIVATIVE_1, min, max)
        print("ableitung1_nullstellen", ableitung1_nullstellen)
        extremwerte = [nullstelle[0] for nullstelle in ableitung1_nullstellen]
        print("extremwerte", extremwerte)
        extremstellen_y = self.arr_calc(extremwerte, FunctionDerivative.ORIGINAL)
        print("extremstellen", extremstellen_y)
        extremstellen = []
        for i in range(len(extremstellen_y)):
            extremstellen.append((extremwerte[i], extremstellen_y[i]))
        print("extremstellen", extremstellen)
        return extremstellen

    def calc_wendepunkte(self, min, max):
        if isinstance(self.term, GanzrationaleTerm) and len(self.term.original) < 4:
            raise ValueError("term ist unterdem 3. Grad und hat somit keine Wendepunkte")
        if self.calc_deriv3(1) == 0:
            return None
        ableitung2_nullstellen = self.calc_nullstellen(FunctionDerivative.DERIVATIVE_2, min, max)
        wendepunktwerte = [nullstelle[0] for nullstelle in ableitung2_nullstellen]
        wendepunkt_y = self.arr_calc(wendepunktwerte, FunctionDerivative.ORIGINAL)
        wendepunkte = []
        for i in range(len(wendepunkt_y)):
            wendepunkte.append((wendepunktwerte[i], wendepunkt_y[i]))
        return wendepunkte





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
            to_return = self.deriv3[i] * x ** float(i)
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
                if len(self.deriv1) == 1:
                    toReturn += f"{self.deriv1[i]}"
                elif self.deriv1[i] < 0:
                    toReturn += f"-{abs(self.deriv1[i])}"
                else:
                    toReturn += f"+{self.deriv1[i]}"
            elif i == 1:
                if len(self.deriv1) - 1 == i or self.deriv1[i] < 0:
                    toReturn += f"{self.deriv1[i]}x"
                else:
                    toReturn += f"+{self.deriv1[i]}x"
            elif len(self.deriv1) - 1 == i:
                toReturn += f"{self.deriv1[i]}x{superscript_of(i)}"
            elif self.deriv1[i] < 0:
                toReturn += f"-{abs(self.deriv1[i])}x{superscript_of(i)}"
            else:
                toReturn += f"+{self.deriv1[i]}x{superscript_of(i)}"
        if toReturn == "":
            toReturn = "0"
        return toReturn
    def deriv2_as_str(self):
        toReturn = ""
        for i in range(len(self.deriv2) - 1, -1, -1):
            if i == 0:
                if len(self.deriv2) == 1:
                    toReturn += f"{self.deriv2[i]}"
                elif self.deriv2[i] < 0:
                    toReturn += f"-{abs(self.deriv2[i])}"
                else:
                    toReturn += f"+{self.deriv2[i]}"
            elif i == 1:
                if len(self.deriv2) - 1 == i or self.deriv2[i] < 0:
                    toReturn += f"{self.deriv2[i]}x"
                else:
                    toReturn += f"+{self.deriv2[i]}x"
            elif len(self.deriv2) - 1 == i:
                toReturn += f"{self.deriv2[i]}x{superscript_of(i)}"
            elif self.deriv2[i] < 0:
                toReturn += f"-{abs(self.deriv2[i])}x{superscript_of(i)}"
            else:
                toReturn += f"+{self.deriv2[i]}x{superscript_of(i)}"
        if toReturn == "":
            toReturn = "0"
        return toReturn
    def deriv3_as_str(self):
        toReturn = ""
        for i in range(len(self.deriv3) - 1, -1, -1):
            if i == 0:
                if len(self.deriv3) == 1:
                    toReturn += f"{self.deriv3[i]}"
                elif self.deriv3[i] < 0:
                    toReturn += f"-{abs(self.deriv3[i])}"
                else:
                    toReturn += f"+{self.deriv3[i]}"
            elif i == 1:
                if len(self.deriv3) - 1 == i or self.deriv3[i] < 0:
                    toReturn += f"{self.deriv3[i]}x"
                else:
                    toReturn += f"+{self.deriv3[i]}x"
            elif len(self.deriv3) - 1 == i:
                toReturn += f"{self.deriv3[i]}x{superscript_of(i)}"
            elif self.deriv3[i] < 0:
                toReturn += f"-{abs(self.deriv3[i])}x{superscript_of(i)}"
            else:
                toReturn += f"+{self.deriv3[i]}x{superscript_of(i)}"
        if toReturn == "":
            toReturn = "0"
        return toReturn

    def __str__(self):
        toReturn = ""
        for i in range(len(self.original)-1, -1, -1):
            if i == 0:
                if len(self.original) == 1:
                    toReturn += f"{self.original[i]}"
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
                toReturn += f"{self.original[i]}x{superscript_of(i)}"
            elif self.original[i] < 0:
                toReturn += f"-{abs(self.original[i])}x{superscript_of(i)}"
            else:
                toReturn += f"+{self.original[i]}x{superscript_of(i)}"
        if toReturn == "":
            toReturn = "0"
        return toReturn


class SchnittpunktTerm:

    def __init__(self, *args):
        self.original = []
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
            to_return = self.deriv1[0] * (np.cos((np.pi * 2) / self.deriv1[2] * x + self.deriv1[1]))
        elif self.trigOp == TrigonometrischerOperator.COS:
            to_return = self.deriv1[0] * -1 * (np.sin((np.pi * 2) / self.deriv1[2] * x + self.deriv1[1]))
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
        elif self.trigOp == TrigonometrischerOperator.COS:
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
