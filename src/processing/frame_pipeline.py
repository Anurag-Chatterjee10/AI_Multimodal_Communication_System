"""
Frame Processing Pipeline
-------------------------

Acts as the central frame dispatcher for the
entire application.

Every camera frame flows through this class.

Responsibilities
----------------
• Store latest frame
• Notify registered processors
• Convert frame for GUI
"""

from src.processing.frame_converter import FrameConverter


class FramePipeline:
    """
    Central frame processing pipeline.
    """

    _latest_frame = None

    _processors = []

    # ==========================================================
    # Registration
    # ==========================================================

    @classmethod
    def register_processor(cls, processor):
        """
        Register a frame processor.

        Every registered processor must implement

            process(frame)

        Parameters
        ----------
        processor :
            Any object containing a process(frame)
            method.
        """

        if processor not in cls._processors:
            cls._processors.append(processor)

    @classmethod
    def unregister_processor(cls, processor):
        """
        Remove a processor.
        """

        if processor in cls._processors:
            cls._processors.remove(processor)

    # ==========================================================
    # Main Pipeline
    # ==========================================================

    @classmethod
    def process(cls, frame):
        """
        Process one camera frame.
        """

        cls._latest_frame = frame.copy()

        #
        # Notify every processor
        #

        for processor in cls._processors:

            processor.process(frame)

        #
        # GUI Conversion
        #

        return FrameConverter.to_qpixmap(frame)

    # ==========================================================
    # Latest Frame
    # ==========================================================

    @classmethod
    def latest_frame(cls):
        """
        Return latest frame.
        """

        return cls._latest_frame