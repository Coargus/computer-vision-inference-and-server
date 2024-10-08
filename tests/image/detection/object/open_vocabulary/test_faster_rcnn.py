from pathlib import Path

import pytest
from cogcvutil import read_image

from cvias.common.utils_mmdet import install_dependencies

install_dependencies()
from cvias.image.detection.object.open_vocabulary.faster_rcnn import (  # noqa: E402
    FasterRCNN,
)

ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent.parent
SAMPLE_DATA_DIR = ROOT_DIR / "sample_data"


def test_faster_rcnn_detection() -> None:
    """Test Yolo detection on a sample image."""
    image_path = SAMPLE_DATA_DIR / "coco_bus_and_car.png"
    assert image_path.exists(), f"Sample image {image_path} does not exist."

    image_array = read_image(image_path, "numpy")
    assert image_array is not None, "Failed to read image as numpy array."

    model = FasterRCNN(
        model_name="faster-rcnn_r50_fpn_1x_coco",
        explicit_checkpoint_path=None,
        gpu_number=0,
    )
    detected_object_set = model.detect(image_array)
    assert len(detected_object_set.keys()) == 8
    assert detected_object_set["bus"].confidence > 0.99
    assert detected_object_set["car"].confidence > 0.98


if __name__ == "__main__":
    pytest.main()
