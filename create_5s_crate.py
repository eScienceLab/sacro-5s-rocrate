#!/usr/bin/env python3

from pathlib import Path
import argparse
from fivesafe_crate_py import FiveSafesCrate
from provff_py import ProvData
from datetime import datetime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--sacro', type=Path, default="results.json", help='Path to the SACRO results.json to use')
    parser.add_argument('--wffile', type=Path, default="analysis.py", help='TODO explain analysis.py')
    parser.add_argument('--input', type=Path, default="input_data.txt",  help='TODO explain input_data.txt')
    parser.add_argument('--output', type=Path, default=None)

    args = parser.parse_args()
    if args.output is None:
        args.output = args.root if args.root is not None else Path(".")

    crate = FiveSafesCrate(root_dataset_id="https://tre72.example.org/activities/A123/current",
                            record_identifier="https://tre72.example.org/activities/A123",
                            identifier="https://tre72.example.org/activities/A123/current"
                          )
    provData = ProvData()
    provData.load_pff_data(["user"])

    crate.add_person_from_prov(provData.serviceData["user"])


    # Special handling default is to write to ./ but that is in the pwd whereas crate.write should place inside the crate no?
    # so if output is specified and is a directory, then add ro-crate-metadata.json in that location
    if args.output.is_dir():
        out = args.output / 'ro-crate-metadata.json'
        if out.exists():
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            noclobber = out.with_name(f"{out.stem}-{timestamp}{out.suffix}")
            print("moving inferred",out,"to",noclobber)
            out.rename(noclobber)
        print("New metadata file in ", args.output / 'ro-crate-metadata.json')
        crate.write_detached(args.output / 'ro-crate-metadata.json') # Need to write detached apparently as crate lib doesn't know where to put file otherwise
    else:
        out = args.output
        if out.exists():
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            noclobber = out.with_name(f"{out.stem}-{timestamp}{out.suffix}")
            print("moving specified ",out,"to",noclobber)
            out.rename(noclobber)
        print("New metadata file in ", args.output )
        crate.write(args.output)

if __name__ == "__main__":
    main()
