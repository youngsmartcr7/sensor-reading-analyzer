import argparse
import random
import statistics
import sys
from datetime import datetime

LOW_THRESHOLD = 18
HIGH_THRESHOLD = 30
ANOMALY_MARGING = 10
MIN_READING = 3

def safe_input(prompt: str) -> str:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting. Goodbye")
        sys.exit(0)


def get_reading() -> float:
    
    while True:
        raw = safe_input("Enter the temperature reading: ").strip()
        try:
            value = float(raw)
            break
        except ValueError:
            print("That's not a number - try again ")

    while True:
        unit = safe_input("Enter the unit (C or F): ").strip().lower()
        if unit in ("c", "f"):
            break
        print("Unit must be C or F.")

    return (value - 32) * 5/9 if unit == "f" else value   

def collect_readings() -> list[float]:
    readings:list[float] = []
    while True:
        readings.append(get_reading())
        if len(readings) >= MIN_READING:
            choice = safe_input("Type 'done' to stop, or press Enter to continue: ").strip().lower()
            if choice == "done":
                break
    return readings    

def classify(reading: float) -> str:
    if reading < LOW_THRESHOLD:
        return "low"
    if reading > HIGH_THRESHOLD:
        return "high"
    return "normal"

def count_by_class(readings: list[float]) -> dict[str, int]:
    counts = {"low": 0, "normal": 0, "high":0}
    for value in readings: 
        counts[classify(value)] += 1

    return counts

def flag_anomalies(readings: list[float]) -> list[float]:
    avg = statistics.mean(readings)
    return [r for r in readings if abs(r - avg) > ANOMALY_MARGING]

def build_report(readings: list[float]) ->str:
    counts = count_by_class(readings)
    anomalies = flag_anomalies(readings)
    lines = [
        f"Total readings: {len(readings)}",
        f"Mean: {statistics.mean(readings):.1f}",
        f"Median: {statistics.median(readings):.1f}",
        f"Minimum: {min(readings):.1f}",
        f"Maximum: {max(readings):.1f}",
        f"By class: {counts}",
        f"Anomalies: {[round(a, 1) for a in anomalies]}"
        f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}",
    ]
    return "\n".join(lines)

def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze temperature sensor readings.")
    parser.add_argument("--demo", action="store_true", help="use random demo data instead of prompting")
    args = parser.parse_args()

    if args.demo:
        readings = [round(random.uniform(-5, 45), 1) for _ in range(10)]
    else:
        readings = collect_readings()

    report = build_report(readings)
    print(report)

    with open("temp_readings.txt", "w", encoding="utf-8") as f:
        f.write(report)

    sys.exit(0)

if __name__ == "__main__":
    main()                 

