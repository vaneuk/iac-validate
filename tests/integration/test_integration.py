# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Daniel Schmidt <danischm@cisco.com>

import os

from click.testing import CliRunner
import pytest

import iac_validate.cli.main

pytestmark = pytest.mark.integration


def test_validate():
    runner = CliRunner()
    input_path = "tests/integration/fixtures/data/"
    schema_path = "tests/integration/fixtures/schema/schema.yaml"
    rules_path = "tests/integration/fixtures/rules/"
    result = runner.invoke(
        iac_validate.cli.main.main,
        [
            "-s",
            schema_path,
            "-r",
            rules_path,
            input_path,
        ],
    )
    assert result.exit_code == 0


def test_validate_vault():
    runner = CliRunner()
    input_path = "tests/integration/fixtures/data_vault/"
    schema_path = "tests/integration/fixtures/schema/schema.yaml"
    os.environ["ANSIBLE_VAULT_ID"] = "dev"
    os.environ["ANSIBLE_VAULT_PASSWORD"] = "Password123"
    result = runner.invoke(
        iac_validate.cli.main.main,
        [
            "-s",
            schema_path,
            input_path,
        ],
    )
    assert result.exit_code == 0


def test_validate_additional_data():
    runner = CliRunner()
    input_path = "tests/integration/fixtures/data/"
    input_path_2 = "tests/integration/fixtures/additional_data/"
    schema_path = "tests/integration/fixtures/additional_data_schema/schema.yaml"
    schema_path_fail = "tests/integration/fixtures/schema/schema.yaml"
    rules_path = "tests/integration/fixtures/rules/"
    result = runner.invoke(
        iac_validate.cli.main.main,
        [
            "-s",
            schema_path,
            "-r",
            rules_path,
            input_path,
            input_path_2,
        ],
    )
    assert result.exit_code == 0
    result = runner.invoke(
        iac_validate.cli.main.main,
        [
            "-s",
            schema_path_fail,
            "-r",
            rules_path,
            input_path,
            input_path_2,
        ],
    )
    assert result.exit_code == 1


def test_validate_syntax():
    runner = CliRunner()
    input_path = "tests/integration/fixtures/data_syntax_error/"
    schema_path = "tests/integration/fixtures/schema/schema.yaml"
    result = runner.invoke(
        iac_validate.cli.main.main,
        [
            "-s",
            schema_path,
            input_path,
        ],
    )
    assert result.exit_code == 1


def test_validate_semantics():
    runner = CliRunner()
    input_path = "tests/integration/fixtures/data_semantic_error/"
    rules_path = "tests/integration/fixtures/rules/"
    result = runner.invoke(
        iac_validate.cli.main.main,
        [
            "-r",
            rules_path,
            input_path,
        ],
    )
    assert result.exit_code == 1
