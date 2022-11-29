import argparse
import collections
import time
from typing import Callable


def avg_fps_counter(window_size):
    window = collections.deque(maxlen=window_size)
    prev = time.monotonic()
    yield 0.0  # First fps value.

    while True:
        curr = time.monotonic()
        window.append(curr - prev)
        prev = curr
        yield len(window) / sum(window)


def arg_parser(
        program_name: str,
        runner: Callable
):
    parser = argparse.ArgumentParser(program_name)
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
    args = parser.parse_args()

    print('Loading {} with {} labels.'.format(args.model, args.labels))
    runner(args)
