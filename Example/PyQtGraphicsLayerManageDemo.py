from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsItemGroup, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QRectF

class CustomItem(QGraphicsItem):
    def __init__(self):
        super().__init__()

    def boundingRect(self):
        return QRectF(0, 0, 100, 100)

    def paint(self, painter, option, widget):
        painter.drawRect(self.boundingRect())

class LayerManager:
    def __init__(self):
        self.scene = QGraphicsScene()
        self.layers = []
        self.buttons = []
        self.active_layer_index = -1
        self.selected_item = None

    def add_layer(self, layer_name, item=None):
        layer = QGraphicsItemGroup()
        layer.setFlag(QGraphicsItem.ItemIsSelectable, True)
        layer.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.scene.addItem(layer)
        self.layers.append(layer)

        if item is not None:
            layer.addToGroup(item)

        button = QPushButton(layer_name)
        button.setCheckable(True)
        button.setChecked(True)
        button.clicked.connect(lambda checked, layer_index=len(self.buttons): self.toggle_visibility(layer_index))
        self.buttons.append(button)

    def remove_layer(self, layer_index):
        if 0 <= layer_index < len(self.layers):
            layer = self.layers[layer_index]
            self.scene.removeItem(layer)
            self.layers.remove(layer)
            button = self.buttons[layer_index]
            self.buttons.remove(button)

    def get_layer(self, layer_index):
        if 0 <= layer_index < len(self.layers):
            return self.layers[layer_index]
        return None

    def set_active_layer(self, layer_index):
        if 0 <= layer_index < len(self.layers):
            for i, layer in enumerate(self.layers):
                layer.setZValue(i)
            active_layer = self.layers[layer_index]
            active_layer.setZValue(len(self.layers))
            self.active_layer_index = layer_index

    def get_active_layer(self):
        return self.active_layer_index

    def toggle_visibility(self, layer_index):
        if 0 <= layer_index < len(self.layers):
            layer = self.layers[layer_index]
            button = self.buttons[layer_index]
            layer.setVisible(button.isChecked())

    def mousePressEvent(self, event):
        if self.active_layer_index >= 0:
            item = self.scene.itemAt(event.scenePos(), self.scene.views()[0].transform())
            if item is not None and item.parentItem() == self.layers[self.active_layer_index]:
                self.selected_item = item
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.selected_item is not None:
            self.selected_item.setPos(event.scenePos())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.selected_item = None
        super().mouseReleaseEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    view = QGraphicsView()
    manager = LayerManager()

    manager.add_layer("Layer 1")
    manager.add_layer("Layer 2")
    manager.add_layer("Layer 3")

    item = CustomItem()

    for layer in manager.layers:
        item = CustomItem()
        layer.addToGroup(item)

    layout = QVBoxLayout()
    widget = QWidget()
    widget.setLayout(layout)

    for button in manager.buttons:
        layout.addWidget(button)

    view.setScene(manager.scene)
    layout.addWidget(view)
    widget.show()

    manager.set_active_layer(1)

    app.exec_()
