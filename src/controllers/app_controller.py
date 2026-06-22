"""
Application Controller
----------------------

Coordinates communication between the UI
and application services.

The controller contains no business logic.
It simply connects signals and delegates work.
"""

from src.processing.frame_pipeline import FramePipeline
from src.services.snapshot_manager import SnapshotManager


class AppController:
    """
    Coordinates communication between the UI
    and application services.
    """

    def __init__(
        self,
        main_window,
        camera_service,
    ):
        self.main_window = main_window
        self.camera_service = camera_service

        self._connect_signals()

    # ==========================================================
    # Signal Connections
    # ==========================================================

    def _connect_signals(self):
        """
        Connect UI actions and service signals.
        """

        # ------------------------------------------------------
        # Toolbar Actions
        # ------------------------------------------------------

        self.main_window.tool_bar.start_action.triggered.connect(
            self._start_camera
        )

        self.main_window.tool_bar.stop_action.triggered.connect(
            self._stop_camera
        )

        self.main_window.tool_bar.snapshot_action.triggered.connect(
            self._take_snapshot
        )

        # ------------------------------------------------------
        # Camera Service Signals
        # ------------------------------------------------------

        self.camera_service.frame_ready.connect(
            self._update_camera_frame
        )

        self.camera_service.camera_started.connect(
            self._camera_started
        )

        self.camera_service.camera_stopped.connect(
            self._camera_stopped
        )

        self.camera_service.camera_error.connect(
            self._camera_error
        )

        self.camera_service.fps_updated.connect(
            self._update_fps
        )

    # ==========================================================
    # Toolbar Actions
    # ==========================================================

    def _start_camera(self):
        """
        Start the camera.
        """

        self.camera_service.start()

    def _stop_camera(self):
        """
        Stop the camera.
        """

        self.camera_service.stop()

    def _take_snapshot(self):
        """
        Save the latest camera frame.
        """

        frame = FramePipeline.latest_frame()

        if frame is None:

            self.main_window.statusBar().showMessage(
                "No frame available."
            )

            return

        path = SnapshotManager.save_snapshot(frame)

        self.main_window.statusBar().showMessage(
            f"Snapshot saved : {path.name}"
        )

    # ==========================================================
    # Camera Updates
    # ==========================================================

    def _update_camera_frame(self, frame):
        """
        Display the processed frame.
        """

        pixmap = FramePipeline.process(frame)

        self.main_window.workspace.camera_panel.set_frame(
            pixmap
        )

    # ==========================================================
    # Camera Status
    # ==========================================================

    def _camera_started(self):
        """
        Camera started successfully.
        """

        self.main_window.statusBar().showMessage(
            "Camera Started"
        )

        self.main_window.workspace.camera_panel.set_status(
            "🟢 LIVE"
        )

    def _camera_stopped(self):
        """
        Camera stopped.
        """

        self.main_window.statusBar().showMessage(
            "Camera Stopped"
        )

        self.main_window.workspace.camera_panel.set_status(
            "🔴 OFFLINE"
        )

    def _camera_error(self, message):
        """
        Camera error occurred.
        """

        self.main_window.statusBar().showMessage(
            message
        )

        self.main_window.workspace.camera_panel.set_status(
            "❌ CAMERA ERROR"
        )

    def _update_fps(self, fps):
        """
        Update camera FPS.
        """

        self.main_window.statusBar().showMessage(
            f"FPS : {fps:.1f}"
        )

        self.main_window.workspace.camera_panel.set_status(
            f"🟢 LIVE | FPS : {fps:.1f}"
        )