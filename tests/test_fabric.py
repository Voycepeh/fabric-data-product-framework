import pytest

from fabric_data_product_framework.fabric_io import (
    build_table_identifier,
    read_table,
    write_table,
)


def test_build_table_identifier_supports_table_only():
    assert build_table_identifier(table="orders") == "orders"


def test_build_table_identifier_supports_schema_table():
    assert build_table_identifier(schema="source", table="orders") == "source.orders"


def test_build_table_identifier_supports_lakehouse_schema_table():
    assert (
        build_table_identifier(lakehouse="lh_dev", schema="source", table="orders")
        == "lh_dev.source.orders"
    )


def test_read_table_calls_injected_reader():
    calls = []

    def fake_reader(identifier):
        calls.append(identifier)
        return {"identifier": identifier}

    result = read_table("source.orders", reader=fake_reader)
    assert result == {"identifier": "source.orders"}
    assert calls == ["source.orders"]


def test_write_table_calls_injected_writer():
    calls = []

    def fake_writer(df, identifier, mode="append", **options):
        calls.append((df, identifier, mode, options))
        return "ok"

    result = write_table(
        df=[{"id": 1}],
        table_identifier="product.orders",
        writer=fake_writer,
        mode="overwrite",
        merge_schema=True,
    )
    assert result == "ok"
    assert calls == [([{"id": 1}], "product.orders", "overwrite", {"merge_schema": True})]


def test_write_table_rejects_invalid_write_mode():
    with pytest.raises(ValueError):
        write_table(df=[], table_identifier="product.orders", writer=lambda *args, **kwargs: None, mode="upsert")


def test_reader_and_writer_raise_not_implemented_without_injection():
    with pytest.raises(NotImplementedError):
        read_table("source.orders")

    with pytest.raises(NotImplementedError):
        write_table(df=[], table_identifier="product.orders")
