# SACRO 5-Safes RO-Crate Prototype

Example tooling for reading the contents of a SACRO `results.py` file and creating a provenance RO-Crate from this.


## Setup

This package has two dependencies which currently are not on pypi.

Clone the following repositories, and install them within the same virtual environment, following the instructions in their README's:
- https://github.com/eScienceLab/provff-py
- https://github.com/eScienceLab/5s-crate-py


## Usage

The tool help page can be accessed using:
```bash
python create_5s_crate.py --help
```

Once the tool is more developed this section will be expanded.

## Notes
 1. Need a `results.json` this comes from [SACRO](https://dareuk.org.uk/how-we-work/previous-activities/dare-uk-phase-1-driver-projects/sacro-semi-automated-checking-of-research-outputs/) process.
    * It contains a fair section wihch is ultimately what we're interested in.
    * That is consumed by the `sacro-5s-rocrate/create_5s_crate.py`
    * (@nimpo, find this in the `~/Project/SACRO5s/SACRO_Example_ROCrate` @douglowe sent you a tarball)
 3. Set up the .env such that it has a path PFFPATH as per env.example,
    ```
    export PFFPATH="tests/provenance/user:tests/provenance/project:tests/provenance/tre"
    ```
    * This needs to be the tests directory in this repo so if running outside of this in e.g.
      `REPO_HOME=/home/zzalsmaj/Repos/sacro-5s-rocrate`
      then need to set env thus:
      ```
      export PFFPATH="$REPO_HOME/tests/provenance/user:$REPO_HOME/tests/provenance/project:$REPO_HOME/tests/provenance/tre"
      ```
 5. Run with the command in the SACRO5s project environment 
    * The python virtual environment as discussed in [Setup](#Setup) above (For @nimpo this is venv in `~/Project/SACRO5s/` and the example is a subdirectory of this)
    ```
    python create_5s_crate.py --root ./SACRO_Example_ROCrate \
                              --sacro ./SACRO_Example_ROCrate/results.json \
                              --wffile ./SACRO_Example_ROCrate/analysis.py \
                              --input ./SACRO_Example_ROCrate/input_data.txt
    ```
