# -*- coding: utf-8 -*-
import json

import numpy as np
import pytest

import csdmpy as cp


def test_internal_new():
    data = cp.new()
    test_array = np.arange(20).reshape(2, 10)
    dim = {
        "type": "internal",
        "numeric_type": "float32",
        "quantity_type": "vector_2",
        "components": test_array,
    }
    data.add_dependent_variable(dim)

    # check type
    assert data.dependent_variables[0].type == "internal"
    data.dependent_variables[0].type = "external"
    assert data.dependent_variables[0].type == "external"
    error = "is not a valid value. The allowed values are"
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].type = "celestial"

    # check components
    assert np.all(data.dependent_variables[0].components == test_array)
    assert data.dependent_variables[0].numeric_type == "float32"

    # assign and check components
    data.dependent_variables[0].components = test_array.astype("int32") + 100

    assert np.all(data.dependent_variables[0].components == test_array + 100.0)
    assert data.dependent_variables[0].numeric_type == "int32"

    # check name
    assert data.dependent_variables[0].name == ""
    data.dependent_variables[0].name = "happy days"
    assert data.dependent_variables[0].name == "happy days"

    # check unit
    assert data.dependent_variables[0].unit == ""
    error = r"`unit` attribute cannot be modified"
    with pytest.raises(AttributeError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].unit = "m/s"

    # check component_url
    error = r"DependentVariable' object has no attribute 'component_url"
    with pytest.raises(AttributeError, match=error):
        data.dependent_variables[0].component_url

    # component names
    assert data.dependent_variables[0].component_labels == ["", ""]
    data.dependent_variables[0].component_labels = [":)"]
    assert data.dependent_variables[0].component_labels == [":)", ""]

    data.dependent_variables[0].component_labels = []
    assert data.dependent_variables[0].component_labels == ["", ""]

    data.dependent_variables[0].component_labels = ["1", "2", "3"]
    assert data.dependent_variables[0].component_labels == ["1", "2"]

    data.dependent_variables[0].component_labels[0] = ":("
    assert data.dependent_variables[0].component_labels == [":(", "2"]

    # quantity type
    assert data.dependent_variables[0].quantity_type == "vector_2"

    # Need to fix this
    data.dependent_variables[0].quantity_type = "vector_2"

    # encoding
    assert data.dependent_variables[0].encoding == "base64"
    data.dependent_variables[0].encoding = "none"
    assert data.dependent_variables[0].encoding == "none"
    error = "not a valid `encoding` enumeration literal. The allowed values are"
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].encoding = "base16"
    data.dependent_variables[0].encoding = "raw"
    assert data.dependent_variables[0].encoding == "raw"

    # numeric_type
    assert data.dependent_variables[0].numeric_type == "int32"
    data.dependent_variables[0].numeric_type = "complex64"
    assert data.dependent_variables[0].numeric_type == "complex64"
    assert np.all(data.dependent_variables[0].components == test_array + 100.0)
    error = "not a valid `numeric_type` enumeration literal. The allowed values are"
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].numeric_type = "complex32"

    # quantity_name
    assert data.dependent_variables[0].quantity_name == "dimensionless"
    error = "`quantity_name` attribute cannot be modified."
    with pytest.raises(NotImplementedError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].quantity_name = "time"

    # description
    assert data.dependent_variables[0].description == ""
    data.dependent_variables[0].description = "This is a test"
    assert data.dependent_variables[0].description == "This is a test"
    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].description = {}

    # application
    assert data.dependent_variables[0].application == {}
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].application = ""

    dict1 = {
        "csdm": {
            "version": "1.0",
            "dimensions": [],
            "dependent_variables": [
                {
                    "type": "internal",
                    "description": "This is a test",
                    "name": "happy days",
                    "numeric_type": "complex64",
                    "quantity_type": "vector_2",
                    "component_labels": [":(", "2"],
                    "components": [
                        ["(100+0j), (101+0j), ..., " "(108+0j), (109+0j)"],
                        ["(110+0j), (111+0j), ..., (118+0j), (119+0j)"],
                    ],
                }
            ],
        }
    }

    assert data.data_structure == str(
        json.dumps(dict1, ensure_ascii=False, sort_keys=False, indent=2)
    )


def test_external_new():
    data = cp.new()
    dim = {
        "type": "external",
        "components_url": (
            "https://www.grandinetti.org/resources/CSDM/cinnamon_raw_cinnamon stick.dat"
        ),
        "component_labels": ["monotonic"],
        "name": "Headspace from cinnamon stick",
        "numeric_type": "float32",
        "quantity_type": "scalar",
    }
    data.add_dependent_variable(dim)

    # check type
    assert data.dependent_variables[0].type == "internal"
    data.dependent_variables[0].type = "external"
    assert data.dependent_variables[0].type == "external"

    # check components
    assert data.dependent_variables[0].numeric_type == "float32"

    # assign and check components
    data.dependent_variables[0].numeric_type = "int32"
    assert data.dependent_variables[0].numeric_type == "int32"
    assert data.dependent_variables[0].components.dtype == "int32"

    # check name
    assert data.dependent_variables[0].name == "Headspace from cinnamon stick"

    # check unit
    assert data.dependent_variables[0].unit == ""

    # check component_url
    assert data.dependent_variables[0].components_url == (
        "https://www.grandinetti.org/resources/CSDM/cinnamon_raw_cinnamon stick.dat"
    )

    # component names
    assert data.dependent_variables[0].component_labels == ["monotonic"]

    # quantity type
    assert data.dependent_variables[0].quantity_type == "scalar"

    # encoding
    assert data.dependent_variables[0].encoding == "base64"
    data.dependent_variables[0].encoding = "raw"
    assert data.dependent_variables[0].encoding == "raw"

    # description
    assert data.dependent_variables[0].description == ""
    data.dependent_variables[0].description = "This is also a test"
    assert data.dependent_variables[0].description == "This is also a test"

    # application
    assert data.dependent_variables[0].application == {}

    dict1 = {
        "csdm": {
            "version": "1.0",
            "dimensions": [],
            "dependent_variables": [
                {
                    "type": "internal",
                    "description": "This is also a test",
                    "name": "Headspace from cinnamon stick",
                    "numeric_type": "int32",
                    "quantity_type": "scalar",
                    "component_labels": ["monotonic"],
                    "components": [["48453, 48444, ..., 48040, 48040"]],
                }
            ],
        }
    }

    assert data.data_structure == json.dumps(
        dict1, ensure_ascii=False, sort_keys=False, indent=2
    )


def test_missing_type():
    data = cp.new()
    dim = {
        "numeric_type": "float32",
        "quantity_type": "scalar",
        "components": [np.arange(10)],
    }
    error = "Missing a required `type` key from the dependent variable."
    with pytest.raises(KeyError, match=".*{0}.*".format(error)):
        data.add_dependent_variable(dim)


def test_wrong_type():
    data = cp.new()
    dim = {
        "type": "",
        "numeric_type": "float32",
        "quantity_type": "scalar",
        "components": [np.arange(10)],
    }
    error = "is an invalid DependentVariable 'type'"
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        data.add_dependent_variable(dim)


def test_missing_component():
    data = cp.new()
    dim = {"type": "internal", "numeric_type": "float32", "quantity_type": "scalar"}
    error = "Missing a required `components` key"
    with pytest.raises(KeyError, match=".*{0}.*".format(error)):
        data.add_dependent_variable(dim)


def test_missing_component_url():
    data = cp.new()
    dim = {"type": "external", "numeric_type": "float32", "quantity_type": "scalar"}
    error = "Missing a required `components_url` key"
    with pytest.raises(KeyError, match=".*{0}.*".format(error)):
        data.add_dependent_variable(dim)