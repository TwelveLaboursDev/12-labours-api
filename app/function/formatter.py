"""
Base formatting class
- handle_thumbnail
- handle_manifest
- handle_name_object
"""
import json
import re


class Formatter:
    """
    Functionality for formatting data
    """

    def handle_thumbnail(self, data):
        """
        Handler for updating thumbnail
        """
        result = []
        if not data:
            return result
        for _ in data:
            if _["additional_types"] is None:
                result.append(_)
        return result

    def _handle_multiple_cite_path(self, filename, cite):
        """
        Handler for updating multiple cite path
        """
        full_path = ""
        result = {"path": [], "relative": {"path": []}}
        data = json.loads(re.sub("'", '"', cite))
        for _ in data:
            full_path_list = filename.split("/")
            full_path_list[-1] = _.split("/")[-1]
            full_path = "/".join(full_path_list)
            result["path"].append(full_path)
            result["relative"]["path"].append(_.split("/")[-1])
        return result

    # filename: (contains full file path), cite: isDerivedFrom/isDescribedBy/isSourceOf
    def _handle_cite_path(self, filename, cite):
        """
        Handler for updating cite path
        """
        cite_path = self._handle_empty(cite)
        full_path = ""
        result = {"path": [], "relative": {"path": []}}
        if cite_path:
            if len(cite_path.split(",")) > 1:
                result = self._handle_multiple_cite_path(filename, cite_path)
                return result
            full_path_list = filename.split("/")
            full_path_list[-1] = cite_path.split("/")[-1]
            full_path = "/".join(full_path_list)
        result["path"].append(full_path)
        result["relative"]["path"].append(cite_path.split("/")[-1])
        return result

    def _handle_empty(self, data):
        """
        Handler for updating empty value
        """
        if data is None or data == "NA":
            return ""
        return data

    def _handle_image_link(self, preview, filename, is_source_of, has_image):
        """
        Handler for updating the image url
        """
        result = preview
        if has_image:
            if is_source_of:
                path_list = filename.split("/")
                path_list[-1] = is_source_of.split("/")[-1]
                filepath = "/".join(path_list)
                result += filepath
            else:
                result += filename
        else:
            return ""
        return result

    def handle_manifest(self, uuid, preview, data, has_image=False):
        """
        Handler for updating the data format which be queried based on manifest structure
        """
        result = []
        for _ in data:
            filename = _["filename"]
            item = {
                "image_url": self._handle_image_link(
                    preview,
                    filename,
                    self._handle_empty(_["is_source_of"]),
                    has_image,
                ),
                "additional_metadata": self._handle_empty(_["additional_metadata"]),
                "additional_mimetype": {
                    "name": self._handle_empty(_["additional_types"])
                },
                "datacite": {
                    "isDerivedFrom": self._handle_cite_path(
                        filename, _["is_derived_from"]
                    ),
                    "isDescribedBy": self._handle_cite_path(
                        filename, _["is_described_by"]
                    ),
                    "isSourceOf": self._handle_cite_path(filename, _["is_source_of"]),
                    "supplemental_json_metadata": {
                        "description": self._handle_empty(
                            _["supplemental_json_metadata"]
                        )
                    },
                },
                "dataset": {
                    "identifier": uuid,
                    "path": filename,
                },
                "file_type": {
                    "name": self._handle_empty(_["file_type"]),
                },
                "identifier": _["id"],
                "name": filename.split("/")[-1],
            }
            result.append(item)
        return result

    def handle_name_object(self, data, capitalize=False):
        """
        Handler for updating string content to object format.
        For fields in dataset_description node.
        [
            {"name": ""},
            ...
        ]
        """
        result = []
        if not data:
            return result
        for _ in data:
            if capitalize:
                name = {"name": _.capitalize()}
            else:
                name = {"name": _}
            result.append(name)
        return result
