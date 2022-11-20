class EdgeTPUServer:
    """Main application."""

    def __init__(
            self,
            model_file: str,
            label_file: str,
            top_k: int,
            threshold: float,
            video_format: str,
            headless: bool,
            video_src: str,
    ):
        """Initialize an EdgeTPU server."""
        self._model_file = model_file
        self._label_file = label_file
        self._top_k = top_k
        self._threshold = threshold
        self._video_format = video_format
        self._headless = headless
        self._video_stream = video_src
