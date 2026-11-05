import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TESTS_ROOT = Path(__file__).resolve().parent


def run_test(source_file: Path, should_succeed: bool) -> bool:
    result = subprocess.run(
        [sys.executable, "main.py", str(source_file)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    succeeded = result.returncode == 0
    passed = succeeded == should_succeed

    relative_path = source_file.relative_to(PROJECT_ROOT)
    status = "PASS" if passed else "FAIL"

    print(f"[{status}] {relative_path}")

    if not passed:
        output = result.stdout + result.stderr
        print(output.strip())

    return passed


def main() -> int:
    test_cases = []

    for source_file in sorted((TESTS_ROOT / "valid").glob("*.oos")):
        test_cases.append((source_file, True))

    for source_file in sorted((TESTS_ROOT / "invalid").glob("*.oos")):
        test_cases.append((source_file, False))

    if not test_cases:
        print("No test files found.")
        return 1

    passed_count = 0

    for source_file, should_succeed in test_cases:
        if run_test(source_file, should_succeed):
            passed_count += 1

    total_count = len(test_cases)
    print(f"\nResult: {passed_count}/{total_count} tests passed.")

    return 0 if passed_count == total_count else 1


if __name__ == "__main__":
    sys.exit(main())