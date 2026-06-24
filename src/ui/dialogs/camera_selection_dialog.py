"""
Camera Selection Dialog
-----------------------

Allows the user to choose an available camera.
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QHBoxLayout,
)


class CameraSelectionDialog(QDialog):
    """
    Camera selection dialog.
    """

    def __init__(
        self,
        cameras: list[int],
        current_camera: int,
        parent=None,
    ):
        super().__init__(parent)

        self.setWindowTitle("Select Camera")

        self.setMinimumWidth(320)

        self._camera_list = QListWidget()

        for camera in cameras:

            self._camera_list.addItem(
                f"Camera {camera}"
            )

        if current_camera in cameras:

            self._camera_list.setCurrentRow(
                cameras.index(current_camera)
            )

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel("Available Cameras")
        )

        layout.addWidget(
            self._camera_list
        )

        button_layout = QHBoxLayout()

        ok_button = QPushButton("OK")

        cancel_button = QPushButton("Cancel")

        ok_button.clicked.connect(
            self.accept
        )

        cancel_button.clicked.connect(
            self.reject
        )

        button_layout.addStretch()

        button_layout.addWidget(ok_button)

        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def selected_camera(self):
        """
        Returns the selected camera index.
        """

        row = self._camera_list.currentRow()

        if row < 0:

            return None

        text = self._camera_list.currentItem().text()

        return int(
            text.replace("Camera ", "")
        )