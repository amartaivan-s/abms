import sys
from PyQt6 import QtWidgets
from view_pyqt import BoidQtViewer
from model import BoidFlockers  #Mesa Model

def main():
    params = dict(
        population=100,
        width=200,
        height=200,
        speed=3,
        vision=10,
        separation=2,
    )
    model = BoidFlockers(**params)

    app = QtWidgets.QApplication(sys.argv)
    viewer = BoidQtViewer(model=model, fps=50, point_size=3.0, swarm_radius=2.0)
    viewer.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


