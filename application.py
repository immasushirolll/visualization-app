import sys
import pandas as pd
import recommend
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QSizePolicy, QLabel,QPushButton,QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


#READS THE DATA
df = pd.read_csv('fraud_only.csv')

#TAKES RECOMMENDATIONS AS A LIST
liste = recommend.predict_most_influential_feature()


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class DataDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Data Visualization Dashboard")
        self.setGeometry(100, 100, 800, 800)

        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        
        
        self.layout = QVBoxLayout(self.central_widget)
        
        #LABELS
        self.title_label = QLabel("Frequency of Fraud according to given parameter")
        self.title_label.setStyleSheet("font-size: 30px; font-weight: bold; color: black;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.altyazi = QLabel("Recommended parameters to look at are: " + self.returnItems() )
        self.altyazi.setStyleSheet("font-size: 18px; font-weight: italic; color: red;")
        self.button_layout = QHBoxLayout()
        
    
        # ADDING BUTTONS FOR EVERY RECOMMENDATION  
        listWithout = self.returnListWithout()
        for s in listWithout:
            name = "button" + s
            self.name = QPushButton(s)
            self.name.clicked.connect(self.buton_clicked) 
            self.name.setMaximumWidth(250)
            self.name.setStyleSheet("background-color: red; color: white; font-size: 16px; font-weight: bold;")
            self.button_layout.addWidget(self.name)


        
        self.layout.addWidget(self.title_label) 
        self.layout.addWidget(self.altyazi) 
        
        self.layout.addLayout(self.button_layout)
        
        # Create a dropdown menu for y-axis
        self.y_dropdown = QComboBox()
        self.y_dropdown.addItems(df.columns)
        self.y_dropdown.setMinimumHeight(35)
        self.y_dropdown.currentTextChanged.connect(self.update_graph)
        self.layout.addWidget(self.y_dropdown)

        
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        self.layout.addWidget(self.canvas)

        # Initial graph
        self.update_graph()
    
    #CHANGES THE GRAPH FOR EACH BUTTON
    def buton_clicked(self):
         button = app.sender()
         button_name = button.text()
         self.y_dropdown.setCurrentText(button_name)      
    
    #RETURNS EVERY RECOMMENDATION
    def returnItems(self):
        a = ""
        for s in liste:
             a += s + ", "        
        return a[0:len(a)-2]
    
    #RETURNS LIST WITHOUT DUPLICATES AND INDEXES FOR THE BUTTONS
    def returnListWithout(self):
        a = []
        for s in liste:
            a.append(s[0:s.index('_')])
        m =[]
        for element in a:
            if element not in m:
                m.append(element) 
        return m
    
    def update_graph(self):
        y_column = self.y_dropdown.currentText()

        self.canvas.axes.clear()
        if y_column == "VehicleCategory" or y_column == "CarsInvolved" or y_column == "AddressChange" :
            self.canvas.axes.hist(df[y_column],ec = "black",color="red")
            self.y_dropdown.setStyleSheet("color: red; font-size: 18px;")
        else:
            self.canvas.axes.hist(df[y_column],ec = "black",color="blue")
            self.y_dropdown.setStyleSheet("color: blue; font-size: 18px; ")

        
        
        self.canvas.axes.set_ylabel("Number Of Frauds")  
        self.canvas.axes.set_xlabel(y_column)
        

        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = DataDashboard()
    dashboard.show()
    sys.exit(app.exec_())
