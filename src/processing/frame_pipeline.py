"""
Frame Processing Pipeline
-------------------------

Processes camera frames before they are
displayed in the GUI.
"""

from src.processing.frame_converter import FrameConverter


class FramePipeline:
    """
    Central frame processing pipeline.
    """

    _latest_frame = None

    @classmethod
    def process(cls, frame):
        """
        Process a camera frame.
        """

        cls._latest_frame = frame.copy()

        return FrameConverter.to_qpixmap(frame)

    @classmethod
    def latest_frame(cls):
        """
        Return the latest camera frame.
        """

        return cls._latest_frame