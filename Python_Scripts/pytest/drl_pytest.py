import pytest
import os
import pandas as pd
from drl_test_suite import config_reader
from drl_test_suite import merge_frames

dummi_config = "test_config.txt"


@pytest.mark.parametrize("dummi_config,expected", [(dummi_config,["test_one.xlsx"])])
def test_config_reading(dummi_config, expected):
    file_list = config_reader(dummi_config)
    assert file_list == expected

@pytest.mark.parametrize("dummi_config,expected", [(None,ValueError),
                            ((1),ValueError), ([1,3,4],ValueError), ({"a":"b"},ValueError), (("tuplestring","tuplestring"),ValueError)])
def test_config_reading_types(dummi_config, expected):
    file_list = config_reader(dummi_config)
    assert file_list == expected

@pytest.mark.parametrize("dummi_list,expected",[(None, ValueError), (["string",1], ValueError)])
def test_frame_merging_datatype(dummi_list, expected):
    merged_frame = merge_frames(dummi_list)
    assert merged_frame == expected
