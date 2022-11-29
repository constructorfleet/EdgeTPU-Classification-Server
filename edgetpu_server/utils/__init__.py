import collections
import time


def avg_fps_counter(window_size):
    window = collections.deque(maxlen=window_size)
    prev = time.monotonic()
    yield 0.0  # First fps value.

    while True:
        curr = time.monotonic()
        window.append(curr - prev)
        prev = curr
        yield len(window) / sum(window)


def get_dev_board_model():
    try:
        model = open('/sys/firmware/devicetree/base/model').read().lower()
        if 'mx8mq' in model:
            return 'mx8mq'
        if 'mt8167' in model:
            return 'mt8167'
    except:
        pass
    return None
