"""
Application Controller
----------------------

Coordinates communication between the UI
and application services.

The controller contains no business logic.
It simply connects signals and delegates work.
"""
from src.ai.overlays.overlay_engine import OverlayEngine
from src.ui.dialogs.camera_selection_dialog import (
    CameraSelectionDialog,
)
from src.processing.frame_pipeline import FramePipeline
from src.services.snapshot_manager import SnapshotManager
from src.services.recording.recording_manager import RecordingManager
from PySide6.QtWidgets import QFileDialog

class AppController:
    """
    Coordinates communication between the UI
    and application services.
    """

    def __init__(
        self,
        main_window,
        camera_service,
        video_service,
        model_manager,
        ai_worker,
    ):
        """
        Initialize the application controller.
        """

        self.main_window = main_window

        self.camera_service = camera_service

        self.video_service = video_service

        self.model_manager = model_manager

        self.ai_worker = ai_worker

        self.recording_manager = RecordingManager()

        self.current_media_source = "NONE"

        self.latest_ai_result = None

        self._overlay_engine = OverlayEngine()

        FramePipeline.set_recording_manager(
            self.recording_manager
        )

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
        self.main_window.tool_bar.camera_action.triggered.connect(
            self._select_camera
        )
        self.main_window.tool_bar.start_action.triggered.connect(
            self._start_camera
        )

        self.main_window.tool_bar.stop_action.triggered.connect(
            self._stop_camera
        )

        self.main_window.tool_bar.snapshot_action.triggered.connect(
            self._take_snapshot
        )

        self.main_window.tool_bar.record_action.triggered.connect(
            self._start_recording
        )

        self.main_window.tool_bar.stop_record_action.triggered.connect(
            self._stop_recording
        )
        self.main_window.tool_bar.open_action.triggered.connect(
            self._open_video
        )

        self.main_window.menu_bar.open_video_action.triggered.connect(
            self._open_video
        )
        # ------------------------------------------------------
        # Recording Signals
        # ------------------------------------------------------

        self.recording_manager.recording_started.connect(
            lambda: self.main_window.tool_bar.set_recording_state(True)
        )

        self.recording_manager.recording_stopped.connect(
            lambda: self.main_window.tool_bar.set_recording_state(False)
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

        # ------------------------------------------------------
        # Video Service Signals
        # ------------------------------------------------------

        self.video_service.frame_ready.connect(
            self._update_camera_frame
        )

        self.video_service.video_started.connect(
            self._video_started
        )

        self.video_service.video_finished.connect(
            self._video_finished
        )

        self.video_service.video_error.connect(
            self._video_error
        )

        self.video_service.fps_updated.connect(
            self._update_fps
        )

        # ------------------------------------------------------
        # AI Worker Signals
        # ------------------------------------------------------

        self.ai_worker.inference_error.connect(
            self._ai_error
        )

        self.ai_worker.inference_finished.connect(
            self._ai_finished
        )
    # ==========================================================
    # Toolbar Actions
    # ==========================================================

    def _select_camera(self):
        """
        Display the camera selection dialog
        and switch to the selected camera.
        """

        cameras = self.camera_service.enumerate_cameras()

        if not cameras:

            self.main_window.statusBar().showMessage(
                "No camera devices found."
            )

            return

        dialog = CameraSelectionDialog(
            cameras=cameras,
            current_camera=self.camera_service.current_camera,
            parent=self.main_window,
        )

        if not dialog.exec():

            return

        selected_camera = dialog.selected_camera()

        if selected_camera is None:

            return

        if (
            selected_camera
            == self.camera_service.current_camera
        ):

            self.main_window.statusBar().showMessage(
                f"Camera {selected_camera} already selected."
            )

            return

        was_running = self.camera_service.is_running

        if was_running:

            self.camera_service.stop()

        self.camera_service.switch_camera(
            selected_camera
        )

        if was_running:

            self.camera_service.start()

        self.main_window.statusBar().showMessage(
            f"Switched to Camera {selected_camera}"
        )
    def _start_camera(self):
        """
        Start the camera.
        """

        if self.video_service.is_running:

            self.video_service.stop()

        self.camera_service.start()

    def _stop_camera(self):
        """
        Stop current media.
        """

        if self.recording_manager.is_recording:

            self.recording_manager.stop()

        if self.camera_service.is_running:

            self.camera_service.stop()

        if self.video_service.is_running:

            self.video_service.stop()

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

    def _start_recording(self):
        """
        Start video recording.
        """

        if self.recording_manager.is_recording:

            self.main_window.statusBar().showMessage(
                "Recording already in progress."
            )

            return

        frame = FramePipeline.latest_frame()

        if frame is None:

            self.main_window.statusBar().showMessage(
                "No frame available."
            )

            return

        if self.recording_manager.start(frame):

            self.main_window.statusBar().showMessage(
                "Recording Started"
            )

            self.main_window.workspace.camera_panel.set_status(
                "🔴 REC"
            )

        else:

            self.main_window.statusBar().showMessage(
                "Failed to start recording."
            )

    def _stop_recording(self):
        """
        Stop video recording.
        """

        if not self.recording_manager.is_recording:

            self.main_window.statusBar().showMessage(
                "Recording is not active."
            )

            return

        self.recording_manager.stop()

        self.main_window.statusBar().showMessage(
            "Recording Stopped"
        )

        self.current_media_source = "CAMERA"

        self.main_window.workspace.camera_panel.set_status(
            "🟢 LIVE"
        )
    # ==========================================================
    # Camera Updates
    # ==========================================================

    def _update_camera_frame(self, frame):
        """
        Display the processed frame.
        """

        if self.latest_ai_result is not None:

            frame = self._overlay_engine.render(
                frame,
                self.latest_ai_result,
            )

        pixmap = FramePipeline.process(frame)

        if not self.ai_worker.is_busy:

            if self.ai_worker.set_frame(frame):

                self.ai_worker.start()

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

        self.current_media_source = "CAMERA"

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
        if self.recording_manager.is_recording:
            self.recording_manager.stop()

        self.current_media_source = "NONE"

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

        if self.recording_manager.is_recording:
            self.recording_manager.stop()

        self.main_window.statusBar().showMessage(
            message
        )

        self.main_window.workspace.camera_panel.set_status(
            "❌ CAMERA ERROR"
        )

    def _update_fps(self, fps):
        """
        Update media FPS.
        """
        camera_running = self.camera_service.is_running
        video_running = self.video_service.is_running

        if not camera_running and not video_running:
            return

        self.main_window.statusBar().showMessage(
            f"FPS : {fps:.1f}"
        )

        if self.recording_manager.is_recording:

            status = f"🔴 REC | FPS : {fps:.1f}"

        elif video_running:

            status = f"▶ VIDEO | FPS : {fps:.1f}"

        elif camera_running:

            status = f"🟢 LIVE | FPS : {fps:.1f}"

        else:

            status = "🔴 OFFLINE"

        self.main_window.workspace.camera_panel.set_status(
            status
        )
    # ==========================================================
    # Video Status
    # ==========================================================

    def _video_started(self):
        """
        Video playback started.
        """

        self.current_media_source = "VIDEO"

        self.main_window.statusBar().showMessage(
            "Video Started"
        )

        self.main_window.workspace.camera_panel.set_status(
            "▶ VIDEO"
        )

    def _video_finished(self):
        """
        Video playback finished.
        """

        if self.recording_manager.is_recording:
            self.recording_manager.stop()

        self.current_media_source = "NONE"

        self.main_window.statusBar().showMessage(
            "Video Finished"
        )

        self.main_window.workspace.camera_panel.set_status(
            "■ VIDEO END"
        )


    def _video_error(self, message):
        """
        Handle video playback errors.
        """

        if self.recording_manager.is_recording:
            self.recording_manager.stop()

        self.current_media_source = "NONE"

        self.main_window.statusBar().showMessage(
            message
        )

        self.main_window.workspace.camera_panel.set_status(
            "❌ VIDEO ERROR"
        )
    def _open_video(self):
        """
        Open and play a video.
        """

        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Open Video",
            "",
            (
                "Video Files "
                "(*.mp4 *.avi *.mov *.mkv *.wmv);;"
                "All Files (*)"
            ),
        )

        if not file_path:

            return

        # Stop camera if running

        if self.camera_service.is_running:

            self.camera_service.stop()

        # Stop previous video

        if self.video_service.is_running:

            self.video_service.stop()

        # Load video

        self.video_service.open(file_path)

        # Start playback

        self.video_service.start()

        self.main_window.statusBar().showMessage(
            f"Playing : {file_path}"
        )
    
    # ==========================================================
    # AI Worker
    # ==========================================================

    def _ai_finished(self, result):
        """
        AI inference completed.
        """

        self.latest_ai_result = result

        print(
            f"AI Result Updated : "
            f"{result.message}"
        )

    def _ai_error(self, message):
        """
        AI inference error.
        """

        self.latest_ai_result = None

        print(
            f"AI Error : {message}"
        )

    @property
    def overlay_engine(self) -> OverlayEngine:
        """
        Returns the application's overlay engine.
        """

        return self._overlay_engine