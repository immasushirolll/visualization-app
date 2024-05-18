import sys
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QSizePolicy, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


df = pd.read_csv('fraud_only.csv')




class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class DataDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Data Visualization Dashboard")
        self.setGeometry(100, 100, 800, 600)

        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        
        self.layout = QVBoxLayout(self.central_widget)
         
        self.title_label = QLabel("Frequency of Fraud according to given parameter")
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: black;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label) 
        # Create a dropdown menu for y-axis
        self.y_dropdown = QComboBox()
        self.y_dropdown.addItems(df.columns)
        self.y_dropdown.currentTextChanged.connect(self.update_graph)
        self.layout.addWidget(self.y_dropdown)

        
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        self.layout.addWidget(self.canvas)

        # Initial graph
        self.update_graph()

    def update_graph(self):
        y_column = self.y_dropdown.currentText()

        self.canvas.axes.clear()
        self.canvas.axes.hist(df[y_column],ec = "black",color="blue")
        
        
        self.canvas.axes.set_ylabel("Number Of Frauds")  
        self.canvas.axes.set_xlabel(y_column)
        

        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = DataDashboard()
    dashboard.show()
    sys.exit(app.exec_())