from pathlib import Path
import yaml

PFFPATH="/Users/user/work/manchester/eScience/TREvolution/SATRE_work/sacro_create_crate_tool/tests/provenance/user;/Users/user/work/manchester/eScience/TREvolution/SATRE_work/sacro_create_crate_tool/tests/provenance/project;/Users/user/work/manchester/eScience/TREvolution/SATRE_work/sacro_create_crate_tool/tests/provenance/tre"


class ProvData():

    def __init__(self,
                 pffpath=PFFPATH):
        self.serviceData = {}
        self.provSourceFiles = []
        self.__check_and_list_source_files(pffpath)


    def __check_and_list_source_files(self, pffpath):
        pathStrings = pffpath.split(";")
        for pathString in pathStrings:
            path = Path(pathString)
            if path.is_dir():
                pffFiles = list(path.glob("**/*.pff"))
                self.provSourceFiles += pffFiles 


    def load_pff_data(self,services):
        servicesProcess = services
        for sourceFile in self.provSourceFiles:
            servicesListNew = []
            with open(sourceFile, 'r') as f:
                data = yaml.load(f, Loader=yaml.SafeLoader)
                for service in servicesProcess:
                    if service in data.keys():
                        self.serviceData[service] = data[service]
                    else:
                        servicesListNew.append(service)
            if not servicesListNew:
                break
            else:
                servicesProcess = servicesListNew
