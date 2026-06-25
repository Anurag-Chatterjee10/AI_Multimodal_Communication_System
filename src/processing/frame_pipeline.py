"""
Frame Processing Pipeline
-------------------------

Processes camera frames before they are
displayed in the GUI.
"""
from src.ai.overlays.overlay_engine import OverlayEngine
from src.processing.frame_converter import FrameConverter


class FramePipeline:
    """
    Central frame processing pipeline.
    """

    _latest_frame = None
    _recording_manager = None
    _ai_worker = None

    @classmethod
    def set_recording_manager(cls, recording_manager):
        """
        Register the RecordingManager.
        """

        cls._recording_manager = recording_manager
    
    @classmethod
    def set_ai_worker(cls, ai_worker):
        """
        Register the AIWorker used for future inference.
        """

        cls._ai_worker = ai_worker

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

        if (
            cls._ai_worker is not None
            and not cls._ai_worker.is_busy
        ):
            if cls._ai_worker.set_frame(frame.copy()):
                cls._ai_worker.start()
                
        return FrameConverter.to_qpixmap(frame)

    @classmethod
    def latest_frame(cls):
        """
        Return the latest frame.
        """

        return cls._latest_frame