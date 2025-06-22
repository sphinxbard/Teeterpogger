import sys
from random import randint
from PyQt6.QtWidgets import (QApplication,
    QWidget,
    QLabel,
    QComboBox,
    QSpinBox,
    QCheckBox,
    QButtonGroup,
    QRadioButton,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout)

from PyQt6.QtGui import (QIntValidator, QValidator)

DICE_SIDES = [3,4,5,6,7,8,10,12,14,16,20,24,30,100]
FATE_DICE = [1,1,0,0,-1,-1]
INT_MIN=-2147483648
INT_MAX=2147483647

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
    per_die=False

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

        modifier_input=QSpinBox()
        modifier_input.setRange(INT_MIN, INT_MAX)
        modifier_input.setValue(0)

        modifier_type=QButtonGroup()
        rb_per_roll=QRadioButton('Per Roll', self)
        rb_per_die=QRadioButton('Per Die', self)
        modifier_type.addButton(rb_per_roll,1)
        modifier_type.addButton(rb_per_die,2)
        rb_per_roll.setChecked(True)
        rb_per_die.toggled.connect(lambda: self.setPerDie(rb_per_die))
        modifier_type_layout = QHBoxLayout()
        modifier_type_layout.addWidget(rb_per_roll)
        modifier_type_layout.addWidget(rb_per_die)
        
        form_layout.addWidget(fate_checkbox)
        form_layout.addRow('No.of dice: ', line_num_dice)
        form_layout.addRow('No. of sides on each dice: ', line_sides_dice)
        form_layout.addRow('Modifier: ', modifier_input)        
        form_layout.addRow('Modifier Type: ', modifier_type_layout)

        button=QPushButton("Roll Dice", self)
        button.clicked.connect(lambda: self.getDiceResults(result_label, sum_result_label, int(modifier_input.value())))

        form_layout.addWidget(button)

        layout.addWidget(input_pane)

        #output pane
        output_pane=QWidget(self)
        result_layout=QVBoxLayout()
        output_pane.setLayout(result_layout)

        result_label=QLabel('Rolls:')
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


    def getDiceResults(self, result_label, sum_result_label, modifier=0):
        self.dice.roll_dice()
        times=1
        if self.per_die:
            times=len(self.dice.results)
        total=sum(self.dice.results)+(modifier*times)       
        result_label.setText(f'Rolls: {self.dice.results}')
        sum_result_label.setText(f'Total: {total}')

    def setPerDie(self, rb):
        if rb.isChecked():
            self.per_die=True
        else:
            self.per_die=False

    def _setup_inputs(self,combobox):
        #combobox.setEditable(True)
        combobox.InsertPolicy=QComboBox.InsertPolicy.NoInsert

    

def main():
    app=QApplication(sys.argv)
    window=MainWindow()
    sys.exit(app.exec())

if __name__=='__main__':
    main()