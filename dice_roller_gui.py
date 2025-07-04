import sys
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
    QFormLayout,
    QGridLayout,
    QScrollArea)

from PyQt6.QtGui import (QIntValidator, QValidator, QFontDatabase, QIcon, QPixmap, QPainter)
from PyQt6.QtCore import Qt

from DiceRollerConsts import *
from CustomClasses import Dice

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



class MainWindow(QWidget):

    dice = Dice()
    per_die=False
    history=[]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName('mainWindow')
        self.display()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("images/parchment_light.jpg")
        if not pixmap.isNull():
            painter.drawPixmap(self.rect(), pixmap)
        super().paintEvent(event)

    def display(self):
        self.setWindowTitle('Teeterpogger-Simple Dice Roller for TTRPGs')
        self.setWindowIcon(QIcon("images/dice.png"))
        main_grid_layout=QGridLayout()
        self.setLayout(main_grid_layout)

        #I/O Pane
        io_pane=QWidget(self)
        io_pane.setObjectName("ioPane")
        io_layout=QVBoxLayout()
        io_pane.setLayout(io_layout)
        main_grid_layout.addWidget(io_pane,0,0)

        #history pane
        history_pane=QWidget(self)
        history_pane.setObjectName("historyPane")
        history_layout=QVBoxLayout()
        history_pane.setLayout(history_layout)

        history_title=QLabel("HISTORY")
        history_title.setObjectName('h3')
        history_layout.addWidget(history_title, alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignCenter)
        history_text=QLabel()   
        history_layout.addWidget(history_text, alignment=Qt.AlignmentFlag.AlignTop)
        clear_button=QPushButton("Clear History")
        clear_button.clicked.connect(lambda: [history_text.setText(""), self.history.clear()])
        history_layout.addWidget(clear_button, alignment=Qt.AlignmentFlag.AlignBottom)

        history_scroll_area=QScrollArea()
        history_scroll_area.setObjectName("historyScrollArea")
        history_scroll_area.setWidgetResizable(True)
        history_scroll_area.setWidget(history_pane)
        history_scroll_area.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_grid_layout.addWidget(history_scroll_area, 0, 1)

        #input pane
        input_pane=QWidget(io_pane)
        form_layout=QFormLayout()
        input_pane.setLayout(form_layout)

        fate_checkbox=QCheckBox('Using Fate/Fudge Dice?', self)
        fate_checkbox.stateChanged.connect(lambda: [self.dice.toggleFateState(), line_sides_dice.setCurrentText('6'), self.freezeUnfreezeInput(line_sides_dice)])
        
        line_num_dice=QComboBox()
        num_validator=QIntValidator(1,20,self)
        line_num_dice.setValidator(num_validator)
        line_num_dice.addItems(str(num) for num in range(1,21))
        line_num_dice.currentTextChanged.connect(lambda: [self.dice.setN(line_num_dice.currentText()), line_sides_dice.setFocus()])
        
        line_sides_dice=QComboBox()
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
        button.clicked.connect(lambda: self.getDiceResults(result_label, sum_result_label, history_text, int(modifier_input.value())))

        form_layout.addWidget(button)

        io_layout.addWidget(input_pane, alignment=Qt.AlignmentFlag.AlignTop)

        #output pane
        output_pane=QWidget(io_pane)
        result_layout=QVBoxLayout()
        output_pane.setLayout(result_layout)

        result_label=QLabel('Rolls:')
        sum_result_label=QLabel('Total:')

        result_layout.addWidget(result_label)
        result_layout.addWidget(sum_result_label)

        io_layout.addWidget(output_pane,alignment=Qt.AlignmentFlag.AlignTop)

        self.show()
    
    def freezeUnfreezeInput(self, inputbox):
        if self.dice.fateState:
            inputbox.setEnabled(False)
            inputbox.setCurrentText('6')
        else:
            inputbox.setEnabled(True)


    def getDiceResults(self, result_label, sum_result_label, history_label, modifier=0):
        self.dice.roll_dice()
        times=1
        if self.per_die:
            times=len(self.dice.results)
        total=sum(self.dice.results)+(modifier*times)       
        result_label.setText(f'Rolls: {self.dice.results}')
        sum_result_label.setText(f'Total: {total}')
        self.updateHistory(total, modifier, history_label)

    def setPerDie(self, rb):
        if rb.isChecked():
            self.per_die=True
        else:
            self.per_die=False
     
    def updateHistory(self, recent_total, recent_mod, history_label):
        #recent_tuple = (roll input, roll results, total) all strings
        n=str(self.dice.n)
        if self.dice.fateState:
            d='F'
        else:
            d=str(self.dice.d)
        #construct the first string of the new tuple to be added to history, i.e. roll input
        recent_roll_input=''
        mod_string=''
        if recent_mod>0:
            mod_string=f'+{str(recent_mod)}'
        elif recent_mod<0:
            mod_string=f'{str(recent_mod)}'

        if self.per_die:
            recent_roll_input=f'{n}(d{d}{mod_string})' # per die: 4(d6+mod) or dF
        else:
            recent_roll_input=f'{n}d{d}{mod_string}' # per roll: 4d6 + mod or dF

        recent_tuple=(recent_roll_input, self.dice.results, recent_total)
        self.history.append(recent_tuple)
        # Update the history pane display
        history_text = ""
        old_text=history_label.text()
        for entry in self.history[::-1]:
            roll_input, results, total = entry
            history_text += f"You rolled:\n{roll_input}: {total}\t{results}\n"
        
        #history_text+=old_text
        history_label.setText(history_text)

    

def main():
    app=QApplication(sys.argv)
    window=MainWindow()
    window.setObjectName("mainWindow")
    window.resize(600, 400)

    QFontDatabase.addApplicationFont("Fonts/Eczar-VariableFont_wght.ttf")
    QFontDatabase.addApplicationFont("Fonts/Grenze-Regular.ttf")
    with open('stylesheet.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)
    sys.exit(app.exec())

if __name__=='__main__':
    main()