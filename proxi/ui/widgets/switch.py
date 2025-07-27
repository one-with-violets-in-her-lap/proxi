from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QParallelAnimationGroup,
    QPointF,
    QPropertyAnimation,
    QRectF,
    Qt,
)
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QCheckBox


class SwitchButton(QCheckBox):
    def __init__(self, width=60):
        super().__init__()

        self.setFixedSize(width, width // 2)

        # Container
        # TODO: Theming
        self._container_off_color = QColor(142, 142, 147)
        self._container_on_color = QColor(42, 42, 42)

        self._bg_color = self._container_off_color

        # Knob
        # TODO: Theming
        self._knob_color = QColor(242, 242, 247)

        self._radius_factor = 0.8

        self._animation_curve = QEasingCurve.Type.OutExpo
        self._animation_duration = 300

        self._pos_factor = 0

        self._knob_animation = QPropertyAnimation(self, b"pos_factor", self)
        self._knob_animation.setEasingCurve(self._animation_curve)
        self._knob_animation.setDuration(self._animation_duration)

        self._container_animation = QPropertyAnimation(self, b"bg_color", self)
        self._container_animation.setEasingCurve(self._animation_curve)
        self._container_animation.setDuration(self._animation_duration)

        self._animation_group = QParallelAnimationGroup()
        self._animation_group.addAnimation(self._knob_animation)
        self._animation_group.addAnimation(self._container_animation)

        self.toggled.connect(self.start_animation)

    @Property(float)
    def pos_factor(self):
        return self._pos_factor

    @pos_factor.setter
    def pos_factor(self, value):
        self._pos_factor = value
        self.update()

    @Property(QColor)
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, color):
        self._bg_color = color
        self.update()

    def hitButton(self, pos):
        return self.contentsRect().contains(pos)

    def start_animation(self, state):
        self._animation_group.stop()

        if state:
            self._knob_animation.setEndValue(1)
            self._container_animation.setEndValue(self._container_on_color)
        else:
            self._knob_animation.setEndValue(0)
            self._container_animation.setEndValue(self._container_off_color)

        self._animation_group.start()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)

        # Rounded rect
        rect = QRectF(0, 0, self.width(), self.height())
        corner = min(self.height() / 2, self.width() / 2)

        radius = min(self.height(), self.width()) / 2 * self._radius_factor

        lengths = max(self.width() - self.height(), 0)
        circle_center_x = (
            min(self.height() / 2, self.width() / 2) + lengths * self._pos_factor
        )

        circle_center = QPointF(circle_center_x, self.height() / 2)

        # Paint bg
        p.setBrush(self._bg_color)
        p.drawRoundedRect(rect, corner, corner)

        # Paint circle
        p.setBrush(self._knob_color)
        p.drawEllipse(circle_center, radius, radius)

        p.end()
