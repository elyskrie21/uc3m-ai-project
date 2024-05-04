import sys
import matplotlib
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QScrollArea,
)

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigCanvas,
    NavigationToolbar2QT as NabToolbar,
)

matplotlib.use('Qt5Agg')


def runGui(fig):
    app = QApplication(sys.argv)
    window = MyApp(fig)
    sys.exit(app.exec_())


class MyApp(QWidget):
    def __init__(self, fig):
        super().__init__()
        self.title = 'AI Fuzzy Project'
        self.posXY = (700, 40)
        self.windowSize = (1200, 800)
        self.fig = fig
        self.initUI()

    def initUI(self):
        QMainWindow().setCentralWidget(QWidget())

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        canvas = FigCanvas(self.fig)
        canvas.draw()

        scroll = QScrollArea(self)
        scroll.setWidget(canvas)

        nav = NabToolbar(canvas, self)
        self.layout().addWidget(nav)
        self.layout().addWidget(scroll)

        self.show_basic()

    def show_basic(self):
        self.setWindowTitle(self.title)
        self.setGeometry(*self.posXY, *self.windowSize)
        self.show()
