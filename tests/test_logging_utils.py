from __future__ import annotations

from altium_cruncher.logging_utils import _configure_stream_encoding_errors


class _FakeReconfigurableStream:
    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []

    def reconfigure(self, **kwargs: str) -> None:
        self.calls.append(kwargs)


def test_configure_stream_encoding_errors_uses_backslashreplace() -> None:
    stream = _FakeReconfigurableStream()

    _configure_stream_encoding_errors(stream)

    assert stream.calls == [{"errors": "backslashreplace"}]


def test_configure_stream_encoding_errors_allows_non_reconfigurable_stream() -> None:
    _configure_stream_encoding_errors(object())
