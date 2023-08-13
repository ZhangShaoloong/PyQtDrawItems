import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QPushButton,QGraphicsLineItem
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPointF

class LineItem(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
        self.setPen(QPen(Qt.red, 2))

class GraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.current_line = None
        self.draw_enabled = True

        self.horizontal_button = QPushButton("Horizontal", self)
        self.horizontal_button.setCheckable(True)
        self.horizontal_button.clicked.connect(self.set_horizontal_mode)
        self.horizontal_button.setEnabled(False)

        self.vertical_button = QPushButton("Vertical", self)
        self.vertical_button.setCheckable(True)
        self.vertical_button.clicked.connect(self.set_vertical_mode)
        self.vertical_button.setEnabled(True)

        self.draw_button = QPushButton("Draw", self)
        self.draw_button.setCheckable(True)
        self.draw_button.clicked.connect(self.toggle_draw)
        self.draw_button.setChecked(True)

    def set_horizontal_mode(self):
        self.current_mode = "horizontal"
        self.horizontal_button.setEnabled(False)
        self.vertical_button.setEnabled(True)
        self.draw_button.setEnabled(True)

    def set_vertical_mode(self):
        self.current_mode = "vertical"
        self.horizontal_button.setEnabled(True)
        self.vertical_button.setEnabled(False)
        self.draw_button.setEnabled(True)

    def toggle_draw(self):
        if self.draw_button.isChecked():
            self.setDrawEnabled(False)
        else:
            self.setDrawEnabled(True)

    def setDrawEnabled(self, enabled):
        self.draw_enabled = enabled
        if enabled:
            self.draw_button.setText("Draw")
        else:
            self.draw_button.setText("Not Draw")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        button_width = self.horizontal_button.width()
        button_height = self.horizontal_button.height()
        view_width = self.viewport().width()
        view_height = self.viewport().height()
        self.horizontal_button.move(view_width - button_width - 10, 10)
        self.vertical_button.move(view_width - button_width - 10, 10 + button_height + 10)
        self.draw_button.move(view_width - button_width - 10, 10 + 2 * (button_height + 10))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.draw_enabled:
            start_pos = self.mapToScene(event.pos())
            self.current_line = LineItem(start_pos.x(), start_pos.y(), start_pos.x(), start_pos.y())
            self.scene.addItem(self.current_line)

    def mouseMoveEvent(self, event):
        if self.current_line is not None and self.draw_enabled:
            end_pos = self.mapToScene(event.pos())
            if self.current_mode == "horizontal":
                self.current_line.setLine(self.current_line.line().x1(), self.current_line.line().y1(),
                                          end_pos.x(), self.current_line.line().y2())
            elif self.current_mode == "vertical":
                self.current_line.setLine(self.current_line.line().x1(), self.current_line.line().y1(),
                                          self.current_line.line().x1(), end_pos.y())

    def mouseReleaseEvent(self, event):
        self.current_line = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = GraphicsView()
    view.show()
    sys.exit(app.exec_())
