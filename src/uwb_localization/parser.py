import os
import re
import time
import threading
import subprocess

from config import (
    LAST_DISTANCE,
    STATUS,
    TOF,
    ANGLE,
    MEASUREMENTS,
    LAST_UPDATE,
    SPEED_OF_LIGHT,
    ALPHA,
    MIN_DISTANCE,
    MAX_DISTANCE,
    TIMEOUT,
)


class UWBParser:

    def __init__(self):

        self.current_mac = None
        self.current_status = None

        self.cmd = [
            "/home/pi1/uwb_venv/bin/python3",
            "scripts/fira/run_fira_twr/run_fira_twr.py",
            "-p", "/dev/ttyACM0",
            "--session", "1",
            "--node", "onetomany",
            "--mac", "0x0",
            "--dest-mac", "[0x1,0x2,0x3,0x4]",
            "--n_controlees", "4",
            "-t", "-1"
        ]

    def start(self):

        thread = threading.Thread(
            target=self.reader,
            daemon=True
        )

        thread.start()

    def reader(self):

        env = os.environ.copy()

        env["PYTHONPATH"] = "/home/pi1/uwb-qorvo-tools"

        process = subprocess.Popen(
            self.cmd,
            cwd="/home/pi1/uwb-qorvo-tools",
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in process.stdout:

            print(line, end="")

            line_lower = line.lower()

            # ------------------------------
            # STATUS
            # ------------------------------

            if "status:" in line_lower:

                if "ok" in line_lower:

                    self.current_status = "OK"

                else:

                    self.current_status = "TIMEOUT"

            # ------------------------------
            # MAC ADDRESS
            # ------------------------------

            elif "mac address:" in line_lower:

                match = re.search(
                    r'([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2})',
                    line
                )

                if match:

                    self.current_mac = match.group(1)

            # ------------------------------
            # DISTANCE
            # ------------------------------

            elif "distance:" in line_lower:

                if self.current_status != "OK":

                    continue

                match = re.search(
                    r'([0-9.]+)\s*cm',
                    line
                )

                if not match:

                    continue

                if self.current_mac is None:

                    continue

                if self.current_mac not in LAST_DISTANCE:

                    continue

                distance = float(match.group(1)) / 100.0

                if (
                    distance < MIN_DISTANCE
                    or
                    distance > MAX_DISTANCE
                ):

                    continue

                previous = LAST_DISTANCE[self.current_mac]

                if previous is None:

                    filtered = distance

                else:

                    filtered = (
                        ALPHA * distance
                        +
                        (1 - ALPHA) * previous
                    )
                                    # ------------------------------
                # Store Filtered Distance
                # ------------------------------

                LAST_DISTANCE[self.current_mac] = filtered

                # ------------------------------
                # Estimated Time of Flight (ns)
                # ------------------------------

                TOF[self.current_mac] = (
                    filtered / SPEED_OF_LIGHT
                ) * 1e9

                # ------------------------------
                # Update Status
                # ------------------------------

                STATUS[self.current_mac] = "OK"

                # ------------------------------
                # Count Measurements
                # ------------------------------

                MEASUREMENTS[self.current_mac] += 1

                # ------------------------------
                # Save Last Update Time
                # ------------------------------

                LAST_UPDATE[self.current_mac] = time.time()

            # ------------------------------
            # Timeout Detection
            # ------------------------------

            current_time = time.time()

            for mac in LAST_UPDATE:

                if LAST_UPDATE[mac] == 0:
                    continue

                if current_time - LAST_UPDATE[mac] > TIMEOUT:

                    STATUS[mac] = "TIMEOUT"


# ==================================================
# Getter Functions
# ==================================================

def get_distances():

    return LAST_DISTANCE


def get_status():

    return STATUS


def get_tof():

    return TOF


def get_angles():

    return ANGLE


def get_measurements():

    return MEASUREMENTS


def get_last_update():

    return LAST_UPDATE
