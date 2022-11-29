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

"""A demo which runs object classification on camera frames.

Run default object detection:
python3 classify.py

Choose different camera and input encoding
python3 classify.py --videosrc /dev/video1 --videofmt jpeg
"""
from typing import List

from edgetpu_server import App
from edgetpu_server.utils.svg import SVG
from pycoral.adapters.classify import get_classes


class ClassifyApp(App):

    def __init__(self):
        super().__init__(get_classes)

    @property
    def name(self):
        return "classify"

    def get_overlay(
            self,
            source_size,
            text_lines: List[str],
            results: List,
            inference_box,
    ):
        svg = SVG(source_size)
        for y, line in enumerate(text_lines, start=1):
            svg.add_text(10, y * 20, line, 20)
        return svg.finish()


if __name__ == '__main__':
    ClassifyApp().run()
