"""
=========================================================
uwb_localization.py
Main Entry Point for UWB Indoor Localization
=========================================================
"""

from parser import UWBParser
from plotter import Plotter


def main():

    print("======================================")
    print(" UWB Localization Started")
    print("======================================")

    # Start UWB ranging parser
    parser = UWBParser()
    parser.start()

    # Start real-time visualization
    plotter = Plotter()
    plotter.start()


if __name__ == "__main__":
    main()
