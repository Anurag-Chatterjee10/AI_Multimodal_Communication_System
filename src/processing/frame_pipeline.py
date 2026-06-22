"""
Frame Processing Pipeline
-------------------------

Processes frames before they are
displayed in the GUI.

Future stages will include:

- Recording
- Snapshot
- YOLO
- MediaPipe
- OCR
- Face Recognition
"""

from src.processing.frame_converter import FrameConverter


class FramePipeline:
    """
    Central processing pipeline for all
    incoming camera frames.
    """

    @staticmethod
    def process(frame):
        """
        Process an OpenCV frame.

        Parameters
        ----------
        frame
            OpenCV frame.

        Returns
        -------
        QPixmap
        """

        # ==========================================
        # Future Processing
        # ==========================================

        #
        # frame = recorder.process(frame)
        #
        # frame = snapshot.process(frame)
        #
        # frame = yolo.process(frame)
        #
        # frame = mediapipe.process(frame)
        #
        # frame = ocr.process(frame)
        #

        # ==========================================

        return FrameConverter.to_qpixmap(frame)