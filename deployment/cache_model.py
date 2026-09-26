"""Download the deployment model during build instead of the first request."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "implementation"))
from cloud import CloudEncoder
encoder = CloudEncoder()
assert len(encoder.encode("build verification")) == 384
print("Cloud embedding model ready")
