import sys
from random import randint
from PyQt6.QtWidgets import (QApplication,
    QWidget,
    QLabel,
    QComboBox,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QVBoxLayout,
    QFormLayout)

from PyQt6.QtGui import (QIntValidator, QValidator)

DICE_SIDES = [3,4,5,6,7,8,10,12,14,16,20,24,30,100]
FATE_DICE = [1,1,0,0,-1,-1]

class QDiceSidesValidator(QValidator):
    def __init__(self, parent=None):
        super().__init__(parent)

    def validate(self, input_str, pos):
        if input_str.isdigit() and int(input_str) in DICE_SIDES:
            return (QValidator.State.Acceptable, input_str, pos)
        elif input_str == "":
            return (QValidator.State.Intermediate, input_str, pos)
        else:
            return (QValidator.State.Invalid, input_str, pos)

    def fixup(self):
        return ""

class Dice:
    n=1
    d=6
    fateState=False
    results=[]
    def __init__(self):
        pass

    def setN(self, num):
        self.n=int(num)

    def setD(self, sides):
        self.d=int(sides)

    def toggleFateState(self):
        self.fateState = not(self.fateState)
        if self.fateState:
            self.d=6

    def roll_dice(self):
        if self.fateState:
            self.results = [FATE_DICE[randint(0,5)] for _ in range(self.n)]
        else:
            self.results = [randint(1, self.d) for _ in range(self.n)]

class MainWindow(QWidget):

    dice = Dice()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Teeterpogger-Simple Dice Roller for TTRPGs')

        layout=QVBoxLayout()
        self.setLayout(layout)

        #input pane
        input_pane=QWidget(self)
        form_layout=QFormLayout()
        input_pane.setLayout(form_layout)

        fate_checkbox=QCheckBox('Using Fate/Fudge Dice?', self)
        fate_checkbox.stateChanged.connect(lambda: [self.dice.toggleFateState(), line_sides_dice.setCurrentText('6'), self.freezeUnfreezeInput(line_sides_dice)])
        
        line_num_dice=QComboBox()
        self._setup_inputs(line_num_dice)
        num_validator=QIntValidator(1,20,self)
        line_num_dice.setValidator(num_validator)
        line_num_dice.addItems(str(num) for num in range(1,21))
        line_num_dice.currentTextChanged.connect(lambda: [self.dice.setN(line_num_dice.currentText()), line_sides_dice.setFocus()])
        
        line_sides_dice=QComboBox()
        self._setup_inputs(line_sides_dice)
        sides_validator=QDiceSidesValidator()
        line_sides_dice.setValidator(sides_validator)
        line_sides_dice.addItems(str(s) for s in DICE_SIDES)
        line_sides_dice.currentTextChanged.connect(lambda: self.dice.setD(line_sides_dice.currentText()))

        form_layout.addWidget(fate_checkbox)
        form_layout.addRow('No.of dice: ', line_num_dice)
        form_layout.addRow('No. of sides on each dice: ', line_sides_dice)

        button=QPushButton("Roll Dice", self)
        button.clicked.connect(lambda: self.getDiceResults(result_label, sum_result_label))

        form_layout.addWidget(button)

        layout.addWidget(input_pane)

        #output pane
        output_pane=QWidget(self)
        result_layout=QVBoxLayout()
        output_pane.setLayout(result_layout)

        result_label=QLabel('Results:')
        sum_result_label=QLabel('Total:')

        result_layout.addWidget(result_label)
        result_layout.addWidget(sum_result_label)

        layout.addWidget(output_pane)

        self.show()
    
    def freezeUnfreezeInput(self, inputbox):
        if self.dice.fateState:
            inputbox.setEnabled(False)
            inputbox.setCurrentText('6')
        else:
            inputbox.setEnabled(True)


    def getDiceResults(self, result_label, sum_result_label):
        self.dice.roll_dice()        
        result_label.setText(f'Results: {self.dice.results}')
        sum_result_label.setText(f'Total: {sum(self.dice.results)}')

    def _setup_inputs(self,combobox):
        #combobox.setEditable(True)
        combobox.InsertPolicy=QComboBox.InsertPolicy.NoInsert

    

def main():
    app=QApplication(sys.argv)
    window=MainWindow()
    sys.exit(app.exec())

if __name__=='__main__':
    main()