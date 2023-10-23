from tests.test_function.test_query.fixture import (
    dummy_filter_cache,
    dummy_filter_cache_private,
    dummy_query_data,
    qf_class,
)


def test_process_data_output_mode_data(qf_class, dummy_query_data):
    mode = "data"
    qf_class.set_query_mode(mode)
    qf_class.set_private_filter({})
    output = qf_class.process_data_output(dummy_query_data)
    assert output[mode] == dummy_query_data


def test_process_data_output_mode_detail(qf_class, dummy_query_data):
    mode = "detail"
    qf_class.set_query_mode(mode)
    qf_class.set_private_filter({})
    output = qf_class.process_data_output(dummy_query_data)
    detail = output["detail"]
    assert detail["source_url_middle"] == "/data/download/dummy submitter/"
    assert detail["contributors"] == [
        {
            "name": "dummy name",
        },
    ]
    assert detail["contributor_orcids"] == [
        {
            "name": "dummy orcid",
        },
    ]
    assert detail["contributor_affiliations"] == [
        {
            "name": "dummy affiliation",
        },
    ]
    assert detail["identifier"] == [
        {
            "name": "dummy identifier",
        },
    ]
    assert detail["identifier_type"] == [
        {
            "name": "dummy identifier type",
        },
    ]
    assert detail["keywords"] == [
        {
            "name": "Dummy keyword",
        },
    ]
    assert detail["numberSamples"] == 12
    assert detail["numberSubjects"] == 12
    assert detail["study_purpose"] == [
        {
            "name": "dummy purpose",
        },
    ]
    assert detail["name"] == "dummy title"
    assert detail["subname"] == "dummy subtitle"
    assert detail["datasetId"] == "dummy submitter"
    assert detail["plots"] == [
        {
            "image_url": "",
            "additional_metadata": "",
            "additional_mimetype": {
                "name": "text/vnd.abi.plot+tab-separated-values",
            },
            "datacite": {
                "isDerivedFrom": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "isDescribedBy": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "isSourceOf": {
                    "path": [""],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "supplemental_json_metadata": {
                    "description": "",
                },
            },
            "dataset": {
                "identifier": "dummy id",
                "path": "dummy_filepath/dummy_filename.csv",
            },
            "file_type": {
                "name": ".csv",
            },
            "identifier": "dummy id",
            "name": "dummy_filename.csv",
        },
        {
            "image_url": "",
            "additional_metadata": "",
            "additional_mimetype": {
                "name": "text/vnd.abi.plot+csv",
            },
            "datacite": {
                "isDerivedFrom": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "isDescribedBy": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "isSourceOf": {
                    "path": [""],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "supplemental_json_metadata": {
                    "description": "",
                },
            },
            "dataset": {
                "identifier": "dummy id",
                "path": "dummy_filepath/dummy_filename.csv",
            },
            "file_type": {
                "name": ".csv",
            },
            "identifier": "dummy id",
            "name": "dummy_filename.csv",
        },
    ]
    assert detail["scaffoldViews"] == []
    assert detail["scaffolds"] == [
        {
            "image_url": "",
            "additional_metadata": "",
            "additional_mimetype": {
                "name": "application/x.vnd.abi.scaffold.meta+json",
            },
            "datacite": {
                "isDerivedFrom": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "isDescribedBy": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "isSourceOf": {
                    "path": [
                        "dummy_filepath/dummy_view.json",
                    ],
                    "relative": {
                        "path": [
                            "dummy_view.json",
                        ],
                    },
                },
                "supplemental_json_metadata": {
                    "description": "",
                },
            },
            "dataset": {
                "identifier": "dummy id",
                "path": "dummy_filepath/dummy_filename.json",
            },
            "file_type": {
                "name": ".json",
            },
            "identifier": "dummy id",
            "name": "dummy_filename.json",
        },
    ]
    assert detail["thumbnails"] == []
    assert detail["mris"] == [
        {
            "image_url": "",
            "additional_metadata": "",
            "additional_mimetype": {
                "name": "",
            },
            "datacite": {
                "isDerivedFrom": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "isDescribedBy": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "isSourceOf": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "supplemental_json_metadata": {
                    "description": "",
                },
            },
            "dataset": {
                "identifier": "dummy id",
                "path": "dummy_filepath/sub-dummy/sam-dummy/dummy_filename.nrrd",
            },
            "file_type": {
                "name": ".nrrd",
            },
            "identifier": "dummy id",
            "name": "dummy_filename.nrrd",
        },
        {
            "image_url": "",
            "additional_metadata": "",
            "additional_mimetype": {
                "name": "",
            },
            "datacite": {
                "isDerivedFrom": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "isDescribedBy": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "isSourceOf": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "supplemental_json_metadata": {
                    "description": "",
                },
            },
            "dataset": {
                "identifier": "dummy id",
                "path": "dummy_filepath/sub-dummy/sam-dummy/dummy_filename_extra.nrrd",
            },
            "file_type": {
                "name": ".nrrd",
            },
            "identifier": "dummy id",
            "name": "dummy_filename_extra.nrrd",
        },
    ]
    assert detail["dicomImages"] == [
        {
            "image_url": "",
            "additional_metadata": "",
            "additional_mimetype": {
                "name": "application/dicom",
            },
            "datacite": {
                "isDerivedFrom": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "isDescribedBy": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "isSourceOf": {
                    "path": [
                        "",
                    ],
                    "relative": {
                        "path": [
                            "",
                        ],
                    },
                },
                "supplemental_json_metadata": {
                    "description": "",
                },
            },
            "dataset": {
                "identifier": "dummy id",
                "path": "dummy_filepath/sub-dummy/sam-dummy/1-01.dcm",
            },
            "file_type": {
                "name": ".dcm",
            },
            "identifier": "dummy id",
            "name": "1-01.dcm",
        },
    ]
    assert output["facet"] == {
        "Data type": [
            "Scaffold",
            "Plot",
            "Dicom",
        ],
        "Age category": [
            "Dummy age category",
        ],
        "Sex": [
            "Male",
        ],
        "Species": [
            "Dummy species",
        ],
        "Anatomical structure": [
            "Dummy organ",
        ],
    }


def test_process_data_output_mode_detail_private(
    qf_class, dummy_filter_cache_private, dummy_query_data
):
    mode = "detail"
    qf_class.set_query_mode(mode)
    qf_class.set_private_filter(dummy_filter_cache_private)
    output = qf_class.process_data_output(dummy_query_data)
    assert output["facet"] == {
        "Data type": [
            "Scaffold",
            "Plot",
            "Dicom",
        ],
        "Age category": [
            "Dummy age category",
        ],
        "Sex": [
            "Male",
        ],
        "Species": [
            "Dummy species",
            "Dummy private species",
        ],
        "Anatomical structure": [
            "Dummy organ",
        ],
    }


def test_process_data_output_mode_facet(qf_class, dummy_query_data):
    mode = "facet"
    qf_class.set_query_mode(mode)
    qf_class.set_private_filter({})
    output = qf_class.process_data_output(dummy_query_data)
    assert output[mode] == [
        {
            "facet": "Scaffold",
            "term": "Data type",
            "facetPropPath": "manifest_filter>additional_types",
        },
        {
            "facet": "Plot",
            "term": "Data type",
            "facetPropPath": "manifest_filter>additional_types",
        },
        {
            "facet": "Dicom",
            "term": "Data type",
            "facetPropPath": "manifest_filter>additional_types",
        },
        {
            "facet": "Dummy age category",
            "term": "Age category",
            "facetPropPath": "case_filter>age_category",
        },
        {
            "facet": "Male",
            "term": "Sex",
            "facetPropPath": "case_filter>sex",
        },
        {
            "facet": "Dummy species",
            "term": "Species",
            "facetPropPath": "case_filter>species",
        },
        {
            "facet": "Dummy organ",
            "term": "Anatomical structure",
            "facetPropPath": "dataset_description_filter>study_organ_system",
        },
    ]


def test_process_data_output_mode_facet_private(
    qf_class, dummy_filter_cache_private, dummy_query_data
):
    mode = "facet"
    qf_class.set_query_mode(mode)
    qf_class.set_private_filter(dummy_filter_cache_private)
    output = qf_class.process_data_output(dummy_query_data)
    assert output[mode] == [
        {
            "facet": "Scaffold",
            "term": "Data type",
            "facetPropPath": "manifest_filter>additional_types",
        },
        {
            "facet": "Plot",
            "term": "Data type",
            "facetPropPath": "manifest_filter>additional_types",
        },
        {
            "facet": "Dicom",
            "term": "Data type",
            "facetPropPath": "manifest_filter>additional_types",
        },
        {
            "facet": "Dummy age category",
            "term": "Age category",
            "facetPropPath": "case_filter>age_category",
        },
        {
            "facet": "Male",
            "term": "Sex",
            "facetPropPath": "case_filter>sex",
        },
        {
            "facet": "Dummy species",
            "term": "Species",
            "facetPropPath": "case_filter>species",
        },
        {
            "facet": "Dummy private species",
            "term": "Species",
            "facetPropPath": "case_filter>species",
        },
        {
            "facet": "Dummy organ",
            "term": "Anatomical structure",
            "facetPropPath": "dataset_description_filter>study_organ_system",
        },
    ]


def test_process_data_output_mode_mri(qf_class, dummy_query_data):
    mode = "mri"
    qf_class.set_query_mode(mode)
    qf_class.set_private_filter({})
    output = qf_class.process_data_output(dummy_query_data)
    assert output[mode] == {
        "dummy_filename": [
            "dummy_filepath/sub-dummy/sam-dummy/dummy_filename_c0.nrrd",
            "dummy_filepath/sub-dummy/sam-dummy/dummy_filename_c1.nrrd",
            "dummy_filepath/sub-dummy/sam-dummy/dummy_filename_c2.nrrd",
            "dummy_filepath/sub-dummy/sam-dummy/dummy_filename_c3.nrrd",
            "dummy_filepath/sub-dummy/sam-dummy/dummy_filename_c4.nrrd",
        ],
        "dummy_filename_extra": [
            "dummy_filepath/sub-dummy/sam-dummy/dummy_filename_extra_c0.nrrd",
        ],
    }
