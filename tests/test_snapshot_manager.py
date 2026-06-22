import numpy as np

from src.services.snapshot_manager import SnapshotManager


frame = np.zeros(
    (480, 640, 3),
    dtype=np.uint8,
)

path = SnapshotManager.save_snapshot(frame)

print(path)