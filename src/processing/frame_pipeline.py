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
    _recording_manager = None

    @classmethod
    def set_recording_manager(cls, recording_manager):
        """
        Register the RecordingManager.
        """

        cls._recording_manager = recording_manager

    @classmethod
    def process(cls, frame):
        """
        Process a camera frame.
        """

        cls._latest_frame = frame.copy()

        if (
            cls._recording_manager is not None
            and cls._recording_manager.is_recording
        ):
            cls._recording_manager.write(frame)

        return FrameConverter.to_qpixmap(frame)

    @classmethod
    def latest_frame(cls):
        """
        Return the latest frame.
        """

        return cls._latest_frame