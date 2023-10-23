"""
Functionality for processing query data output
- set_query_mode
- set_private_filter
- process_data_output
"""
import re

from app.function.formatter import Formatter


class QueryFormatter(Formatter):
    """
    fe -> filter editor object is required
    """

    def __init__(self, fe):
        self.__filter_cache = fe.cache_loader()
        self.__query_mode = None
        self.__private_filter = None

    def set_query_mode(self, mode):
        """
        Handler for setting query_mode
        """
        self.__query_mode = mode

    def set_private_filter(self, filter_):
        """
        Handler for setting private_filter
        """
        self.__private_filter = filter_

    def _handle_mri_path(self, data):
        """
        Handler for generating related mri paths
        """
        mri_paths = {}
        for _ in data:
            filepath = _["filename"]
            start = filepath.rindex("/") + 1
            end = filepath.rindex("_")
            filename = filepath[start:end]
            if filename not in mri_paths:
                mri_paths[filename] = [filepath]
            else:
                mri_paths[filename].append(filepath)
        return mri_paths

    def _update_facet_mode(self, related_facets, facet_name, content):
        """
        Handler for updating facet mode related facets
        """
        if facet_name not in related_facets:
            # Based on map integrated viewer map sidebar required filter format
            facet_format = {}
            facet_format["facet"] = facet_name
            facet_format["term"] = content["title"].capitalize()
            facet_format["facetPropPath"] = f"{content['node']}>{content['field']}"
            related_facets[facet_name] = facet_format

    def _update_detail_mode(self, related_facets, facet_name, content):
        """
        Handler for updating detail mode related facets
        """
        title = content["title"].capitalize()
        if title in related_facets:
            if facet_name not in related_facets[title]:
                related_facets[title].append(facet_name)
        else:
            related_facets[title] = [facet_name]

    def _handle_facet_check(self, facet_value, field_value):
        """
        Handler for checking whether facet exist
        """
        if isinstance(facet_value, str):
            # For study_organ_system
            # Array type field
            if isinstance(field_value, list) and facet_value in field_value:
                return True
            # For age_category/species
            # String type field
            elif field_value == facet_value:
                return True
        # For additional_types/sex
        elif isinstance(facet_value, list) and field_value in facet_value:
            return True
        return False

    def _update_related_facet(self, related_facets, field, data):
        """
        Handler for updating related facet
        """
        mapped_element = f"MAPPED_{field.upper()}"
        content = self.__filter_cache[mapped_element]
        if mapped_element in self.__private_filter:
            content = self.__private_filter[mapped_element]
        for facet_name, facet_value in content["facets"].items():
            for _ in data:
                field_value = _[field]
                if self._handle_facet_check(facet_value, field_value):
                    if self.__query_mode == "detail":
                        self._update_detail_mode(related_facets, facet_name, content)
                    elif self.__query_mode == "facet":
                        self._update_facet_mode(related_facets, facet_name, content)

    def _handle_facet_source(self):
        """
        Handler for generating facet source
        """
        sources = []
        for mapped_content in self.__filter_cache.values():
            node = re.sub("_filter", "s", mapped_content["node"])
            field = mapped_content["field"]
            if node == "experiments":
                pass
            elif node == "manifests":
                sources.append(f"scaffolds>{field}")
                sources.append(f"plots>{field}")
                sources.append(f"dicomImages>{field}")
            else:
                sources.append(f"{node}>{field}")
        return sources

    def _handle_related_facet(self, data):
        """
        Handler for generating related facets for corresponding dataset
        """
        related_facets = {}
        for _ in self._handle_facet_source():
            key = _.split(">")[0]
            field = _.split(">")[1]
            if key in data and data[key]:
                self._update_related_facet(related_facets, field, data[key])
        if self.__query_mode == "detail":
            return related_facets
        result = list(related_facets.values())
        return result

    def handle_contributor(self, data):
        """
        Handler for updating contributor format.
        """
        result = []
        if not data:
            return result
        for _ in data:
            name_list = _.split(", ")
            if len(name_list) == 2:
                name = name_list[1] + " " + name_list[0]
            else:
                name = name_list[0]
            result.append(name)
        return result

    def _construct_query_format(self, data):
        """
        Reconstructing the structure to support portal services
        """
        dataset_description = data["dataset_descriptions"][0]
        submitter_id = data["submitter_id"]
        uuid = data["id"]
        preview_url_middle = f"/data/preview/{submitter_id}/"
        dataset_format = {
            "source_url_middle": f"/data/download/{submitter_id}/",
            "contributors": self.handle_contributor(
                dataset_description["contributor_name"]
            ),
            "contributor_orcid": dataset_description["contributor_orcid"],
            "contributor_affiliation": dataset_description["contributor_affiliation"],
            "identifier": dataset_description["identifier"],
            "identifier_type": dataset_description["identifier_type"],
            "keywords": super().handle_keyword(dataset_description["keywords"]),
            "numberSamples": int(dataset_description["number_of_samples"][0]),
            "numberSubjects": int(dataset_description["number_of_subjects"][0]),
            "study_purpose": dataset_description["study_purpose"],
            "name": dataset_description["title"][0],
            "subname": dataset_description["subtitle"][0],
            "datasetId": submitter_id,
            "plots": super().handle_manifest(uuid, preview_url_middle, data["plots"]),
            "scaffoldViews": super().handle_manifest(
                uuid, preview_url_middle, data["scaffoldViews"], True
            ),
            "scaffolds": super().handle_manifest(
                uuid, preview_url_middle, data["scaffolds"]
            ),
            "thumbnails": super().handle_manifest(
                uuid,
                preview_url_middle,
                super().handle_thumbnail(data["thumbnails"]),
                True,
            ),
            "mris": super().handle_manifest(uuid, preview_url_middle, data["mris"]),
            "dicomImages": super().handle_manifest(
                uuid, preview_url_middle, data["dicomImages"]
            ),
            "created": data["created_datetime"],
            "updated": data["updated_datetime"],
        }
        return dataset_format

    def _handle_mri(self, data):
        """
        Handler for updating mri data, keep one only
        """
        mris = []
        for _ in data:
            filepath = _["filename"]
            if "_c0" in filepath:
                _["filename"] = re.sub("_c0", "", _["filename"])
                mris.append(_)
        return mris

    def _handle_dicom_image(self, data):
        """
        Handler for updating dicom image data, keep one only
        """
        dicom_images = {}
        for _ in data:
            filepath = _["filename"]
            # Find the last "/" index in the file path
            index = filepath.rindex("/")
            folder_path = filepath[:index]
            # Keep only the first dicom data each folder
            if folder_path not in dicom_images:
                dicom_images[folder_path] = _
        result = list(dicom_images.values())
        return result

    def _handle_detail_content(self, data):
        """
        Handler for updating detail content
        """
        # Combine multiple files within the dataset into one
        # Only need to display one in the portal
        if data["dicomImages"]:
            data["dicomImages"] = self._handle_dicom_image(data["dicomImages"])
        if data["mris"]:
            data["mris"] = self._handle_mri(data["mris"])
        result = self._construct_query_format(data)
        return result

    def process_data_output(self, data):
        """
        Handler for processing data output to support portal services
        """
        result = {}
        if self.__query_mode == "data":
            result["data"] = data
        elif self.__query_mode == "detail":
            result["detail"] = self._handle_detail_content(data)
            # Filter format facet
            result["facet"] = self._handle_related_facet(data)
        elif self.__query_mode == "facet":
            # Sidebar format facet
            result["facet"] = self._handle_related_facet(data)
        elif self.__query_mode == "mri":
            # Combine 5 sub-file paths based on filename
            result["mri"] = self._handle_mri_path(data["mris"])
        return result
