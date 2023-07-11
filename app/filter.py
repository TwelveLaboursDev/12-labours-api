from app.data_schema import *

# This list contains all the "Array" type fields that used as a filter
FIELDS = [
    "study_organ_system"
]


class Filter(object):
    def __init__(self, fg):
        self.FG = fg
        self.FIELDS = FIELDS

    def get_fields(self):
        return self.FIELDS

    def generate_filtered_datasets(self, filter, field, data):
        result = []
        for dataset in data:
            for kwd in filter[field]:
                if kwd in dataset[field]:
                    result.append(dataset)
        return result

    def get_filtered_datasets(self, filter, data):
        field = list(filter.keys())[0]
        if field in FIELDS:
            data = self.generate_filtered_datasets(filter, field, data)
        dataset_list = []
        for record in data:
            if "experiments" in record:
                dataset_list.append(record["experiments"][0]["submitter_id"])
            else:
                # Implement filter in experiment node
                dataset_list.append(record["submitter_id"])
        return dataset_list

    def filter_relation(self, item):
        nested_list = item.filter["submitter_id"]
        if item.relation == "and":  # AND relationship
            dataset_list = set(nested_list[0]).intersection(*nested_list)
        elif item.relation == "or":  # OR relationship
            dataset_list = set()
            for sublist in nested_list:
                for id in sublist:
                    dataset_list.add(id)
        item.filter["submitter_id"] = list(dataset_list)

    def set_filter_dict(self, element, extra):
        FILTERS = self.FG.get_filters()
        if element in extra:
            return extra
        else:
            return FILTERS

    def generate_sidebar_filter_information(self, extra):
        FILTERS = self.FG.get_filters()
        sidebar_filter_information = []
        for element in FILTERS:
            filter_dict = self.set_filter_dict(element, extra)
            sidebar_filter_parent = {
                "key": "",
                "label": "",
                "children": [],
            }
            sidebar_filter_parent["key"] = filter_dict[element]["node"] + \
                ">" + filter_dict[element]["field"]
            sidebar_filter_parent["label"] = filter_dict[element]["title"]
            for ele in filter_dict[element]["element"]:
                sidebar_filter_children = {
                    "facetPropPath": "",
                    "label": "",
                }
                sidebar_filter_children["facetPropPath"] = sidebar_filter_parent["key"]
                sidebar_filter_children["label"] = ele
                sidebar_filter_parent["children"].append(
                    sidebar_filter_children)
            sidebar_filter_information.append(sidebar_filter_parent)
        return sidebar_filter_information

    def generate_filter_information(self, extra):
        FILTERS = self.FG.get_filters()
        filter_information = {
            "size": len(FILTERS),
            "titles": [],
            "nodes": [],
            "fields": [],
            "elements": [],
            "ids": []
        }
        for element in FILTERS:
            filter_dict = self.set_filter_dict(element, extra)
            filter_information["titles"].append(filter_dict[element]["title"])
            filter_information["nodes"].append(filter_dict[element]["node"])
            filter_information["fields"].append(filter_dict[element]["field"])
            filter_information["elements"].append(
                filter_dict[element]["element"])
            for ele in filter_dict[element]["element"]:
                filter_information["ids"].append(ele)
        return filter_information
