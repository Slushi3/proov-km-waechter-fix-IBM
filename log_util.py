# log_util.py
# Simple logger for KM-Waechter. Modernised 2025.
# Removed dead debug() function (DEBUG has been False since 2014 and was never set).

import time

LOG_LINES: list = []   # module-level buffer; flushed by flush_log()


def log(message: str) -> None:
    """Append a timestamped line to the log buffer and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def flush_log(path: str) -> None:
    """Write all buffered log lines to *path* (append mode) and clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
