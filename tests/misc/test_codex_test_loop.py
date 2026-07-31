"""Regression tests for the canonical Codex Docker verification loop."""

from __future__ import annotations

import os
import stat
import subprocess
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _write_executable(path: Path, content: str) -> None:
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def test_make_codex_test_fails_when_localstack_bootstrap_is_incomplete(
    tmp_path: Path,
) -> None:
    """A missing required LocalStack resource must make the canonical target fail."""
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()

    _write_executable(
        fake_bin / "git",
        """
        #!/usr/bin/env bash
        set -euo pipefail

        case "${1:-} ${2:-}" in
          "branch --show-current")
            echo "feature/db/regression"
            ;;
          "status --short")
            exit 0
            ;;
          *)
            echo "unexpected git invocation: $*" >&2
            exit 1
            ;;
        esac
        """,
    )

    _write_executable(
        fake_bin / "curl",
        """
        #!/usr/bin/env bash
        exit 0
        """,
    )

    _write_executable(
        fake_bin / "docker",
        """
        #!/usr/bin/env bash
        set -euo pipefail

        invocation="$*"

        case "${invocation}" in
          *"logs --no-color --tail=500"*)
            exit 0
            ;;
          *"config --quiet"*)
            exit 0
            ;;
          *"up --build -d"*)
            exit 0
            ;;
          *"exec -T postgres pg_isready -U cdp -d cdp"*)
            exit 0
            ;;
          *"exec -T postgres psql -U cdp -d cdp -Atqc"*)
            echo "1"
            exit 0
            ;;
          *"exec -T localstack awslocal events describe-event-bus --name cdp-events-local"*)
            echo "event bus not found" >&2
            exit 1
            ;;
          *"exec -T localstack awslocal "*)
            exit 0
            ;;
          *" ps")
            exit 0
            ;;
          *)
            echo "unexpected docker invocation: ${invocation}" >&2
            exit 1
            ;;
        esac
        """,
    )

    no_op_suite = tmp_path / "test-suite.sh"
    _write_executable(
        no_op_suite,
        """
        #!/usr/bin/env bash
        exit 0
        """,
    )

    env = os.environ.copy()
    env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"
    env["CDP_TEST_SUITE_SCRIPT"] = str(no_op_suite)
    env["CDP_TEST_LOG_DIR"] = str(tmp_path / "logs")
    env["CDP_LOCALSTACK_BOOTSTRAP_ATTEMPTS"] = "1"
    env["CDP_LOCALSTACK_BOOTSTRAP_DELAY_SECONDS"] = "0"

    completed = subprocess.run(
        ["make", "codex-test"],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )

    output = f"{completed.stdout}\n{completed.stderr}"

    assert completed.returncode != 0
    assert "EventBridge bus cdp-events-local" in output
    assert "Codex test loop failed" in output
