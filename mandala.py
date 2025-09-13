#Importacion de modulos necesarios
import sys
import math
from PyQt5.QtWidgets import * 

from PyQt5.QtGui import *
from PyQt5.QtCore import *

#Clase personalizada para el lienzo deonde se dibujan las figuras
class MandalaCanvas(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 600, 600) #Define el tamaño del area de dibujo

    def deleteSelected(self):
        #Elimina los elementos seleccionados en el lienzo
        for item in self.selectedItems():
            self.removeItem(item)

#Clase principal de la aplicacion
class MandalaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mandals Interactivas") #Titulo de la ventana
        self.setGeometry(100, 100, 850, 700) #Tamaño de la ventana
        self.color = QColor("blue") #Color inicial del contorno
        self.init_ui() # Inicializa la interfaz

    def init_ui(self):
        main_layout = QHBoxLayout() #Layout principal horizontal
        
        #Crear el lienzo y la vista
        self.scene = MandalaCanvas() #Instancia del lienzo
        self.view = QGraphicsView(self.scene) #Vista para mostrar el lienzo
        self.view.setStyleSheet("background-color: white;") #Color de fondo del lienzo
        self.view.setDragMode(QGraphicsView.RubberBandDrag) #Permite seleccionar multiples elementos
        main_layout.addWidget(self.view, stretch=3) #Agrega la vista al layout principal

        #Panel lateral de controles
        control_panel = QVBoxLayout()

        #Grupo de seleccion de figura
        shape_group = QGroupBox("Figura")
        shape_layout = QVBoxLayout()
        self.shape_combo = QComboBox() #Menu desplegable para elegir la figura
        self.shape_combo.addItems(["Círculo", "Estrella", "Pétalo"]) #Opciones disponibles
        shape_layout.addWidget(QLabel("Tipo:")) #Etiqueta
        shape_layout.addWidget(self.shape_combo) #Agrega el menu al layout
        shape_group.setLayout(shape_layout)
        control_panel.addWidget(shape_group)

        #Grupo de parametros de dibujo
        param_group = QGroupBox("Parametros")
        param_layout = QVBoxLayout()
        self.rep_spin = QSpinBox() #Selector de numero de repeticiones
        self.rep_spin.setRange(4, 100)
        self.rep_spin.setValue(12)
        self.size_spin = QSpinBox() #Selector de tamaño
        self.size_spin.setRange(10, 200)
        self.size_spin.setValue(60)
        param_layout.addWidget(QLabel("Repeticiones:"))
        param_layout.addWidget(self.rep_spin)
        param_layout.addWidget(QLabel("Tamaño:"))
        param_layout.addWidget(self.size_spin)
        param_group.setLayout(param_layout)
        control_panel.addWidget(param_group)

        #Grupo de seleccion de color
        color_group = QGroupBox("Color del contorno")
        color_layout = QVBoxLayout()
        color_btn = QPushButton("Seleccionar color") #Boton para abrir el dialogo de color
        color_btn.clicked.connect(self.choose_color)
        color_layout.addWidget(color_btn)
        color_group.setLayout(color_layout)
        control_panel.addWidget(color_group)

        #Grupo de acciones (dibujar y borrar)
        action_group = QGroupBox("Acciones")
        action_layout = QVBoxLayout()
        draw_btn = QPushButton("Dibujar figura") #Boton para dibujar la figura
        draw_btn = QPushButton("🖌️ Dibujar figura")  # Botón para dibujar
        draw_btn.clicked.connect(self.draw_mandala)
        delete_btn = QPushButton("🗑️ Borrar figuras seleccionadas")  # Botón para borrar
        delete_btn.clicked.connect(self.scene.deleteSelected)
        action_layout.addWidget(draw_btn)
        action_layout.addWidget(delete_btn)
        action_group.setLayout(action_layout)
        control_panel.addWidget(action_group)

        # Añade el panel de controles al layout principal
        main_layout.addLayout(control_panel, stretch=1)
        self.setLayout(main_layout)

    def choose_color(self):
        # Abre un diálogo para seleccionar color
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color  # Guarda el color seleccionado

    def draw_mandala(self):
        # Dibuja una figura repetida en forma de mandala
        reps = self.rep_spin.value()  # Número de repeticiones
        size = self.size_spin.value()  # Tamaño de cada figura
        shape = self.shape_combo.currentText()  # Tipo de figura seleccionada
        center = QPointF(300, 300)  # Centro del mandala

        for i in range(reps):
            angle = 360 / reps * i  # Ángulo de rotación para cada figura
            rad = math.radians(angle)
            dx = math.cos(rad) * 100  # Desplazamiento en X
            dy = math.sin(rad) * 100  # Desplazamiento en Y
            pos = QPointF(center.x() + dx, center.y() + dy)  # Posición final

            # Crea la figura según el tipo seleccionado
            if shape == "Círculo":
                item = QGraphicsEllipseItem(-size/2, -size/2, size, size)
            elif shape == "Estrella":
                item = self.create_star(size)
            elif shape == "Pétalo":
                item = self.create_petals(size)

            # Estilo sin relleno y con contorno
            item.setBrush(QBrush(Qt.NoBrush))  # Sin relleno
            item.setPen(QPen(self.color, 2))   # Contorno con color y grosor
            item.setFlags(item.ItemIsMovable | item.ItemIsSelectable)  # Movible y seleccionable
            item.setPos(pos)  # Posición en el lienzo
            self.scene.addItem(item)  # Añade la figura al lienzo

    def create_star(self, size):
        # Crea una estrella de 5 puntas
        points = []
        for i in range(10):
            angle = i * 36
            radius = size if i % 2 == 0 else size / 2  # Alterna entre punta y base
            rad = math.radians(angle)
            x = math.cos(rad) * radius
            y = math.sin(rad) * radius
            points.append(QPointF(x, y))
        return QGraphicsPolygonItem(QPolygonF(points))  # Devuelve la figura

    def create_petals(self, size):
        # Crea una figura con forma de pétalo doble
        points = []
        for i in range(2):
            angle = i * 180
            rad = math.radians(angle)
            x = math.cos(rad) * size
            y = math.sin(rad) * size
            points.append(QPointF(x, y))
        return QGraphicsPolygonItem(QPolygonF(points))  # Devuelve la figura

# Punto de entrada de la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Crea la aplicación
    window = MandalaApp()  # Instancia de la ventana principal
    window.show()  # Muestra la ventana
    sys.exit(app.exec_())  # Ejecuta el bucle principal
        
