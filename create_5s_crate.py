from pathlib import Path
import argparse
from fivesafe_crate_py import FiveSafesCrate
from provff_py import ProvData


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--sacro', type=Path, default="results.json")
    parser.add_argument('--wffile', type=Path, default="analysis.py")
    parser.add_argument('--input', type=Path, default="input_data.txt")

    args = parser.parse_args()

    crate = FiveSafesCrate(root_dataset_id="https://tre72.example.org/activities/A123/current",
                            record_identifier="https://tre72.example.org/activities/A123",
                            identifier="https://tre72.example.org/activities/A123/current"
                          )
    provData = ProvData()
    provData.load_pff_data(["user"])

    crate.add_person_from_prov(provData.serviceData["user"])

    crate.write("./")
    print("finished writing crate metadata")
    
if __name__ == "__main__":
    main()
