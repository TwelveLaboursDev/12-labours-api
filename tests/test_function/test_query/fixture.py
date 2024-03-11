import pytest

from app.function.filter.filter_editor import FilterEditor
from app.function.query.query_formatter import QueryFormatter


@pytest.fixture
def qf_class(dummy_filter_cache):
    fe = FilterEditor()
    fe.update_filter_cache(dummy_filter_cache)
    return QueryFormatter(fe)


@pytest.fixture
def dummy_filter_cache():
    return {
        "MAPPED_ADDITIONAL_TYPES": {
            "title": "data type",
            "node": "manifest_filter",
            "field": "additional_types",
            "facets": {
                "Dicom": "application/dicom",
                "Plot": [
                    "text/vnd.abi.plot+tab-separated-values",
                    "text/vnd.abi.plot+csv",
                ],
                "Scaffold": "application/x.vnd.abi.scaffold.meta+json",
            },
        },
        "MAPPED_AGE_CATEGORY": {
            "title": "age category",
            "node": "case_filter",
            "field": "age_category",
            "facets": {
                "Dummy age category": "dummy age category",
            },
        },
        "MAPPED_SEX": {
            "title": "sex",
            "node": "case_filter",
            "field": "sex",
            "facets": {
                "Female": "Female",
                "Male": "Male",
            },
        },
        "MAPPED_SPECIES": {
            "title": "species",
            "node": "case_filter",
            "field": "species",
            "facets": {
                "Dummy species": "dummy species",
            },
        },
        "MAPPED_STUDY_ORGAN_SYSTEM": {
            "title": "anatomical structure",
            "node": "dataset_description_filter",
            "field": "study_organ_system",
            "facets": {
                "Dummy organ": "dummy organ",
            },
        },
    }


@pytest.fixture
def dummy_filter_cache_private():
    return {
        "MAPPED_SPECIES": {
            "title": "species",
            "node": "case_filter",
            "field": "species",
            "facets": {
                "Dummy species": "dummy species",
                "Dummy private species": "dummy private species",
            },
        },
    }


@pytest.fixture
def dummy_query_data():
    return {
        "cases": [
            {
                "age": "dummy age",
                "age_category": "dummy age category",
                "also_in_dataset": "NA",
                "id": "dummy id",
                "member_of": "NA",
                "pool_id": "NA",
                "rrid_for_strain": "dummy rrid",
                "sex": "Male",
                "species": "dummy species",
                "strain": "dummy strain",
                "subject_experimental_group": "dummy experimental group",
                "subject_id": "dummy subject id",
                "submitter_id": "dummy submitter",
                "type": "case",
            },
            {
                "age": "dummy age",
                "age_category": "dummy age category",
                "also_in_dataset": "NA",
                "id": "dummy id",
                "member_of": "NA",
                "pool_id": "NA",
                "rrid_for_strain": "dummy rrid",
                "sex": "Male",
                "species": "dummy private species",
                "strain": "dummy strain",
                "subject_experimental_group": "dummy experimental group",
                "subject_id": "dummy subject id",
                "submitter_id": "dummy submitter",
                "type": "case",
            },
        ],
        "dataset_descriptions": [
            {
                "contributor_affiliation": [
                    "dummy affiliation",
                ],
                "contributor_name": [
                    "dummy name",
                ],
                "contributor_orcid": [
                    "dummy orcid 1",
                    "https://orcid.org/dummy orcid 2",
                ],
                "contributor_role": [
                    "dummy role",
                ],
                "dataset_type": [
                    "dummy dataset type",
                ],
                "id": "dummy id",
                "identifier": [
                    "dummy identifier",
                ],
                "identifier_description": [
                    "dummy description",
                ],
                "identifier_type": [
                    "dummy identifier type",
                ],
                "keywords": [
                    "dummy keyword",
                ],
                "metadata_version": [
                    "dummy version",
                ],
                "number_of_samples": [
                    "12",
                ],
                "number_of_subjects": [
                    "12",
                ],
                "relation_type": [
                    "dummy relation type",
                ],
                "study_approach": [
                    "dummy approach",
                ],
                "study_data_collection": [
                    "dummy data collection",
                ],
                "study_organ_system": [
                    "dummy organ",
                ],
                "study_primary_conclusion": [
                    "dummy conclusion",
                ],
                "study_purpose": [
                    "dummy purpose",
                ],
                "study_technique": [
                    "dummy technique",
                ],
                "submitter_id": "dummy submitter",
                "subtitle": [
                    "dummy subtitle",
                ],
                "title": [
                    "dummy title",
                ],
                "type": "dataset_description",
            }
        ],
        "dicomImages": [
            {
                "additional_metadata": None,
                "additional_types": "application/dicom",
                "description": "NA",
                "file_type": ".dcm",
                "filename": "dummy_filepath/sub-dummy/sam-dummy/1-01.dcm",
                "id": "dummy id",
                "is_derived_from": None,
                "is_described_by": None,
                "is_source_of": None,
                "submitter_id": "dummy submitter",
                "supplemental_json_metadata": None,
                "timestamp": "dummy timestamp",
                "type": "manifest",
            },
            {
                "additional_metadata": None,
                "additional_types": None,
                "description": "NA",
                "file_type": ".dcm",
                "filename": "dummy_filepath/sub-dummy/sam-dummy/1-02.dcm",
                "id": "dummy id",
                "is_derived_from": None,
                "is_described_by": None,
                "is_source_of": None,
                "submitter_id": "dummy submitter",
                "supplemental_json_metadata": None,
                "timestamp": "dummy timestamp",
                "type": "manifest",
            },
            {
                "additional_metadata": None,
                "additional_types": None,
                "description": "NA",
                "file_type": ".dcm",
                "filename": "dummy_filepath/sub-dummy/sam-dummy/1-03.dcm",
                "id": "dummy id",
                "is_derived_from": None,
                "is_described_by": None,
                "is_source_of": None,
                "submitter_id": "dummy submitter",
                "supplemental_json_metadata": None,
                "timestamp": "dummy timestamp",
                "type": "manifest",
            },
        ],
        "id": "dummy id",
        "mris": [
            {
                "additional_metadata": None,
                "additional_types": None,
                "description": "NA",
                "file_type": ".nrrd",
                "filename": "dummy_filepath/sub-dummy/sam-dummy/dummy_filename_c0.nrrd",
                "id": "dummy id",
                "is_derived_from": None,
                "is_described_by": None,
                "is_source_of": None,
                "submitter_id": "dummy submitter",
                "supplemental_json_metadata": None,
                "timestamp": "dummy timestamp",
                "type": "manifest",
            },
            {
                "additional_metadata": None,
                "additional_types": None,
                "description": "NA",
                "file_type": ".nrrd",
                "filename": "dummy_filepath/sub-dummy/sam-dummy/dummy_filename_c1.nrrd",
                "id": "dummy id",
                "is_derived_from": None,
                "is_described_by": None,
                "is_source_of": None,
                "submitter_id": "dummy submitter",
                "supplemental_json_metadata": None,
                "timestamp": "dummy timestamp",
                "type": "manifest",
            },
            {
                "additional_metadata": None,
                "additional_types": None,
                "description": "NA",
                "file_type": ".nrrd",
                "filename": "dummy_filepath/sub-dummy/sam-dummy/dummy_filename_c2.nrrd",
                "id": "dummy id",
                "is_derived_from": None,
                "is_described_by": None,
                "is_source_of": None,
                "submitter_id": "dummy submitter",
                "supplemental_json_metadata": None,
                "timestamp": "dummy timestamp",
                "type": "manifest",
            },
            {
                "additional_metadata": None,
                "additional_types": None,
                "description": "NA",
                "file_type": ".nrrd",
                "filename": "dummy_filepath/sub-dummy/sam-dummy/dummy_filename_c3.nrrd",
                "id": "dummy id",
                "is_derived_from": None,
                "is_described_by": None,
                "is_source_of": None,
                "submitter_id": "dummy submitter",
                "supplemental_json_metadata": None,
                "timestamp": "dummy timestamp",
                "type": "manifest",
            },
            {
                "additional_metadata": None,
                "additional_types": None,
                "description": "NA",
                "file_type": ".nrrd",
                "filename": "dummy_filepath/sub-dummy/sam-dummy/dummy_filename_c4.nrrd",
                "id": "dummy id",
                "is_derived_from": None,
                "is_described_by": None,
                "is_source_of": None,
                "submitter_id": "dummy submitter",
                "supplemental_json_metadata": None,
                "timestamp": "dummy timestamp",
                "type": "manifest",
            },
            {
                "additional_metadata": None,
                "additional_types": None,
                "description": "NA",
                "file_type": ".nrrd",
                "filename": "dummy_filepath/sub-dummy/sam-dummy/dummy_filename_extra_c0.nrrd",
                "id": "dummy id",
                "is_derived_from": None,
                "is_described_by": None,
                "is_source_of": None,
                "submitter_id": "dummy submitter",
                "supplemental_json_metadata": None,
                "timestamp": "dummy timestamp",
                "type": "manifest",
            },
        ],
        "plots": [
            {
                "additional_metadata": None,
                "additional_types": "text/vnd.abi.plot+tab-separated-values",
                "description": "dummy description",
                "file_type": ".csv",
                "filename": "dummy_filepath/dummy_filename.csv",
                "id": "dummy id",
                "is_derived_from": None,
                "is_described_by": None,
                "is_source_of": None,
                "submitter_id": "dummy submitter",
                "supplemental_json_metadata": None,
                "timestamp": "dummy timestamp",
                "type": "manifest",
            },
            {
                "additional_metadata": None,
                "additional_types": "text/vnd.abi.plot+csv",
                "description": "dummy description",
                "file_type": ".csv",
                "filename": "dummy_filepath/dummy_filename.csv",
                "id": "dummy id",
                "is_derived_from": None,
                "is_described_by": None,
                "is_source_of": None,
                "submitter_id": "dummy submitter",
                "supplemental_json_metadata": None,
                "timestamp": "dummy timestamp",
                "type": "manifest",
            },
        ],
        "scaffoldViews": [],
        "scaffolds": [
            {
                "additional_metadata": None,
                "additional_types": "application/x.vnd.abi.scaffold.meta+json",
                "description": "NA",
                "file_type": ".json",
                "filename": "dummy_filepath/dummy_filename.json",
                "id": "dummy id",
                "is_derived_from": None,
                "is_described_by": None,
                "is_source_of": "dummy_view.json",
                "submitter_id": "dummy submitter",
                "supplemental_json_metadata": None,
                "timestamp": "dummy timestamp",
                "type": "manifest",
            }
        ],
        "submitter_id": "dummy submitter",
        "thumbnails": [],
        "created_datetime": "dummy datetime",
        "updated_datetime": "dummy datetime",
    }
