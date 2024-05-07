import sys
import matplotlib
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from itertools import cycle

from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QComboBox,
    QPushButton,
    QLabel
)

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigCanvas,
    NavigationToolbar2QT as NabToolbar,
)

matplotlib.use('Qt5Agg')


def runGui(rulesGraphData, riskGraphData, riskGraphBasicData, applicationData, basicGraphs):
    app = QApplication(sys.argv)
    window = MyApp(rulesGraphData=rulesGraphData,
                   riskGraphData=riskGraphData,
                   riskGraphBasicData=riskGraphBasicData,
                   applicationData=applicationData,
                   basicGraphs=basicGraphs)
    sys.exit(app.exec_())


class MyApp(QWidget):
    def __init__(self, rulesGraphData, riskGraphData, riskGraphBasicData, applicationData, basicGraphs):
        super().__init__()
        self.title = 'AI Fuzzy Project'
        self.rulesGraphData = rulesGraphData
        self.riskGraphData = riskGraphData
        self.riskGraphBasicData = riskGraphBasicData
        self.applicationData = applicationData
        self.basicGraphs = basicGraphs
        self.applicationDataCanvas = FigCanvas(Figure(figsize=(8, 6)))
        self.basicGraphCanvas = FigCanvas(Figure(figsize=(8,18)))
        self.index = "1"
        self.label = QLabel()
        self.cycol = cycle('bgrcmk')
        self.initUI()

    def initUI(self):
        QMainWindow().setCentralWidget(QWidget())

        self.applicationDataCanvas.draw()

        data = QComboBox()
        data.currentIndexChanged.connect(self.activated)
        data.setMinimumHeight(30)

        for num in range(len(self.rulesGraphData)):
            data.addItem("Application ID: " + str(num + 1))

        scroll = QScrollArea(self)
        scroll.setWidget(self.basicGraphCanvas)

        applicationDataSCroll = QScrollArea(self)
        applicationDataSCroll.setWidget(self.applicationDataCanvas)

        nav = NabToolbar(self.basicGraphCanvas, self)

        basicGraphs = QVBoxLayout()
        basicGraphs.addWidget(nav)
        basicGraphs.addWidget(scroll)

        applicationSelectionButton = QPushButton("View Application")
        applicationSelectionButton.setMinimumHeight(30)
        applicationSelectionButton.setStyleSheet("background-color: red")
        applicationSelectionButton.clicked.connect(self.changeApplication)
        applicationSelectionButton.setMaximumWidth(100);

        applicationSelection = QHBoxLayout()
        applicationSelection.setContentsMargins(0, 10, 10, 0)
        applicationSelection.addWidget(data)
        applicationSelection.addWidget(applicationSelectionButton)

        applicationSelectionGraphs = QVBoxLayout()
        applicationSelectionGraphs.addWidget(applicationDataSCroll)

        initialData = self.applicationData.get(self.index)
        self.label.setText(
            "Age: " + str(initialData["age"]) + 
            "\nIncomeLevel: " + str(initialData["IncomeLevel"]) +
            "\nAssets: " + str(initialData["Assets"]) + 
            "\nAmount: " + str(initialData["Amount"]) +
            "\nJob: " + str(initialData["Job"]) +
            "\nHistory: " + str(initialData["History"]))
        font = self.font();
        font.setPointSize(10); 
        self.setFont(font); 

        applicationSelectionData = QVBoxLayout()
        applicationSelectionData.addWidget(self.label)

        applicationGraphs = QVBoxLayout()
        applicationGraphs.addLayout(applicationSelection)
        applicationGraphs.addLayout(applicationSelectionData)
        applicationGraphs.addLayout(applicationSelectionGraphs)

        layout1 = QHBoxLayout()
        layout1.addLayout(basicGraphs)
        layout1.addLayout(applicationGraphs)
        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.setSpacing(20)

        self.setLayout(layout1)
        self.showBasic()
        self.showBasicGraphs()
        self.showApplicationDataGraph()

    def showBasic(self):
        self.show()

    def activated(self, index):
        self.index = str(index + 1)

    def changeApplication(self):
        self.showApplicationDataGraph()

        newData = self.applicationData.get(self.index)
        self.label.setText(
            "Age: " + str(newData["age"]) + 
            "\nIncomeLevel: " + str(newData["IncomeLevel"]) +
            "\nAssets: " + str(newData["Assets"]) + 
            "\nAmount: " + str(newData["Amount"]) +
            "\nJob: " + str(newData["Job"]) +
            "\nHistory: " + str(newData["History"]))

    def showApplicationDataGraph(self):
        self.applicationDataCanvas.figure.clear()
        axs = self.applicationDataCanvas.figure.subplots(nrows=2)

        axs[0].set_title("Fuzzified Rule Application")
        for ruleData in self.rulesGraphData.get(self.index):
            color = next(self.cycol)
            axs[0].fill_between(ruleData[0], ruleData[2],
                                ruleData[3], facecolor=color, alpha=0.7)
            axs[0].plot(ruleData[0], ruleData[1], color,
                        linewidth=0.5, linestyle='--',)

        riskData = self.riskGraphData.get(self.index)
        axs[1].fill_between(riskData[0], riskData[1], riskData[2],
                            facecolor='Orange', alpha=0.7)
        axs[1].plot([riskData[3], riskData[3]], [0, riskData[4]],
                    'k', linewidth=1.5, alpha=0.9)
        axs[1].set_title('Aggregated risk membership and result (line)')

        for data in self.riskGraphBasicData:
            color = next(self.cycol)
            axs[1].plot(data[0], data[1], color,
                        linewidth=0.5, linestyle='--', )

        # Turn off top/right axes
        for ax in axs.flat:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()

        self.applicationDataCanvas.figure.tight_layout()
        self.applicationDataCanvas.draw() 

    def showBasicGraphs(self):
        self.basicGraphCanvas.figure.clear()
        axs = self.basicGraphCanvas.figure.subplots(nrows=7)
        for data in self.basicGraphs:
            match data["var"]:
                case "Age":
                    axs[0].plot(data["x"], data["y"], c=next(self.cycol),
                                linewidth=1.5, label=data["label"])
                    axs[0].set_title("AGE")
                    axs[0].legend()
                case "IncomeLevel":
                    axs[1].plot(data["x"], data["y"], c=next(self.cycol),
                                linewidth=1.5, label=data["label"])
                    axs[1].set_title("IncomeLevel")
                    axs[1].legend()
                case "Assets":
                    axs[2].plot(data["x"], data["y"], c=next(self.cycol),
                                linewidth=1.5, label=data["label"])
                    axs[2].set_title("Assets")
                    axs[2].legend()
                case "Amount":
                    axs[3].plot(data["x"], data["y"], c=next(self.cycol),
                                linewidth=1.5, label=data["label"])
                    axs[3].set_title("Amount")
                    axs[3].legend()
                case "Job":
                    axs[4].plot(data["x"], data["y"], c=next(self.cycol),
                                linewidth=1.5, label=data["label"])
                    axs[4].set_title("Job")
                    axs[4].legend()
                case "History":
                    axs[5].plot(data["x"], data["y"], c=next(self.cycol),
                                linewidth=1.5, label=data["label"])
                    axs[5].set_title("History")
                    axs[5].legend()
                case "Risk":
                    axs[6].plot(data["x"], data["y"], c=next(self.cycol),
                                linewidth=1.5, label=data["label"])
                    axs[6].set_title("Risk")
                    axs[6].legend()
                case _:
                    print("Unable to find axs to plot from for: " + data["var"])

        for ax in axs.flat:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()

        self.basicGraphCanvas.figure.tight_layout()
        self.basicGraphCanvas.draw()