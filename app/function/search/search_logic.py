"""
Functionality for implementing data searching
- generate_searched_dataset
- implement_search_filter_relation
"""
import re

from fastapi import HTTPException, status
from irods.models import Collection, DataObjectMeta

from app.config import iRODSConfig

SEARCHFIELD = ["TITLE", "SUBTITLE", "CONTRIBUTOR"]


class SearchLogic:
    """
    Search logic functionality
    es -> external service object is required
    """

    def __init__(self, es):
        self.__es = es
        self.__search = SEARCHFIELD

    def _handle_searched_data(self, keyword_list):
        """
        Handler for processing search result, store the number of keyword appear
        """
        dataset_dict = {}
        for keyword in keyword_list:
            search_result = []
            for port in iRODSConfig.IRODS_PORT.split(","):
                irods_ = self.__es.use(f"irods_{port}")
                if irods_:
                    irods_query = irods_.process_keyword_search(self.__search, keyword)
                    if len(irods_query.all()) > 0:
                        search_result.append(irods_query)
            # Any keyword that does not match with the database content will cause search no result
            if not search_result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="There is no matched content in the database",
                )

            for query in search_result:
                for _ in query:
                    exist = re.findall(
                        rf"(\s{keyword}|{keyword}\s)", _[DataObjectMeta.value]
                    )
                    if exist:
                        dataset = re.sub(
                            f"{iRODSConfig.IRODS_ROOT_PATH}/",
                            "",
                            _[Collection.name],
                        )
                        if dataset not in dataset_dict:
                            dataset_dict[dataset] = 1
                        else:
                            dataset_dict[dataset] += 1
        return dataset_dict

    # The datasets order is based on how the dataset content is relevant to the input_ string.
    def generate_searched_dataset(self, input_):
        """
        Handler for generating the searched dataset
        """
        dataset_dict = {"submitter_id": []}
        keyword_list = re.findall("[a-zA-Z0-9]+", input_.lower())
        searched_result = self._handle_searched_data(keyword_list)
        dataset_dict["submitter_id"] = sorted(
            searched_result, key=searched_result.get, reverse=True
        )
        return dataset_dict

    def implement_search_filter_relation(self, item):
        """
        Handler for processing relation between search and filter
        """
        # Search result has order, we need to update item.filter value based on search result
        # The relationship between search and filter will always be AND
        if item.filter != {}:
            datasets = []
            for dataset_id in item.search["submitter_id"]:
                if dataset_id in item.filter["submitter_id"]:
                    datasets.append(dataset_id)
            item.filter["submitter_id"] = datasets
            return datasets
        item.filter["submitter_id"] = item.search["submitter_id"]
        return item.search["submitter_id"]
