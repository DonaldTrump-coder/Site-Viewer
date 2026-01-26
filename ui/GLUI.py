from PyQt5.QtWidgets import QOpenGLWidget
from OpenGL.GL import *
import numpy as np
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QImage, QPainter
import cv2

class GLWidget(QOpenGLWidget):
    def __init__(self, parent, mainwindow):
        super().__init__(parent=parent)
        self.image = None
        self.texture_id = None
        self.main_window = mainwindow

    def initialize(self):
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_TEXTURE_2D)
    
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def set_image(self, img:np.ndarray):
        self.image = img
        self.update()

    def paintGL(self):
        self.makeCurrent()
        painter = QPainter(self)
        painter.fillRect(0, 0, self.width(), self.height(), 0x000000)
        if self.image is None:
            return
        img = np.transpose(self.image, (1, 2, 0))
        img = np.flipud(img).astype(np.uint8)
        h, w, _ = img.shape
        qimg = QImage(img.data.tobytes(), w, h, 3 * w, QImage.Format_RGB888)

        scale = min(self.width() / w, self.height() / h)
        disp_w = int(w * scale)
        disp_h = int(h * scale)
        x0 = (self.width() - disp_w) // 2
        y0 = (self.height() - disp_h) // 2

        painter.drawImage(x0, y0, qimg.scaled(disp_w, disp_h))
        painter.end()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D:
            self.main_window.renderthread.move_right()
        if event.key() == Qt.Key_W:
            self.main_window.renderthread.move_forward()
        if event.key() == Qt.Key_S:
            self.main_window.renderthread.move_back()
        if event.key() == Qt.Key_A:
            self.main_window.renderthread.move_left()

    def mousePressEvent(self, event):
        self.setFocus()
        if event.button() == Qt.LeftButton:
            self.last_pos = QPointF()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            dir = event.pos() - self.last_pos
            self.last_pos = event.pos()
            self.main_window.renderthread.rotate_in_dir(np.array([dir.x(), dir.y()]))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_pos = QPointF()