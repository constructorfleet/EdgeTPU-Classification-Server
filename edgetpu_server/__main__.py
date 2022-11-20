import argparse

from edgetpu_server.classify import run


def main():
    """Start EdgeTPU Server."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--model',
                        help='.tflite model path',
                        required=True)
    parser.add_argument('--labels',
                        help='label file path',
                        required=True)
    parser.add_argument('--top_k',
                        type=int,
                        default=3,
                        help='number of categories with highest score to display')
    parser.add_argument('--threshold',
                        type=float,
                        default=0.1,
                        help='classifier score threshold')
    parser.add_argument('--headless',
                        type=bool,
                        help='Run without displaying the video.',
                        default=False)
    parser.add_argument('--videofmt',
                        help='Input video format.',
                        default='raw',
                        choices=['raw', 'h264', 'jpeg'])
    parser.add_argument('videosrc',
                        help='Which video source to use.',
                        default='/dev/video0')
    args = parser.parse_args()

    print('Loading {} with {} labels.'.format(args.model, args.labels))
    run(args)


if __name__ == '__main__':
    main()
