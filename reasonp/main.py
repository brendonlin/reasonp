import pandas as pd


def find_reason(
    df: pd.DataFrame,
    compare_column: str,
    compare_values: tuple,
    compare_metric: tuple = None,
    weight_metric: tuple = None,
    limit=20,
) -> pd.DataFrame:
    """
    find reason for diffrence
    """
    search_columns = [col for col in df.columns if df.dtypes[col].name in ["object"]]
    if compare_column not in search_columns:
        search_columns.append(compare_column)
    reason_data_map = {}
    print("Search :" + ",".join(search_columns))
    for search_column in search_columns:
        reason_data_map[search_column] = get_sub_reason_data(
            df,
            search_column,
            compare_column,
            compare_values,
            compare_metric,
        )

    if weight_metric is not None:
        weight_data = get_sub_reason_data(
            df,
            search_column=compare_column,
            compare_column=compare_column,
            compare_values=compare_values,
            compare_metric=weight_metric,
        )
        weight = weight_data[["target_metric_value", "compare_metric_value"]].values
        if weight.shape[0] > 1:
            weight = weight.sum(0)
        target_weight, compare_weight = weight

        for search_column in reason_data_map:
            sub_reason_data = reason_data_map.get(search_column)
            sub_reason_data["target_metric_value"] = (
                sub_reason_data["target_metric_value"] / target_weight
            )
            sub_reason_data["compare_metric_value"] = (
                sub_reason_data["compare_metric_value"] / compare_weight
            )
            sub_reason_data["metric_change"] = (
                sub_reason_data["target_metric_value"]
                - sub_reason_data["compare_metric_value"]
            )

    total_diffrence_data = reason_data_map.pop(compare_column)
    total_diffrence = (
        total_diffrence_data["target_metric_value"].sum()
        - total_diffrence_data["compare_metric_value"].sum()
    )
    reason_df = pd.concat(reason_data_map.values())
    reason_df["reason_coef"] = reason_df["metric_change"] / total_diffrence
    ordered_columns = [
        "search_column",
        "target_column_value",
        "compare_column_value",
        "target_metric_value",
        "compare_metric_value",
        "metric_change",
        "reason_coef",
    ]
    return (
        reason_df[ordered_columns]
        .sort_values("reason_coef", ascending=False)
        .head(limit)
    )


def get_sub_reason_data(
    df: pd.DataFrame,
    search_column: str,
    compare_column: str,
    compare_values: tuple,
    compare_metric: tuple = None,
):
    """
    find reason from single search column
    """
    assert len(compare_values) == 2, "Length of compare_values should be 2. "
    target_column_value, compare_column_value = compare_values
    target_df = df[df[compare_column] == target_column_value].groupby(search_column)
    compare_df = df[df[compare_column] == compare_column_value].groupby(search_column)

    if isinstance(compare_metric, tuple):
        target_df = target_df.agg(target_metric_value=compare_metric)
        compare_df = compare_df.agg(compare_metric_value=compare_metric)
    elif isinstance(compare_metric, dict):

        compare_metric_name = list(compare_metric.keys())[0]

        target_df = target_df.agg(compare_metric).rename(
            {compare_metric_name: "target_metric_value"}, axis=1
        )
        compare_df = compare_df.agg(compare_metric).rename(
            {compare_metric_name: "compare_metric_value"}, axis=1
        )
    elif isinstance(compare_metric, dict):
        target_df = target_df.agg(target_metric_value=(compare_metric, "count"))
        compare_df = compare_df.agg(compare_metric_value=(compare_metric, "count"))
    else:
        target_df = target_df.agg(target_metric_value=(compare_column, "count"))
        compare_df = compare_df.agg(compare_metric_value=(compare_column, "count"))

    target_df.index.name = "target_column_value"
    compare_df.index.name = "compare_column_value"

    merge_df = pd.merge(
        target_df.reset_index(),
        compare_df.reset_index(),
        how="outer",
        left_on="target_column_value",
        right_on="compare_column_value",
    )
    fill_na_columns = ["target_metric_value", "compare_metric_value"]
    merge_df[fill_na_columns] = merge_df[fill_na_columns].fillna(0)
    sub_reason_data = merge_df.assign(
        search_column=search_column,
        metric_change=merge_df["target_metric_value"]
        - merge_df["compare_metric_value"],
    )
    return sub_reason_data


def find_insight(df, metric):
    raise NotImplementedError()
