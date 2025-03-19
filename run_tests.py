import subprocess
import time
import os
import sys
from datetime import datetime


def run_tests_and_generate_html_report():
    print("🚀 Running Pytest and Generating HTML Report...")

    # Set project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Add project root to PYTHONPATH
    sys.path.insert(0, project_root)
    os.environ["PYTHONPATH"] = project_root  # Ensures subprocess also gets the updated path

    # Create a reports directory if it doesn't exist
    reports_dir = os.path.join(project_root, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"report_{timestamp}.html"
    report_path = os.path.join(reports_dir, report_filename)

    start_time = time.time()

    # Run Pytest and generate an HTML report
    pytest_command = [
        "pytest",
        "--html", report_path,
        "--self-contained-html",
        "--log-cli-level=INFO",
        "--log-auto-indent=2",
        "--capture=tee-sys",
    ]

    subprocess.run(pytest_command, env=os.environ)  # Pass updated environment variables

    end_time = time.time()
    duration = round(end_time - start_time, 2)

    print("\n✅ HTML Report Generated Successfully!")
    print(f"📌 Test Duration: {duration} seconds")
    print(f"📂 Reports Directory: {reports_dir}")
    print(f"📄 Latest Report: {report_filename}")


if __name__ == "__main__":
    run_tests_and_generate_html_report()
