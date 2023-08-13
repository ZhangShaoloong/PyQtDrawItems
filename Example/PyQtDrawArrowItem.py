from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsLineItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QPainter, QPolygonF
import math

class ArrowItem(QGraphicsLineItem):
    def __init__(self, start, end, parent=None):
        super().__init__(parent)
        self.setLine(start.x(), start.y(), end.x(), end.y())
        self.arrow_head_size = 30

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制箭头线
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(self.line())

        # 计算箭头的方向向量
        direction = self.line().p2() - self.line().p1()
        direction_length = math.sqrt(direction.x()**2 + direction.y()**2)
        if direction_length > 0:
            direction /= direction_length

        # 计算箭头的两个侧面向量
        side_vector1 = QPointF(-direction.y(), direction.x())
        side_vector2 = QPointF(direction.y(), -direction.x())

        # 计算箭头的三个顶点
        left_arrow_points = QPolygonF()
        left_arrow_points.append(self.line().p2())
        left_arrow_points.append(self.line().p2() - direction * self.arrow_head_size)
        left_arrow_points.append(self.line().p2() - direction * self.arrow_head_size + side_vector1 * self.arrow_head_size * 0.3)
        
        right_arrow_points = QPolygonF()
        right_arrow_points.append(self.line().p2() - direction * self.arrow_head_size + side_vector2 * self.arrow_head_size * 0.3)
        right_arrow_points.append(self.line().p2() - direction * self.arrow_head_size)
        right_arrow_points.append(self.line().p2())

        # 绘制箭头
        painter.setPen(QPen(Qt.black))
        painter.setBrush(Qt.black)
        painter.drawPolygon(left_arrow_points)
        painter.drawPolygon(right_arrow_points)

class ArrowView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.start_point = None
        self.current_arrow = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = self.mapToScene(event.pos())
            self.current_arrow = ArrowItem(self.start_point, self.start_point)
            self.scene().addItem(self.current_arrow)

    def mouseMoveEvent(self, event):
        if self.start_point is not None:
            end_point = self.mapToScene(event.pos())
            self.current_arrow.setLine(self.start_point.x(), self.start_point.y(), end_point.x(), end_point.y())
            self.current_arrow.update()

    def mouseReleaseEvent(self, event):
        self.start_point = None
        self.current_arrow = None

if __name__ == "__main__":
    app = QApplication([])

    scene = QGraphicsScene()
    view = ArrowView(scene)

    view.show()

    app.exec_()
