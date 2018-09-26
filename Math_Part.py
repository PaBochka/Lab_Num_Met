# -*- coding: utf-8 -*-
import math
import pylab
from matplotlib import mlab
from matplotlib.figure import Figure
from label_for_graphic import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from main import MyWin
#######################################
class Math_Part(Ui_MainWindow):

    def bilding(self, n, L, I, h, x, R, w, E):
        eps = 0.00001
        print(L, R, I, h, x, n, E, w)
        self.tableWidget.setRowCount(n+1)
        for i in range(n+1):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))
        def abs_solution(x, I):
            return (((E * R * math.sin(w * x))/((L**2)*(w**2) + (R**2))) - ((E * L * w * math.cos(w * x))/((L**2)*(w**2) + (R**2))) + (sol_const(I) * math.exp((-(R * x)) / L)))
        def sol_const(I):
            return I + E * L * w / ((L**2)*(w**2) + (R**2))
        def f(x, I):
            return (E * (math.sin(w * x)) - R * I) / L

        def loc_err(step_I, two_step_I):
            return ((two_step_I - step_I) * ((8.0) / 7.0))

        def step_func1(step, x, I):
            return step * f(x, I)

        def step_func2(step, x, I):
            return step * f(x + step / 2, I + step_func1(step, x, I) / 2)

        def step_func3(step, x, I):
            return step * f(x + step, I + 2 * step_func2(step, x, I) - step_func1(step, x, I))

        def next_point_x(step, x):
            return x + step

        def next_point_I(I, x, step):
            return I + (step_func1(step, x, I) + 4 * step_func2(step, x, I) + step_func3(step, x, I)) / 6

        ##################################################
        def new_point(step, x, I, number_r):
            nonlocal h
            new_I = next_point_I(I, x, step)
            new_x = next_point_x(step, x)

            add_I = next_point_I(I, x, step / 2)
            add_x = next_point_x(step / 2, x)

            add_I = next_point_I(add_I, add_x, step / 2)
            add_x = next_point_x(step / 2, add_x)

            S = loc_err(new_I, add_I)

            self.tableWidget.setItem(number_r, 3, QtWidgets.QTableWidgetItem(str(add_I)))
            self.tableWidget.setItem(number_r, 4, QtWidgets.QTableWidgetItem(str(add_x)))
            self.tableWidget.setItem(number_r, 5, QtWidgets.QTableWidgetItem(str(h)))
            self.tableWidget.setItem(number_r, 6, QtWidgets.QTableWidgetItem(str(S)))

            print("S####: ", S)
            print("exp###: ", eps / 16, eps)
            print("####", h)
            if abs(S) >= eps / 16 and abs(S) <= eps:
                print("save point")
                return new_x, new_I
            if abs(S) < eps / 16:
                print("save point, but change step")
                h *= 2
                return new_x, new_I
            if abs(S) > eps:
                print("Fail")
                h /= 2
                return new_point(h, x, I, number_r)

        ax = self.figure.add_subplot(111)
        ax.axis([-10, 20, -10, 20])
        abs_x, abs_I, I0 = x, abs_solution(x, I), I
        for i in range(n):
            old_abs_x, old_abs_I = abs_x, abs_I
            self.tableWidget.setItem(i, 7, QtWidgets.QTableWidgetItem(str(old_abs_I)))
            self.tableWidget.setItem(i, 8, QtWidgets.QTableWidgetItem(str(old_abs_x)))
            old_x, old_I = x, I
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(old_I)))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(old_x)))
            x, I = new_point(h, old_x, old_I, i + 1)
            ax.plot([old_x, x], [old_I, I], '-b')
            abs_x = x
            abs_I = abs_solution(abs_x, I0)
            ax.plot([old_abs_x, abs_x], [old_abs_I, abs_I], '-r')
        self.tableWidget.setItem(n, 7, QtWidgets.QTableWidgetItem(str(abs_I)))
        self.tableWidget.setItem(n, 8, QtWidgets.QTableWidgetItem(str(abs_x)))
        self.tableWidget.setItem(n, 1, QtWidgets.QTableWidgetItem(str(I)))
        self.tableWidget.setItem(n, 2, QtWidgets.QTableWidgetItem(str(x)))
        ax.grid(True)
        self.canvas.draw()
        #координата х численного решения с некоторого шага отличается от координаты х
        #точного решения из - за пересчеста чтоки с учетом ЛП, т.е. в некоторый момент
        #в ЧР ЛП в некоторый момент > чем указанная окрустность => происходит пересчет
        #с корректировкой шага, но т.к. 1 в очереди считается коорд. х ТР то она ост.
        #с со значением шага полученным на пред. итерации => коорд. х ТР и ЧР отличны
        #поэтому целесообразно использовать в качестве коорд. х ТР - коорд. х ЧР)))))