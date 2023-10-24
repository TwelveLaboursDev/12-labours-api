"""
Functionality for processing pagination related logic
- get_pagination_data
- get_pagination_count
- process_pagination_item
"""
import json
import queue
import threading

from fastapi import HTTPException, status

from app.config import Gen3Config
from app.data_schema import GraphQLPaginationItem, GraphQLQueryItem


class PaginationLogic:
    """
    fe -> filter editor object is required
    fl -> filter logic object is required
    sl -> search logic object is required
    es -> external service object is required
    """

    def __init__(self, fe, fl, sl, es):
        self.__filter_cache = fe.cache_loader()
        self.__fl = fl
        self.__sl = sl
        self.__es = es
        self.__public_access = Gen3Config.GEN3_PUBLIC_ACCESS.split(",")
        self.__private_filter = None

    def set_private_filter(self, filter_):
        """
        Handler for setting private_filter
        """
        self.__private_filter = filter_

    def _handle_dataset(self, data):
        """
        Handler for generating dataset dictionary
        """
        dataset_dict = {}
        for dataset in data:
            dataset_id = dataset["submitter_id"]
            if dataset_id not in dataset_dict:
                dataset_dict[dataset_id] = dataset
            else:
                dataset_id = f"{dataset['submitter_id']}-{dataset['id']}"
                dataset_dict[dataset_id] = dataset
        return dataset_dict

    def _handle_thread_fetch(self, items):
        """
        Handler for using thread to fetch data
        """
        queue_ = queue.Queue()
        threads_pool = []
        for args in items:
            thread = threading.Thread(
                target=self.__es.use("gen3").process_graphql_query, args=(*args, queue_)
            )
            threads_pool.append(thread)
            thread.start()
        for thread in threads_pool:
            thread.join()
        result = {}
        while not queue_.empty():
            data = queue_.get()
            result.update(data)
        return result

    def _handle_order_by_dataset_description(self, filter_):
        """
        Handler for updating submitter_id for order by dataset description
        """
        result = {}
        if "submitter_id" in filter_:
            result["submitter_id"] = []
            for dataset in filter_["submitter_id"]:
                result["submitter_id"].append(f"{dataset}-dataset_description")
        return result

    def _handle_pagination_order(self, item):
        """
        Handler for updating pagination data order
        """
        query_item = GraphQLQueryItem(
            node="pagination_order_by_dataset_description",
            limit=item.limit,
            page=item.page,
            filter=self._handle_order_by_dataset_description(item.filter),
            access=item.access,
            asc=item.asc,
            desc=item.desc,
        )
        if "asc" in item.order:
            query_item.asc = "title"
        elif "desc" in item.order:
            query_item.desc = "title"
        # Include both public and private if have the access
        ordered_datasets = []
        query_result = self.__es.use("gen3").process_graphql_query(query_item)
        for _ in query_result:
            dataset_id = _["experiments"][0]["submitter_id"]
            if dataset_id not in ordered_datasets:
                ordered_datasets.append(dataset_id)
        return ordered_datasets

    def get_pagination_data(self, item, match_pair, is_public_access_filtered):
        """
        Handler for fetching data based on pagination item
        """
        if "title" in item.order.lower():
            # Get an ordered filter
            order_result = self._handle_pagination_order(item)
            item.filter["submitter_id"] = order_result
            item.page = 1

        query_item = GraphQLPaginationItem(
            limit=item.limit,
            page=item.page,
            filter=item.filter,
            access=item.access,
            order=item.order,
            asc=item.asc,
            desc=item.desc,
        )
        query_result = self.__es.use("gen3").process_graphql_query(query_item)
        displayed_dataset = self._handle_dataset(query_result)

        items = []
        # match_pair only exist when there is private_access
        if match_pair:
            private_access = list(set(item.access) - set(self.__public_access))
            # Query displayed datasets which have private version
            for dataset_id in match_pair:
                if dataset_id in displayed_dataset:
                    query_item = GraphQLQueryItem(
                        node="experiment_query",
                        filter={"submitter_id": [dataset_id]},
                        access=private_access,
                    )
                    items.append((query_item, dataset_id))

            if not is_public_access_filtered:
                fetch_result = self._handle_thread_fetch(items)
                # Replace the dataset if it has a private version
                for dataset_id, dataset in fetch_result.items():
                    displayed_dataset[dataset_id] = dataset[0]
        return list(displayed_dataset.values())

    def get_pagination_count(self, item):
        """
        Handler for processing the number of data based on pagination item
        """
        user_access = {
            "public_access": self.__public_access,
            "private_access": None,
        }
        private_access = list(set(item.access) - set(self.__public_access))
        if private_access:
            user_access["private_access"] = private_access

        # Used to get the total count for either public or private datasets
        # Public or private datasets will be processed separately
        items = []
        for access_type, access in user_access.items():
            if access:
                pagination_count_item = GraphQLPaginationItem(
                    node="experiment_pagination_count",
                    filter=item.filter,
                    access=access,
                )
                items.append((pagination_count_item, access_type))
        fetch_result = self._handle_thread_fetch(items)

        # Default datasets exist in public repository only,
        # Will contain all available datasets after updating
        displayed_dataset = list(
            map(lambda d: d["submitter_id"], fetch_result["public_access"])
        )
        # Only exist when there is extra private access
        match_pair = []

        if private_access:
            private_dataset = list(
                map(lambda d: d["submitter_id"], fetch_result["private_access"])
            )
            # Datasets which exist in both public and private repository will be added to match_pair
            # It will be used to help achieve priority presentation of private datasets
            for dataset_id in private_dataset:
                if dataset_id not in displayed_dataset:
                    displayed_dataset.append(dataset_id)
                else:
                    match_pair.append(dataset_id)
        return len(displayed_dataset), match_pair

    def _handle_pagination_item_filter(self, filter_field, facets):
        """
        Handler for updating filter in pagination item
        """
        value_list = []
        for facet in facets:
            # Use .capitalize() to make it non-case sensitive
            # Avoid mis-match
            facet_name = facet.capitalize()
            for mapped_element in self.__filter_cache:
                if mapped_element in self.__private_filter:
                    content = self.__private_filter[mapped_element]
                else:
                    content = self.__filter_cache[mapped_element]
                # Check if title can match with a exist filter object
                if content["field"] == filter_field:
                    # Check if ele_name is a key under filter object element field
                    if facet_name not in content["facets"]:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid or unauthorized facet passed in",
                        )

                    facet_value = content["facets"][facet_name]
                    if isinstance(facet_value, list):
                        value_list.extend(facet_value)
                    else:
                        value_list.append(facet_value)
        return {filter_field: value_list}

    def process_pagination_item(self, item, input_):
        """
        Handler for process pagination item to fit the query code generator format
        """
        is_public_access_filtered = False
        has_search_result = False

        # FILTER
        if item.filter:
            items = []
            for node_filed, facets in item.filter.items():
                filter_node = node_filed.split(">")[0]
                filter_field = node_filed.split(">")[1]
                # Update filter based on authority
                valid_filter = self._handle_pagination_item_filter(filter_field, facets)
                query_item = GraphQLQueryItem(
                    node=filter_node, filter=valid_filter, access=self.__public_access
                )
                if filter_node == "experiment_filter":
                    query_item.access = valid_filter["project_id"]
                    public_access_filtered = list(
                        set(self.__public_access).intersection(query_item.access)
                    )
                    if public_access_filtered:
                        is_public_access_filtered = True
                else:
                    query_item.access = item.access
                items.append((query_item, json.dumps(valid_filter)))
            fetch_result = self._handle_thread_fetch(items)
            item.filter = self.__fl.generate_filtered_dataset(fetch_result)
            self.__fl.implement_filter_relation(item)

        # SEARCH
        if input_:
            # If input does not match any content in the database, item.search will be empty
            item.search = self.__sl.generate_searched_dataset(input_)
            if item.search["submitter_id"] and (
                "submitter_id" not in item.filter or item.filter["submitter_id"]
            ):
                has_search_result = True
                self.__sl.implement_search_filter_relation(item)
            if not has_search_result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="There is no matched content in the database",
                )

        # ORDER
        order_type = item.order.lower()
        if order_type == "published(asc)":
            item.asc = "created_datetime"
        elif order_type == "published(desc)":
            item.desc = "created_datetime"
        elif "title" in order_type:
            # See function self.get_pagination_data
            pass
        elif "relevance" in order_type:
            # relevance is for search function applied
            # search_filter_relation has already sort the datasets
            # If search not applied and relevance order chose
            # Order the datasets with created_datetime asc order by default
            if not has_search_result:
                item.asc = "created_datetime"
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{item.order} order option not provided",
            )
        return is_public_access_filtered
