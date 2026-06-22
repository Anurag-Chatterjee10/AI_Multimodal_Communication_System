"""
Frame Converter
---------------

Converts OpenCV (NumPy) frames into Qt QPixmap objects.
"""

import cv2

from PySide6.QtGui import (
    QImage,
    QPixmap,
)


class FrameConverter:
    """
    Utility class for converting OpenCV frames
    into Qt displayable images.
    """

    @staticmethod
    def to_qpixmap(frame):
        """
        Convert an OpenCV BGR frame into QPixmap.

        Parameters
        ----------
        frame : numpy.ndarray
            OpenCV image frame.

        Returns
        -------
        QPixmap
            Ready to display in QLabel.
        """

        if frame is None:
            return QPixmap()

        # Convert BGR → RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        height, width, channels = rgb_frame.shape

        bytes_per_line = channels * width

        image = QImage(
            rgb_frame.data,
            width,
            height,
            bytes_per_line,
            QImage.Format_RGB888
        )

        return QPixmap.fromImage(image.copy())