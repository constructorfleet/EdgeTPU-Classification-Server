import argparse
import time
from typing import Mapping, Tuple, Callable, List

from pycoral.adapters.common import input_size
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter, run_inference

from edgetpu_server.utils import avg_fps_counter, gstreamer
from edgetpu_server.utils.svg import SVG


class App:
    _interpreter = None
    _labels: Mapping[int, str] = None
    _inference_size: Tuple = None
    _get_inferred = None
    _fps_counter = avg_fps_counter(30)
    _threshold: float = None
    _tok_k: int = None

    def __init__(
            self,
            get_inferred: Callable
    ):
        self._get_inferred = get_inferred

    @property
    def name(self):
        pass

    @property
    def _arg_parser(self):
        parser = argparse.ArgumentParser(self.name)
        parser.add_argument('--model',
                            help='.tflite model path')
        parser.add_argument('--labels',
                            help='label file path')
        parser.add_argument('--top_k',
                            type=int,
                            default=3,
                            help='number of categories with highest score to display')
        parser.add_argument('--threshold',
                            type=float,
                            default=0.1,
                            help='classifier score threshold')
        parser.add_argument('--videosrc',
                            help='Which video source to use.',
                            default='/dev/video0')
        parser.add_argument('--headless',
                            type=bool,
                            default=False,
                            help='Run without displaying the video.')
        parser.add_argument('--videofmt',
                            default='raw',
                            choices=['raw', 'h264', 'jpeg'],
                            help='Input video format.')

        return parser

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

    def callback(
            self,
            input_tensor,
            src_size,
            inference_box
    ):
        start_time = time.monotonic()
        run_inference(self._interpreter, input_tensor)

        results = self._get_inferred(
            self._interpreter,
            score_threshold=self._threshold)[:self._tok_k]
        end_time = time.monotonic()
        duration = (end_time - start_time) * 1000
        frame_rate = round(next(self._fps_counter))
        text_lines = [
            " ",
            f"Inference: {duration:.2f} ms",
            f"FPS: {frame_rate} fps",
        ]

        return self.get_overlay(
            src_size,
            text_lines,
            results,
            inference_box,
        )

    def run(
            self,
    ):
        args = self._arg_parser.parse_args()
        self._interpreter = make_interpreter(args.model)
        self._interpreter.allocate_tensors()
        self._labels = read_label_file(args.labels)
        self._inference_size = input_size(self._interpreter)

        print('Loading {} with {} labels.'.format(args.model, args.labels))
        result = gstreamer.run_pipeline(self.callback,
                                        src_size=(640, 480),
                                        appsink_size=self._inference_size,
                                        videosrc=args.videosrc,
                                        videofmt=args.videofmt,
                                        headless=args.headless)
