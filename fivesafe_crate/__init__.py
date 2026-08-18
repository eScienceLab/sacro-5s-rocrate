from rocrate.rocrate import ROCrate
from rocrate.model.contextentity import ContextEntity
from rocrate.model.person import Person

DEFAULT_VERSION = '1.0-draft'
DEFAULT_ROCRATE_VERSION = '1.2'


class FiveSafesCrate(ROCrate):

    def __init__(self,
                 source=None,
                 gen_preview=False,
                 init=False, exclude=None,
                 version=DEFAULT_VERSION,
                 rocrate_base_version=DEFAULT_ROCRATE_VERSION,
                 load_subcrates=False,
                 root_dataset_id=None,
                 record_identifier=None,
                 identifier=None
                 ):
        super().__init__(source, gen_preview, init, exclude,
                         rocrate_base_version, load_subcrates, root_dataset_id)
        
        self.add(ContextEntity(self, f"https://w3id.org/5s-crate/{version}",
					properties = {
						"@type": ["CreativeWork", "Profile"],
						"name": "Five Safes RO-Crate profile",
						"version": version
					}
                ))
        self.root_dataset["conformsTo"] = [{"@id": f"https://w3id.org/5s-crate/{version}"}]

        if record_identifier:
            self.recordIdentifier = {"@id":record_identifier}

        if identifier:
            self.identifier = {"@id":identifier}


    @property
    def recordIdentifier(self):
        self.root_dataset.get('dct:isVersionOf')

    @recordIdentifier.setter
    def recordIdentifier(self, value):
        self.root_dataset['dct:isVersionOf'] = value

    @property
    def identifier(self):
        self.root_dataset.get('identifier')

    @identifier.setter
    def identifier(self, value):
        self.root_dataset['identifier'] = value

    @property
    def currentVersion(self):
        self.root_dataset.get('version')

    @recordIdentifier.setter
    def currentVersion(self, value):
        self.root_dataset['version'] = value

    @property
    def previousVersion(self):
        self.root_dataset.get('version')

    @recordIdentifier.setter
    def previousVersion(self, value):
        self.root_dataset['pav:previousVersion'] = value



def create_empty_fivesafe_crate(rocrate_base_version="1.3",
                                rocrate_fivesafes_version="1.0-draft"
                                ):
    crate = ROCrate(version=rocrate_base_version)

    crate.update_jsonld({
        "@id": "./",
        "@type": "Dataset",
        "conformsTo": [
            {"@id": fivesafes_crate["@id"]}
        ],
        "identifier": "https://tre72.example.org/activities/A123/versions/2",
        "dct:isVersionOf": {"@id": "https://tre72.example.org/activities/A123"},
        "name": "sacro_validation",
        "description": "sacro validation",
        "datePublished": "now",
        "license": {"@id": "http://spdx.org/licenses/CC0-1.0"},
        "version": "2",
        
    })

    return crate