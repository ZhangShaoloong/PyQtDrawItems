from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget,QCheckBox,QGraphicsLineItem
from PyQt5.QtGui import QPen, QColor, QPainter, QCursor
from PyQt5.QtCore import Qt, QLineF, QPointF

class GridScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 500, 500)

        self.grid_visible = True
        self.grid_color = QColor(200, 200, 200)

        self.ruler_pen = QPen(Qt.red)
        self.ruler_pen.setWidth(2)

        self.horizontal_ruler = QGraphicsLineItem(0, 0, self.width(), 0)
        self.horizontal_ruler.setPen(self.ruler_pen)
        self.addItem(self.horizontal_ruler)

        self.vertical_ruler = QGraphicsLineItem(0, 0, 0, self.height())
        self.vertical_ruler.setPen(self.ruler_pen)
        self.addItem(self.vertical_ruler)

        self.horizontal_cursor = QGraphicsLineItem(0, 0, self.width(), 0)
        self.horizontal_cursor.setPen(self.ruler_pen)
        self.addItem(self.horizontal_cursor)

        self.vertical_cursor = QGraphicsLineItem(0, 0, 0, self.height())
        self.vertical_cursor.setPen(self.ruler_pen)
        self.addItem(self.vertical_cursor)

    def toggle_grid_visibility(self, checked):
        self.grid_visible = checked
        self.update()

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        if self.grid_visible:
            left = int(rect.left()) - (int(rect.left()) % 10)
            top = int(rect.top()) - (int(rect.top()) % 10)
            lines = []

            x = left
            while x < rect.right():
                lines.append(QLineF(x, rect.top(), x, rect.bottom()))
                x += 10

            y = top
            while y < rect.bottom():
                lines.append(QLineF(rect.left(), y, rect.right(), y))
                y += 10

            pen = QPen(self.grid_color)
            painter.setPen(pen)

            for line in lines:
                painter.drawLine(line)

            self.horizontal_ruler.setLine(rect.left(), rect.top(), rect.right(), rect.top())
            self.vertical_ruler.setLine(rect.left(), rect.top(), rect.left(), rect.bottom())

    def update_cursor_positions(self, event):
        mouse_pos = self.views()[0].mapToScene(event.pos())
        self.horizontal_cursor.setLine(self.horizontal_ruler.line().x1(), mouse_pos.y(), self.horizontal_ruler.line().x2(), mouse_pos.y())
        self.vertical_cursor.setLine(mouse_pos.x(), self.vertical_ruler.line().y1(), mouse_pos.x(), self.vertical_ruler.line().y2())



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grid Demo")
        self.setGeometry(100, 100, 500, 500)

        self.grid_scene = GridScene()
        self.grid_view = QGraphicsView(self.grid_scene)
        self.grid_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.grid_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.checkbox = QCheckBox("Show Grid")
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(self.grid_scene.toggle_grid_visibility)

        layout = QVBoxLayout()
        layout.addWidget(self.grid_view)
        layout.addWidget(self.checkbox)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.grid_view.mouseMoveEvent = self.grid_scene.update_cursor_positions

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
