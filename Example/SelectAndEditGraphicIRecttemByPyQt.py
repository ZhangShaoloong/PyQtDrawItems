import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter


class ItemDialog(QDialog):
    def __init__(self, item):
        super().__init__()

        self.item = item

        self.setWindowTitle("Change Item Size")
        layout = QVBoxLayout()

        width_label = QLabel("Width:")
        self.width_edit = QLineEdit(str(self.item.rect().width()))
        layout.addWidget(width_label)
        layout.addWidget(self.width_edit)

        height_label = QLabel("Height:")
        self.height_edit = QLineEdit(str(self.item.rect().height()))
        layout.addWidget(height_label)
        layout.addWidget(self.height_edit)

        self.resize_button = QPushButton("Resize")
        self.resize_button.clicked.connect(self.resize_item)
        layout.addWidget(self.resize_button)

        self.setLayout(layout)

    def resize_item(self):
        width = float(self.width_edit.text())
        height = float(self.height_edit.text())

        self.item.setRect(QRectF(0, 0, width, height))
        self.accept()


class GraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.rect_items = []
        for i in range(5):
            rect_item = QGraphicsRectItem(0, 0, 100, 100)
            rect_item.setPos(i * 120, 0)
            self.scene.addItem(rect_item)
            self.rect_items.append(rect_item)

        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRenderHint(QPainter.Antialiasing)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            for item in self.rect_items:
                item.setFlag(QGraphicsRectItem.ItemIsMovable, False)
                item.setFlag(QGraphicsRectItem.ItemIsSelectable, False)

            pos = self.mapToScene(event.pos())
            item = self.scene.itemAt(pos, self.transform())
            if isinstance(item, QGraphicsRectItem):
                item.setFlag(QGraphicsRectItem.ItemIsMovable, True)
                item.setFlag(QGraphicsRectItem.ItemIsSelectable, True)

        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        pos = self.mapToScene(event.pos())
        item = self.scene.itemAt(pos, self.transform())
        if isinstance(item, QGraphicsRectItem):
            dialog = ItemDialog(item)
            if dialog.exec_() == QDialog.Accepted:
                pass

        super().mouseDoubleClickEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    view = GraphicsView()
    view.show()

    sys.exit(app.exec_())
