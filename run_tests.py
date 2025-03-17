import subprocess
import time
import os
from datetime import datetime

def run_tests_and_generate_html_report():
    print("🚀 Running Pytest and Generating HTML Report...")

    # Create a reports directory if it doesn't exist
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"report_{timestamp}.html"
    report_path = os.path.join(reports_dir, report_filename)

    start_time = time.time()

    # Run Pytest and generate an HTML report with logs (no separate log files)
    pytest_command = [
        "pytest",
        "--html", report_path,
        "--self-contained-html",
        "--log-cli-level=INFO",  # Ensures logs appear in the HTML report
        "--log-auto-indent=2",  # Formats logs properly in the HTML
        "--capture=tee-sys",  # Includes console logs in the report (but no separate log file)
    ]

    subprocess.run(pytest_command)

    end_time = time.time()
    duration = round(end_time - start_time, 2)

    print("\n✅ HTML Report Generated Successfully!")
    print(f"📌 Test Duration: {duration} seconds")
    print(f"📂 Reports Directory: {reports_dir}")
    print(f"📄 Latest Report: {report_filename}")

if __name__ == "__main__":
    run_tests_and_generate_html_report()
