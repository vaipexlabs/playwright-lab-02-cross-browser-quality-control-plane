from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Generator
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).parents[2]


def available_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("127.0.0.1", 0))
        return int(server_socket.getsockname()[1])


def wait_until_ready(
    base_url: str,
    process: subprocess.Popen[str] | None = None,
) -> None:
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        if process is not None and process.poll() is not None:
            raise RuntimeError(
                "Vaipex Explorer stopped during startup "
                f"with code {process.returncode}."
            )
        try:
            with urllib.request.urlopen(f"{base_url}/health", timeout=1) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.1)
    raise RuntimeError(
        f"Vaipex Explorer at {base_url} did not become ready within 15 seconds."
    )


@pytest.fixture(scope="session")
def app_server() -> Generator[str]:
    configured_base_url = os.getenv("VAIPEX_BASE_URL", "").strip().rstrip("/")
    if configured_base_url:
        wait_until_ready(configured_base_url)
        yield configured_base_url
        return

    port = available_port()
    base_url = f"http://127.0.0.1:{port}"
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONPATH": str(REPOSITORY_ROOT / "src"),
            "VAIPEX_TEST_MODE": "1",
        }
    )
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "vaipex_cross_browser.app:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "--log-level",
            "warning",
        ],
        cwd=REPOSITORY_ROOT,
        env=environment,
        text=True,
    )
    try:
        wait_until_ready(base_url, process)
        yield base_url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


@pytest.fixture(scope="session")
def base_url(app_server: str) -> str:
    return app_server
