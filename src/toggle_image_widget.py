from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os

class ToggleImageWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Use correct assets directory (lowercase)
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
        # Debug: print asset paths and existence
        print(f"Assets dir: {assets_dir}")
        for fname in [
            'checkbox_unchecked.png',
            'checkbox_unchecked_hover.png',
            'checkbox_checked.png',
            'checkbox_checked_hover.png']:
            fpath = os.path.join(assets_dir, fname)
            print(f"{fname}: exists={os.path.exists(fpath)} path={fpath}")
        self.icon_unchecked = QPixmap(os.path.join(assets_dir, 'checkbox_unchecked.png'))
        self.icon_unchecked_hover = QPixmap(os.path.join(assets_dir, 'checkbox_unchecked_hover.png'))
        self.icon_checked = QPixmap(os.path.join(assets_dir, 'checkbox_checked.png'))
        self.icon_checked_hover = QPixmap(os.path.join(assets_dir, 'checkbox_checked_hover.png'))
        self.checked = False
        self.focused = False
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFixedSize(50, 50)
        self.corner_radius = 8
        self.update_pixmap()
        self.setStyleSheet(f"border-radius: {self.corner_radius}px; background: transparent;")

    def update_pixmap(self):
        # 4 states: unchecked/unfocused, unchecked/focused, checked/unfocused, checked/focused
        if not self.checked and not self.focused:
            pixmap = self.icon_unchecked
        elif not self.checked and self.focused:
            pixmap = self.icon_unchecked_hover
        elif self.checked and not self.focused:
            pixmap = self.icon_checked
        elif self.checked and self.focused:
            pixmap = self.icon_checked_hover
        else:
            pixmap = self.icon_unchecked
        if pixmap and not pixmap.isNull():
            scaled = pixmap.scaled(42, 42, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.setPixmap(scaled)
        else:
            self.clear()

    def focusInEvent(self, event):
        self.focused = True
        self.update_pixmap()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.focused = False
        self.update_pixmap()
        super().focusOutEvent(event)

    def toggle(self):
        self.checked = not self.checked
        self.update_pixmap()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Space, Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.toggle()
        else:
            super().keyPressEvent(event)
