# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo which runs object detection on camera frames using GStreamer.

Run default object detection:
python3 detect.py

Choose different camera and input encoding
python3 detect.py --videosrc /dev/video1 --videofmt jpeg

TEST_DATA=../all_models
Run face detection model:
python3 detect.py \
  --model ${TEST_DATA}/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite

Run coco model:
python3 detect.py \
  --model ${TEST_DATA}/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite \
  --labels ${TEST_DATA}/coco_labels.txt
"""
from typing import List

from edgetpu_server import App
from edgetpu_server.utils.svg import SVG
from pycoral.adapters.detect import get_objects


class DetectApp(App):

    def __init__(self):
        super().__init__(get_objects)

    @property
    def name(self):
        return "detect"

    def get_overlay(
            self,
            source_size,
            text_lines: List[str],
            results: List,
            inference_box,
    ):
        svg = SVG(source_size)
        src_w, src_h = source_size
        box_x, box_y, box_w, box_h = inference_box
        scale_x, scale_y = src_w / box_w, src_h / box_h

        for y, line in enumerate(text_lines, start=1):
            svg.add_text(10, y * 20, line, 20)
        for obj in results:
            bbox = obj.bbox
            if not bbox.valid:
                continue
            # Absolute coordinates, input tensor space.
            x, y = bbox.xmin, bbox.ymin
            w, h = bbox.width, bbox.height
            # Subtract boxing offset.
            x, y = x - box_x, y - box_y
            # Scale to source coordinate space.
            x, y, w, h = x * scale_x, y * scale_y, w * scale_x, h * scale_y
            percent = int(100 * obj.score)
            object_label = self._labels.get(obj.id, obj.id)
            label = f"{percent}% {object_label}"
            svg.add_text(x, y - 5, label, 20)
            svg.add_rect(x, y, w, h, 'red', 2)
        return svg.finish()


if __name__ == '__main__':
    DetectApp().run()
