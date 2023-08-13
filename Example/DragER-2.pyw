import sys
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QApplication, QGraphicsItem
from PyQt5.QtCore import Qt, QRectF

class DemoGraphicsItem(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.isSelected = False
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return QRectF(-20, -20, 40, 40)

    def paint(self, painter, style_options, widget=None):
        if self.isSelected:
            painter.setBrush(Qt.red)
        else:
            painter.setBrush(Qt.blue)
        painter.drawEllipse(-20, -20, 40, 40)

    def hoverEnterEvent(self, event):
        self.setOpacity(0.5)

    def hoverLeaveEvent(self, event):
        self.setOpacity(1.0)

class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        if item and isinstance(item, DemoGraphicsItem):
            item.isSelected = not item.isSelected
            item.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QGraphicsView()
    scene = GraphicsScene()
    view.setScene(scene)
    view.show()

    # 添加一些DemoGraphicsItem
    for i in range(10):
        item = DemoGraphicsItem()
        item.setPos(i * 50, 50)
        scene.addItem(item)

    sys.exit(app.exec_())