import pytest
import pandas as pd
from reasonp import main as rp
import ipdb


@pytest.fixture
def sample_df():
    data = [
        ("A", "P1", "2021-03-02", 1),
        ("B", "P1", "2021-03-02", 1),
        ("A", "P2", "2021-03-02", 1),
        ("B", "P2", "2021-03-02", 1),
        ("A", "P1", "2021-03-03", 3),
        ("B", "P1", "2021-03-03", 4),
        ("A", "P2", "2021-03-03", 1),
        ("B", "P2", "2021-03-03", 2),
        ("C", "P2", "2021-03-03", 1),
    ]
    df = pd.DataFrame(data, columns=["source", "platform", "date", "orders"])
    return df


# @pytest.mark.skip
def test_find_reason(sample_df):
    rdf = rp.find_reason(
        sample_df,
        compare_column="date",
        compare_values=["2021-03-03", "2021-03-02"],
        compare_metric=("orders", "sum"),
    )
    assert rdf.shape[0] > 0

    assert list(rdf.columns) == [
        "search_column",
        "target_column_value",
        "compare_column_value",
        "target_metric_value",
        "compare_metric_value",
        "metric_change",
        "reason_coef",
    ]
    assert rdf["target_column_value"].values[0] == "P1"
    assert rdf["search_column"].values[0] == "platform"
    assert (
        pd.isna(rdf[rdf["target_column_value"] == "C"]["metric_change"].values[0])
        == False
    )
    print("\n")
    print(rdf.to_markdown(index=False))


def test_find_sub_reason_data(sample_df):
    df = rp.get_sub_reason_data(
        sample_df,
        search_column="source",
        compare_column="date",
        compare_values=["2021-03-03", "2021-03-02"],
        compare_metric=("orders", "sum"),
    )
    assert df.shape[0] > 0
    for column in [
        "target_column_value",
        "target_metric_value",
        "compare_column_value",
        "compare_metric_value",
        "search_column",
        "metric_change",
    ]:
        assert column in df.columns
    # ipdb.set_trace()
    assert df[df["target_column_value"] == "A"]["metric_change"].values[0] == 2
    assert df[df["target_column_value"] == "B"]["metric_change"].values[0] == 4


def test_metric_format(sample_df):
    rp.find_reason(
        sample_df,
        compare_column="date",
        compare_values=["2021-03-03", "2021-03-02"],
        compare_metric=("orders", "sum"),
    )
    rp.find_reason(
        sample_df,
        compare_column="date",
        compare_values=["2021-03-03", "2021-03-02"],
        compare_metric={"orders": "count"},
    )
    # 如果数值则求和，如果是类别则计数
    rp.find_reason(
        sample_df,
        compare_column="date",
        compare_values=["2021-03-03", "2021-03-02"],
        compare_metric="orders",
    )
    rp.find_reason(
        sample_df,
        compare_column="date",
        compare_values=["2021-03-03", "2021-03-02"],
    )
    # rp.find_reason(
    #     sample_df,
    #     compare_column="date",
    #     compare_values=["2021-03-02", "2021-03-03"],
    #     ratio_compare_metric=(("orders", "sum"), ("orders", "count")),
    # )


@pytest.mark.skip
def test_find_insight(sample_df):
    insights = rp.find_insight(sample_df, compare_metric=("orders", "count"))
    for insight in insights:
        print(insight)
