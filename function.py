import numpy


class Function:

    original: []
    deriv_1: []
    deriv_2: []
    deriv_3: []

    def __init__(self, *args):
        self.original = [args]
        for i in range(len(self.original)):
            if i == 0: continue
            self.deriv_1.append(i * self.original[i])
        for i in range(len(self.deriv_1)):
            if i == 0: continue
            self.deriv_2.append(i * self.deriv_1[i])
        for i in range(len(self.deriv_2)):
            if i == 0: continue
            self.deriv_3.append(i * self.deriv_2[i])

    def calc_original(self, x):
        to_return = 0
        for i in range(len(self.original)):
            to_return += self.original[i]* x **i
        return to_return
    def calc_deriv1(self, x):
        to_return = 0
        for i in range(len(self.deriv_1)):
            to_return += self.deriv_1[i] * x **i
        return to_return

    def calc_deriv2(self, x):
        to_return = 0
        for i in range(len(self.deriv_2)):
            to_return += self.deriv_2[i] * x **i
        return to_return

    def calc_deriv3(self, x):
        to_return = 0
        for i in range(len(self.deriv_3)):
            to_return = self.deriv_3 * x **i
        return to_return

    def calc_for_range(self, fun, min, max, inc):
        '''
        gibt ergebnisse als array zurück
        :param fun: calc funktion von classe Funktion
        :param min: untere grenze\n
        :param max: obere grenze\n
        :param inc: schritt größe\n
        :return: array der ergebnisse
        '''
        to_return_arr = []
        for i in range(min,max, inc):
            to_return_arr.append(fun(i))
        return to_return_arr