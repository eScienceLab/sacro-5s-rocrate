from pathlib import Path
import os
import json
import argparse
from rocrate.rocrate import ROCrate


def create_empty_provenance_run_crate(rocrate_version="1.1"):
    crate = ROCrate(version=rocrate_version)
    crate.update_jsonld({
        "@id": "ro-crate-metadata.json",
        "conformsTo": [
            {"@id": f"https://w3id.org/ro/crate/{rocrate_version}"},
            {"@id": "https://w3id.org/workflowhub/workflow-ro-crate/1.0"}
        ]
    })
    crate.update_jsonld({
        "@id": "./",
        "conformsTo": [
            {"@id": "https://w3id.org/ro/wfrun/process/0.1"},
            {"@id": "https://w3id.org/ro/wfrun/workflow/0.1"},
            {"@id": "https://w3id.org/ro/wfrun/provenance/0.1"},
            {"@id": "https://w3id.org/workflowhub/workflow-ro-crate/1.0"}
        ]
    })
    return crate

def define_acro_json():
    acro_json = {
        "@id": "https://github.com/AI-SDC/acro",
        "@type": "SoftwareApplication",
        "identifier": {"@id": "https://doi.org/10.5281/zenodo.18456450"},
        "url": {"@id": "https://sacro-tools.org/"},
        "name": "ACRO",
        "version": "0.4.12"
    }
    return acro_json

def define_main_entity(mainentity):
    main_entity = {
        "@id": mainentity,
        "@type": ["File", "SoftwareSourceCode", "ComputationalWorkflow"],
        "name": mainentity,
        "programmingLanguage": {"@id": "https://github.com/AI-SDC/acro"}
    }
    return main_entity
    


def load_sacro_metadata(sacro_file):
    assert sacro_file.is_file(), f"{sacro_file} is not a file"
    with open(sacro_file) as f:
        data = json.load(f)
    return data


def move_to_crate(crate_path):
    assert crate_path.is_dir(), f"{crate_path} is not a directory"
    os.chdir(crate_path)
    print(f"moved to dir {crate_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--sacro', type=Path, default="results.json")
    parser.add_argument('--wffile', type=Path, default="analysis.py")
    

    args = parser.parse_args()

    move_to_crate(args.root)

    sacro_metadata = load_sacro_metadata(args.sacro)

    crate = create_empty_provenance_run_crate()
    crate.add_jsonld(define_main_entity(mainentity=str(args.wffile)))
    crate.add_jsonld(define_acro_json())
    
    crate.write("./")
    print("finished writing crate metadata")
