# load_all_data.py
import subprocess
import sys

def run_script(script_name):
    print(f"\n=== Running {script_name} ===")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"⚠️ Errors in {script_name}:\n{result.stderr}")
    else:
        print(f"✅ {script_name} completed successfully.\n")

if __name__ == "__main__":
    scripts = [
        "load_csv_data.py",   # Loads base CSVs and builds resistance_profiles
        "load_card_data.py"   # Loads CARD gene data and maps to profiles
    ]

    for script in scripts:
        run_script(script)
