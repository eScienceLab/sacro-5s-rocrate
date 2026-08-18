from pathlib import Path
import argparse
from fivesafe_crate import FiveSafesCrate

PFFPATH="/Users/user/work/manchester/eScience/TREvolution/SATRE_work/sacro_create_crate_tool/tests/provenance/user;/Users/user/work/manchester/eScience/TREvolution/SATRE_work/sacro_create_crate_tool/tests/provenance/project;/Users/user/work/manchester/eScience/TREvolution/SATRE_work/sacro_create_crate_tool/tests/provenance/tre"

def load_pff_data(services):
    serviceData = {}
    pathStrings = PFFPATH.split(";")
    paths = []
    for pathString in pathstrings:
        path = Path(pathString)
        if path.is_dir():
            pffFiles = list(path.glob("**/*.pff"))
            paths += pffFiles 
    
    servicesProcess = services
    for path in paths:
        serviceListNew = []
        with open(path, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            for service in servicesProcess:
                if service in data.keys():
                    serviceData[service] = data[service]
                else:
                    servicesListNew.append(service)
        if not servicesListNew:
            break
        else:
            servicesProcess = servicesListNew
    
    return(serviceData)



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

    crate.write("./")
    print("finished writing crate metadata")
    
if __name__ == "__main__":
    main()
