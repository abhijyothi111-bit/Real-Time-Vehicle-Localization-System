"""
=========================================================
plotter.py
Real-Time UWB Localization Visualization
=========================================================
"""

import math

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

from config import (
    ANCHORS,
    ANCHOR_NAMES,
    X_LIMIT,
    Y_LIMIT,
    TITLE,
    ANCHOR_COLOR,
    TAG_COLOR,
    CIRCLE_COLOR,
    LINE_COLOR,
    ANGLE_COLOR,
    OK_COLOR,
    WAITING_COLOR,
    TIMEOUT_COLOR,
    ANCHOR_SIZE,
    TAG_SIZE,
)

from parser import (
    get_distances,
    get_status,
    get_tof,
    get_angles,
    get_measurements,
)

from trilateration import multilaterate


class Plotter:

    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.animation = None

    def update(self, frame):

        self.ax.clear()

        # =================================================
        # Plot Configuration
        # =================================================

        self.ax.set_title(
            TITLE,
            fontsize=18,
            fontweight="bold",
            color="#1f2937",
            pad=15
        )

        self.ax.set_xlabel("X (meters)")
        self.ax.set_ylabel("Y (meters)")

        self.ax.set_xlim(*X_LIMIT)
        self.ax.set_ylim(*Y_LIMIT)

        self.ax.grid(
            True,
            linestyle="--",
            linewidth=0.7,
            alpha=0.35,
            color="gray"
        )

        self.ax.set_aspect(
            "equal",
            adjustable="box"
        )

        # =================================================
        # Get Latest Data
        # =================================================

        distances = get_distances()
        status = get_status()
        tof = get_tof()
        angles = get_angles()
        measurements = get_measurements()

        # =================================================
        # Draw Anchors and Ranging Circles
        # =================================================

        for mac, (x, y) in ANCHORS.items():

            if status[mac] == "OK":
                color = OK_COLOR

            elif status[mac] == "TIMEOUT":
                color = TIMEOUT_COLOR

            else:
                color = WAITING_COLOR

            # Anchor marker
            self.ax.scatter(
                x,
                y,
                s=180,
                color=color,
                edgecolors="black",
                linewidth=1.5,
                zorder=10
            )

            # Anchor label
            label = (
                f"{ANCHOR_NAMES[mac]}\n"
                f"({x:.2f}, {y:.2f})"
            )

            if distances[mac] is not None:
                label += (
                    f"\nD : "
                    f"{distances[mac]:.2f} m"
                )

            if tof[mac] is not None:
                label += (
                    f"\nToF : "
                    f"{tof[mac]:.2f} ns"
                )

            self.ax.text(
                x,
                y + 0.18,
                label,
                ha="center",
                fontsize=9,
                color=color,
                fontweight="bold"
            )

            # =================================================
            # Ranging Circle
            # =================================================

            if distances[mac] is not None:

                circle = Circle(
                    (x, y),
                    distances[mac],
                    fill=False,
                    linestyle="--",
                    linewidth=2.5,
                    color=CIRCLE_COLOR,
                    alpha=0.45
                )

                self.ax.add_patch(circle)

                self.ax.text(
                    x + 0.15,
                    y - 0.15,
                    f"{distances[mac]:.2f} m",
                    fontsize=9,
                    color=CIRCLE_COLOR
                )

        # =================================================
        # Collect Valid Anchor Measurements
        # =================================================

        valid_macs = []

        for mac in ANCHORS:

            if distances[mac] is not None:
                valid_macs.append(mac)

        # =================================================
        # Minimum Anchor Requirement
        # =================================================

        if len(valid_macs) < 3:

            self.ax.text(
                -1.8,
                6.3,
                "Waiting for 3 valid ranging measurements...",
                fontsize=11,
                color="red",
                fontweight="bold"
            )

            return

        # =================================================
        # Prepare Anchor Coordinates and Distances
        # =================================================

        valid_anchors = []
        valid_distances = []

        for mac in valid_macs:

            valid_anchors.append(
                ANCHORS[mac]
            )

            valid_distances.append(
                distances[mac]
            )

        # =================================================
        # Multilateration
        # =================================================

        pos = multilaterate(
            valid_anchors,
            valid_distances
        )

        if pos is None:

            self.ax.text(
                -1.8,
                6.3,
                "Unable to calculate tag position.",
                fontsize=11,
                color="red",
                fontweight="bold"
            )

            return

        tag_x = float(pos[0])
        tag_y = float(pos[1])

        # =================================================
        # Plot Tag
        # =================================================

        self.ax.scatter(
            tag_x,
            tag_y,
            marker="*",
            s=350,
            color=TAG_COLOR,
            edgecolors="black",
            linewidth=1.5,
            zorder=20
        )

        self.ax.text(
            tag_x,
            tag_y + 0.20,
            "TAG",
            fontsize=12,
            fontweight="bold",
            color=TAG_COLOR,
            ha="center"
        )

        # =================================================
        # Anchor → Tag Lines and Angles
        # =================================================

        for mac, (anchor_x, anchor_y) in ANCHORS.items():

            if distances[mac] is None:
                continue

            # Draw line
            self.ax.plot(
                [anchor_x, tag_x],
                [anchor_y, tag_y],
                linestyle=":",
                linewidth=2,
                color=LINE_COLOR
            )

            # Calculate angle
            angle = math.degrees(
                math.atan2(
                    tag_y - anchor_y,
                    tag_x - anchor_x
                )
            )

            angles[mac] = angle

            # Midpoint
            mid_x = (
                anchor_x + tag_x
            ) / 2

            mid_y = (
                anchor_y + tag_y
            ) / 2

            self.ax.text(
                mid_x,
                mid_y,
                f"{angle:.1f}°",
                fontsize=9,
                color=ANGLE_COLOR,
                fontweight="bold",
                bbox=dict(
                    facecolor="white",
                    edgecolor="none",
                    alpha=0.7
                )
            )

        # =================================================
        # Current Position Panel
        # =================================================

        self.ax.text(
            4.15,
            6.25,
            (
                "CURRENT POSITION\n\n"
                f"X : {tag_x:.2f} m\n"
                f"Y : {tag_y:.2f} m"
            ),
            fontsize=11,
            bbox=dict(
                facecolor="#ffffff",
                edgecolor="black",
                boxstyle="round,pad=0.6",
                alpha=0.95
            )
        )

        # =================================================
        # Live Calculation Panel
        # =================================================

        panel = "LIVE CALCULATIONS\n\n"

        for mac in ANCHORS:

            panel += (
                f"{ANCHOR_NAMES[mac]}\n"
            )

            panel += (
                f"Status : "
                f"{status[mac]}\n"
            )

            if distances[mac] is not None:

                panel += (
                    f"Distance : "
                    f"{distances[mac]:.2f} m\n"
                )

            else:

                panel += (
                    "Distance : --\n"
                )

            if tof[mac] is not None:

                panel += (
                    f"Estimated ToF : "
                    f"{tof[mac]:.2f} ns\n"
                )

            else:

                panel += (
                    "Estimated ToF : --\n"
                )

            if angles[mac] is not None:

                panel += (
                    f"Angle : "
                    f"{angles[mac]:.1f}°\n"
                )

            else:

                panel += (
                    "Angle : --\n"
                )

            panel += (
                f"Measurements : "
                f"{measurements[mac]}\n\n"
            )

        self.ax.text(
            -1.85,
            6.30,
            panel,
            fontsize=9,
            verticalalignment="top",
            bbox=dict(
                facecolor="white",
                edgecolor="black",
                alpha=0.90
            )
        )

        # =================================================
        # Legend
        # =================================================

        self.ax.scatter(
            [],
            [],
            color=ANCHOR_COLOR,
            s=ANCHOR_SIZE,
            label="Anchor"
        )

        self.ax.scatter(
            [],
            [],
            color=TAG_COLOR,
            s=TAG_SIZE,
            marker="*",
            label="Tag"
        )

        self.ax.plot(
            [],
            [],
            linestyle="--",
            color=CIRCLE_COLOR,
            label="Ranging Circle"
        )

        self.ax.plot(
            [],
            [],
            linestyle=":",
            color=LINE_COLOR,
            label="Anchor → Tag"
        )

        self.ax.legend(
            loc="upper right",
            fontsize=9
        )

        # =================================================
        # Status Information
        # =================================================

        self.ax.text(
            4.15,
            -0.70,
            (
                "STATUS\n\n"
                "Green : OK\n"
                "Orange : Waiting\n"
                "Red : Timeout"
            ),
            fontsize=9,
            bbox=dict(
                facecolor="white",
                edgecolor="black"
            )
        )

        # =================================================
        # Footer
        # =================================================

        self.ax.text(
            2.0,
            -0.90,
            "Real-Time UWB Indoor Localization "
            "using 4-Anchor Multilateration",
            fontsize=9,
            ha="center",
            color="gray"
        )

    def start(self):

        self.animation = FuncAnimation(
            self.fig,
            self.update,
            interval=200,
            cache_frame_data=False
        )

        plt.tight_layout()
        plt.show()