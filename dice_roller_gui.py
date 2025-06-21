import sys
from random import randint
from PyQt6.QtWidgets import (QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QFormLayout)

class Dice:
    n=1
    d=6
    results=[]
    def __init__(self):
        pass

    def setN(self, num):
        self.n=num

    def setD(self, sides):
        self.d=sides

    def roll_dice(self):
        self.results = [randint(1, self.d) for _ in range(self.n)]

class MainWindow(QWidget):

    dice = Dice()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Teeterpogger-Simple Dice Roller for TTRPGs')

        layout=QHBoxLayout()
        self.setLayout(layout)

        #input pane
        input_pane=QWidget(self)
        form_layout=QFormLayout()
        input_pane.setLayout(form_layout)

        line_num_dice=QLineEdit()
        line_num_dice.returnPressed.connect(self.dice.setN(line_num_dice.text))
        line_sides_dice=QLineEdit()
        line_sides_dice.returnPressed.connect(self.dice.setD(line_sides_dice.text))

        form_layout.addRow('No.of dice: ', line_num_dice)
        form_layout.addRow('No. of sides on each dice: ', line_sides_dice)

        button=QPushButton()
        button.clicked.connect(self.dice.roll_dice)

        form_layout.addWidget(button)

        layout.addWidget(input_pane)

        #output pane
        output_pane=QWidget(self)
        result_layout=QHBoxLayout()
        output_pane.setLayout(result_layout)

        result_label=QLabel(f'Results: {self.dice.results}')
        sum_result_label=QLabel(f'Total: {sum(self.dice.results)}')

        result_layout.addWidget(result_label)
        result_layout.addWidget(sum_result_label)

        self.show()

    

def main():
    app=QApplication(sys.argv)
    window=MainWindow()
    sys.exit(app.exec())

if __name__=='__main__':
    main()