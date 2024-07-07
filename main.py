import sys
import io
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QHBoxLayout,
    QVBoxLayout, QWidget, QFrame, QScrollArea, QSpinBox, QDoubleSpinBox
)
#from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sklearn.linear_model import LinearRegression
import subprocess

# Run data_import.py using subprocess
result = subprocess.run(['python', 'data_import.py'], capture_output=True, text=True)

# Print the output of data_import.py
print(result.stdout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Save Your Heart")
        
        self.neutralize_flag = False
        self.data = None
        self.model = LinearRegression()
        
        parent_widget = QWidget()        
        self.setCentralWidget(parent_widget)
        self.parent_layout = QVBoxLayout()
        parent_widget.setLayout(self.parent_layout)

        
        self.load_button = QPushButton("Load CSV")
        self.load_button.clicked.connect(self.load_data)
        self.parent_layout.addWidget(self.load_button)
        
        self.child_widget = QWidget(parent_widget)
        #self.nested_frame = QFrame()
        #self.nested_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.child_layout = QVBoxLayout()
        self.child_widget.setLayout(self.child_layout)
        self.parent_layout.addWidget(self.child_widget)

        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.parent_layout.addWidget(self.scroll_area)
        self.scroll_area.setWidget(self.child_widget)
        

        self.child_widget.setVisible(False)

        self.structure = QLabel("")
        self.summary = QLabel("")

        # first input widget that changes the feature variable
        self.input1 = QDoubleSpinBox() 
        self.input1.setRange(0.0, 80.0)
        self.input1.setSingleStep(0.1)
        self.input1.valueChanged.connect(self.update_prediction)


        self.h_layout1 = QHBoxLayout()
        self.h_layout1.addWidget(self.input1)
        self.h_layout1.addWidget(QLabel("BIKING (hours per month)"))
        self.h_layout1.addStretch()
        
        # second input widget that changes the feature variable
        self.input2 = QSpinBox()
        self.input2.setRange(0, 40)
        self.input2.valueChanged.connect(self.update_prediction)
        # third input widget that changes the feature variable
        self.neutralize = QPushButton("Neutralize with biking")
        self.neutralize.clicked.connect(self.neutralize_with_biking)
        

        self.h_layout2 = QHBoxLayout()
        self.h_layout2.addWidget(self.input2)
        self.h_layout2.addWidget(QLabel("SMOKING (cigarettes per day)"))
        self.h_layout2.addWidget(self.neutralize)
        self.h_layout2.addStretch()
        
        self.h_layout3 = QHBoxLayout()
        self.prediction_value = QLabel("")
        self.prediction_label = QLabel("Probability of heart disease: ")
        self.h_layout3.addWidget(self.prediction_label)
        
        self.h_layout3.addWidget(self.prediction_value)


        self.subtitle = QLabel("*Assumed baseline probability of heart disease is H% (person does not exercise and eats unhealthy food)")
        self.child_layout.addWidget(self.subtitle)
        self.child_layout.addLayout(self.h_layout1)
        self.child_layout.addLayout(self.h_layout2)
        self.child_layout.addLayout(self.h_layout3)

        
        
        # self.input3 = QLineEdit()
        # self.input3.textChanged.connect(self.update_prediction)
        # self.child_layout.addWidget(self.input3)
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)        
        self.parent_layout.addWidget(self.canvas)
        
        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        #line1.setFrameShadow(QFrame.Shadow.Sunken)
        self.child_layout.addWidget(line1)
        
        self.child_layout.addWidget(QLabel("DataFrame Structure"))
        self.child_layout.addWidget(self.structure)
        self.child_layout.addWidget(QLabel("Statistical Summary"))
        self.child_layout.addWidget(self.summary)

        

    def load_data(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        
        if file_path:
            self.data = pd.read_csv(file_path)
            buffer = io.StringIO()
            self.data.info(buf=buffer)
            #info_df = self.parseInfoToDataFrame(buffer.getvalue())
            self.structure.setText(buffer.getvalue())
            self.summary.setText(self.data.describe().to_html(index=True))            
            self.update_prediction()
    
    def neutralize_with_biking(self):
        X = self.data[['heart.disease', 'smoking']].values
        y = self.data['biking'].values 
        self.model.fit(X, y)
        
        input1_value = 15
        input2_value = self.input2.value()
        
        prediction = self.model.predict([[input1_value, input2_value]]) 
        self.input1.setValue(round(prediction[0],1))
        self.neutralize_flag = True        
        self.update_prediction()
         

    def update_prediction(self):
        if self.data is None:
            return
        
        self.child_widget.setVisible(True)
        
        X = self.data[['biking', 'smoking']].values
        y = self.data['heart.disease'].values
        self.model.fit(X, y)
        
        if self.neutralize_flag is False:
            self.input1.setStyleSheet("color: black; font-weight: normal; background-color: white;")
        else:
            self.input1.setStyleSheet("color: white; font-weight: bold; background-color: green;")
            self.neutralize_flag = False            

        input1_value = self.input1.value()
        input2_value = self.input2.value()
        
        prediction = self.model.predict([[input1_value, input2_value]]) 
        prediction[0] = round(prediction[0],1) - 15
        self.figure.clear()
        ax = self.figure.add_subplot(111) # Add subplot 111 means 1x1 grid, first subplot
        #baseline adjusted data
        data_adjusted = [i-15 for i in self.data['heart.disease']]
        ax.plot(self.data['biking'], data_adjusted, 'bo')
        ax.plot(input1_value, prediction, 'ro')
        #ax.set_title("Probability of getting heart disease")
        ax.set_xlabel("Biking (hours per month)")
        ax.set_ylabel("Increased probability of heart disease (%)")
        
        
        self.prediction_label.setStyleSheet("font-weight: bold;")
        
        self.h_layout3.addStretch()
       
        prediction = round(prediction[0],1)
        self.prediction_value.setText(f"H + {prediction}%")
        if prediction < 0:
                self.prediction_value.setText(f"H {prediction}%")
        self.prediction_value.setStyleSheet("color: red; font-weight: bold;")
        
        self.canvas.draw()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
