# utils/log_reader.py
import json
import os


class MissionLogReader:
    def __init__(self, log_file="mission_log.jsonl"):
        self.log_file = log_file

    # ------------------------------------------------------------------
    # PRIMARY METHODS — TM3 can use these directly in Streamlit
    # ------------------------------------------------------------------
    def read_all(self):
        """
        Reads entire mission log and returns list of all tick payloads.
        TM3 uses this to display full mission history on dashboard.
        """
        if not os.path.exists(self.log_file):
            return []

        entries = []
        with open(self.log_file, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
        return entries

    def read_latest(self):
        """
        Returns only the most recent tick payload.
        TM3 uses this to display current rover status.
        """
        entries = self.read_all()
        if not entries:
            return None
        return entries[-1]

    def read_last_n(self, n=10):
        """
        Returns last n ticks — useful for recent history panel on dashboard.
        """
        entries = self.read_all()
        return entries[-n:] if len(entries) >= n else entries

    def get_summary(self):
        """
        Returns a quick summary of the full mission.
        TM3 uses this for the mission statistics panel.
        """
        entries = self.read_all()
        if not entries:
            return {"error": "No mission data found"}

        first = entries[0]
        last  = entries[-1]

        # Calculate battery consumed across mission
        start_battery = first["sensors"]["battery_level_percent"]
        end_battery   = last["sensors"]["battery_level_percent"]
        battery_used  = round(start_battery - end_battery, 2)

        return {
            "total_ticks":       len(entries),
            "start_position":    first["navigation"]["current_position"],
            "final_position":    last["navigation"]["current_position"],
            "destination":       last["navigation"]["destination"],
            "final_state":       last["system_status"]["state"],
            "battery_start":     start_battery,
            "battery_end":       end_battery,
            "battery_consumed":  battery_used,
            "mission_start":     first["timestamp"],
            "mission_end":       last["timestamp"]
        }


# ------------------------------------------------------------------
# QUICK TEST — run this file directly to verify
# ------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    reader = MissionLogReader(log_file="mission_log.jsonl")

    print("=== LATEST TICK ===")
    latest = reader.read_latest()
    if latest:
        print(json.dumps(latest, indent=2))
    else:
        print("No data found — run main.py first")

    print("\n=== LAST 3 TICKS ===")
    last_3 = reader.read_last_n(3)
    for entry in last_3:
        print(f"  {entry['timestamp']} | "
              f"pos={entry['navigation']['current_position']} | "
              f"battery={entry['sensors']['battery_level_percent']}%")

    print("\n=== MISSION SUMMARY ===")
    summary = reader.get_summary()
    for key, value in summary.items():
        print(f"  {key:<20}: {value}")