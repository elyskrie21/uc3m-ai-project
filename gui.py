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
    QPushButton
)

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigCanvas,
    NavigationToolbar2QT as NabToolbar,
)

matplotlib.use('Qt5Agg')


def runGui(rulesGraphData, riskGraphData, fig):
    app = QApplication(sys.argv)
    window = MyApp(rulesGraphData=rulesGraphData,
                   riskGraphData=riskGraphData, fig=fig)
    sys.exit(app.exec_())


class MyApp(QWidget):
    def __init__(self, rulesGraphData, riskGraphData, fig):
        super().__init__()
        self.title = 'AI Fuzzy Project'
        self.fig = fig
        self.rulesGraphData = rulesGraphData
        self.riskGraphData = riskGraphData
        self.cycol = cycle('bgrcmk')
        self.initUI()

    def initUI(self):
        QMainWindow().setCentralWidget(QWidget())

        canvas = FigCanvas(self.fig)
        canvas.draw()

        applicationDataCanvas = FigCanvas(Figure(figsize=(8, 6)))
        applicationDataCanvas.draw()

        data = QComboBox()
        data.setMaximumHeight(50)

        for num in range(len(self.rulesGraphData)):
            data.addItem("Application ID: " + str(num))

        scroll = QScrollArea(self)
        scroll.setWidget(canvas)

        applicationDataSCroll = QScrollArea(self)
        applicationDataSCroll.setWidget(applicationDataCanvas)

        nav = NabToolbar(canvas, self)

        basicGraphs = QVBoxLayout()
        basicGraphs.addWidget(nav)
        basicGraphs.addWidget(scroll)

        applicationSelectionButton = QPushButton("View Application")

        applicationSelection = QHBoxLayout()
        applicationSelection.addWidget(data)
        applicationSelection.addWidget(applicationSelectionButton)

        applicationSelectionGraphs = QVBoxLayout()
        applicationSelectionGraphs.addWidget(applicationDataSCroll)

        applicationGraphs = QVBoxLayout()
        applicationGraphs.addLayout(applicationSelection)
        applicationGraphs.addLayout(applicationSelectionGraphs)

        layout1 = QHBoxLayout()
        layout1.addLayout(basicGraphs)
        layout1.addLayout(applicationGraphs)
        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.setSpacing(20)

        self.setLayout(layout1)
        self.showBasic()
        self.showApplicationDataGraph(canvas=applicationDataCanvas)

    def showBasic(self):
        self.show()

    def showApplicationDataGraph(self, canvas):
        # canvas.axes.cla()
        axs = canvas.figure.subplots(nrows=2)
        for ruleData in self.rulesGraphData.get("1"):
            color = next(self.cycol)
            axs[0].fill_between(ruleData[0], ruleData[2],
                                ruleData[3], facecolor=color, alpha=0.7)
            axs[0].plot(ruleData[0], ruleData[1], color,
                        linewidth=0.5, linestyle='--',)

        riskData = self.riskGraphData.get("1")
        axs[1].fill_between(riskData[0], riskData[1], riskData[2],
                            facecolor='Orange', alpha=0.7)
        axs[1].plot([riskData[3], riskData[3]], [0, riskData[4]],
                    'k', linewidth=1.5, alpha=0.9)
        axs[1].set_title('Aggregated membership and result (line)')

        # Turn off top/right axes
        for ax in axs.flat:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()
        canvas.draw()
