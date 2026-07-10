import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np

from src.audio.audio_buffer import AudioBuffer

buffer = AudioBuffer()

buffer.append(np.ones(16000, dtype=np.float32))
buffer.append(np.ones(16000, dtype=np.float32))

print("Duration:", buffer.duration)
print("Ready:", buffer.is_ready())
print("Samples:", len(buffer.get_audio()))