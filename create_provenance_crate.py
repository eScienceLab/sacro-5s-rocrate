from pathlib import Path
import os
import json
import argparse
from rocrate.rocrate import ROCrate
from rocrate.model.contextentity import ContextEntity
from rocrate.model.person import Person


def create_empty_provenance_run_crate(rocrate_version="1.1"):
    crate = ROCrate(version=rocrate_version)
    process_crate = crate.add(ContextEntity(
            crate, "https://w3id.org/ro/wfrun/process/0.5",
            properties = {
                "@type": "CreativeWork",
                "name": "Process Run Crate",
                "version": "0.5"
            }
    ))
    wfrun_crate = crate.add_jsonld({
        "@id": "https://w3id.org/ro/wfrun/workflow/0.5",
        "@type": "CreativeWork",
        "name": "Workflow Run Crate",
        "version": "0.5"
    })
    prov_crate = crate.add_jsonld({
        "@id": "https://w3id.org/ro/wfrun/provenance/0.5",
        "@type": "CreativeWork",
        "name": "Provenance Run Crate",
        "version": "0.5"
    })
    wf_crate = crate.add_jsonld({
        "@id": "https://w3id.org/workflowhub/workflow-ro-crate/1.0",
        "@type": "CreativeWork",
        "name": "Workflow RO-Crate",
        "version": "1.0"
    })
    crate.update_jsonld({
        "@id": "ro-crate-metadata.json",
        "conformsTo": [
            {"@id": f"https://w3id.org/ro/crate/{rocrate_version}"},
            {"@id": wf_crate["@id"]}
        ]
    })
    crate.update_jsonld({
        "@id": "./",
        "conformsTo": [
            {"@id": process_crate["@id"]},
            {"@id": wfrun_crate["@id"]},
            {"@id": prov_crate["@id"]},
            {"@id": wf_crate["@id"]}
        ],
        "name": "sacro_validation",
        "description": "sacro validation",
        "license": {"@id": "http://spdx.org/licenses/CC0-1.0"}
    })

    return crate

def get_acro_version(sacro_metadata):
    return sacro_metadata['version']

def define_programminglanguage():
    prog_json = {
        "@id": "sacro",
        "@type": "ComputerLanguage",
        "identifier": "https://sacro-tools.org/",
        "name": "SACRO",
        "url": "https://sacro-tools.org/"
    }
    return prog_json

def define_softwareapplication(version):
    soft_json = {
        "@id": "https://github.com/AI-SDC/acro",
        "@type": "SoftwareApplication",
        "identifier": {"@id": "https://doi.org/10.5281/zenodo.18456450"},
        "url": {"@id": "https://sacro-tools.org/"},
        "name": "ACRO",
        "version": version
    }
    return soft_json

def define_main_entity(mainentity):
    main_entity = {
        "@type": ["File", "SoftwareSourceCode", "ComputationalWorkflow"],
        "name": mainentity,
        "programmingLanguage": {"@id": "sacro"}
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


def get_output_steps_and_files(sacro_metadata):
    outputs_list = []
    for output in sacro_metadata["results"].keys():
        output_count = 0
        for file in sacro_metadata["results"][output]["files"]:
            outputs_list.append({
                         "tool": output,
                         "name": f"{output}_result_{output_count}",
                         "file": file["name"]
                         })
            output_count += 1
    return outputs_list

person_info = {
    "id": "https://orcid.org/0000-0000-0000-0000",
    "name": "Joe Doe",
    "affiliation": "Place University"
    }

def define_inputobject():
    input_object = {
        "@type": "FormalParameter",
        "additionalType": "File",
        "name": "input data",
        "description": "sample data for analysis",
        "conformsTo": {
            "@id": "https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE"
        },
        "valueRequired": "True"
    }
    return input_object

def define_outputobject():
    output_object = {
        "@type": "FormalParameter",
        "additionalType": "File",
        "name": "analysis result",
        "description": "analysis of input",
        "conformsTo": {
            "@id": "https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE"
        }
    }
    return output_object

def define_person(info):
    return {
        "name": info["name"],
        "affiliation": info["affiliation"]
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--sacro', type=Path, default="results.json")
    parser.add_argument('--wffile', type=Path, default="analysis.py")
    parser.add_argument('--input', type=Path, default="input_data.txt")

    args = parser.parse_args()

    move_to_crate(args.root)

    sacro_metadata = load_sacro_metadata(args.sacro)
    outputs_list = get_output_steps_and_files(sacro_metadata)

    crate = create_empty_provenance_run_crate()
    core_dataset = crate.get('./')

    workflow_object = crate.add_file(args.wffile,properties=define_main_entity(str(args.wffile)))
    core_dataset["mainEntity"] = workflow_object

    output_objects = [crate.add(ContextEntity(crate,outobj["name"],define_outputobject())) for outobj in outputs_list]
    input_objects = [crate.add(ContextEntity(crate, "input_data",define_inputobject()))]

    workflow_object["input"] = input_objects
    workflow_object["output"] = output_objects

    crate.add_jsonld(define_programminglanguage())
    crate.add_jsonld(define_softwareapplication(get_acro_version(sacro_metadata)))

    actor = crate.add(Person(crate, person_info["id"], properties=define_person(person_info)))

    input_file = crate.add_file(args.input)
    for output in outputs_list:
        file_object = crate.add_file(output["file"])



    crate.write("./")
    print("finished writing crate metadata")
