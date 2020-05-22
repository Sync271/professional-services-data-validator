# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from data_validation import data_validation, consts


BQ_CONN = {"source_type": "BigQuery", "project_id": os.environ["PROJECT_ID"]}
CONFIG_COUNT_VALID = {
    # BigQuery Specific Connection Config
    "source_conn": BQ_CONN,
    "target_conn": BQ_CONN,
    # Validation Type
    "Type": "Column",
    # Configuration Required Depending on Validator Type
    "schema_name": "bigquery-public-data.new_york_citibike",
    "table_name": "citibike_trips",
    consts.PARTITION_COLUMN: "starttime",
}

CONFIG_GROUPED_COUNT_VALID = {
    # BigQuery Specific Connection Config
    "source_conn": BQ_CONN,
    "target_conn": BQ_CONN,
    # Validation Type
    "Type": "GroupedColumn",
    # Configuration Required Depending on Validator Type
    "schema_name": "bigquery-public-data.new_york_citibike",
    "table_name": "citibike_trips",
    consts.PARTITION_COLUMN: "starttime",
}


def test_count_validator():
    validator = data_validation.DataValidation(CONFIG_COUNT_VALID, verbose=True)
    df = validator.execute()

    assert df["count_inp"][0] > 0
    assert df["count_inp"][0] == df["count_out"][0]


def test_partitioned_count_validator():
    validator = data_validation.DataValidation(CONFIG_GROUPED_COUNT_VALID, verbose=True)
    df = validator.execute()
    rows = list(df.iterrows())

    # Check that all partitions are unique.
    partitions = frozenset(df["partition_key"])
    assert len(rows) == len(partitions)
    assert len(rows) > 1

    for _, row in rows:
        assert row["count_inp"] > 0
        assert row["count_inp"] == row["count_out"]
