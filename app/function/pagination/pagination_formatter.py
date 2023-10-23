"""
Functionality for constructing pagination format
- construct_pagination_format
"""
from app.function.formatter import Formatter


class PaginationFormatter(Formatter):
    """
    fe -> filter editor object is required
    """

    def __init__(self, fe):
        self.__filter_cache = fe.cache_loader()

    def _handle_species(self, data):
        """
        Handler for updating the species format
        """
        result = []
        if not data:
            return result
        for _ in data:
            if _["species"] != "NA":
                species_filter = self.__filter_cache["MAPPED_SPECIES"]["facets"]
                facets = species_filter.values()
                if _["species"] in facets:
                    index = list(facets).index(_["species"])
                    species = list(species_filter.keys())[index]
                else:
                    species = _["species"]
                if species not in result:
                    result.append(species)
        return result

    def construct_pagination_format(self, data):
        """
        Reconstructing the structure to support portal services
        """
        result = []
        for _ in data:
            dataset_description = _["dataset_descriptions"][0]
            submitter_id = _["submitter_id"]
            uuid = _["id"]
            preview_url_middle = f"/data/preview/{submitter_id}/"
            dataset_format = {
                "data_url_suffix": f"/data/browser/dataset/{submitter_id}?datasetTab=abstract",
                "source_url_middle": f"/data/download/{submitter_id}/",
                "contributors": super().handle_name_object(
                    dataset_description["contributor_name"]
                ),
                "keywords": dataset_description["keywords"],
                "numberSamples": int(dataset_description["number_of_samples"][0]),
                "numberSubjects": int(dataset_description["number_of_subjects"][0]),
                "name": dataset_description["title"][0],
                "datasetId": submitter_id,
                "organs": dataset_description["study_organ_system"],
                "species": self._handle_species(_["cases"]),
                "plots": super().handle_manifest(uuid, preview_url_middle, _["plots"]),
                "scaffoldViews": super().handle_manifest(
                    uuid, preview_url_middle, _["scaffoldViews"], True
                ),
                "scaffolds": super().handle_manifest(
                    uuid, preview_url_middle, _["scaffolds"]
                ),
                "thumbnails": super().handle_manifest(
                    uuid,
                    preview_url_middle,
                    super().handle_thumbnail(_["thumbnails"]),
                    True,
                ),
                "mris": super().handle_manifest(uuid, preview_url_middle, _["mris"]),
                "dicomImages": super().handle_manifest(
                    uuid, preview_url_middle, _["dicomImages"]
                ),
                "detailsReady": True,
            }
            result.append(dataset_format)
        return result
