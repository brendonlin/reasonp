import pandas as pd
import reasonp as rp
import pytest


# @pytest.mark.skip
# def test_x_orders():
#     data_path = "tests/data/x_orders.csv"
#     df = pd.read_csv(data_path, nrows=10000)
#     df.head()
#     df["datetime"] = pd.to_datetime(df["event_time"])

#     df = df.assign(date=df["datetime"].map(lambda x: x.strftime("%Y-%m-%d")))

#     result = rp.find_reason(
#         df, "date", ["2020-05-11", "2020-05-10"], compare_metric=("product_id", "count")
#     )
#     print(result)


# @pytest.mark.skip
def test_x_orders():
    data_path = "tests/data/srdf.csv"
    df = pd.read_csv(data_path)

    def regroup(x):
        if x in [2, 3]:
            return 2
        elif x in [1, 4]:
            return 1
        else:
            return 0

    df["group"] = df["group"].map(regroup)
    print(df.head())
    result = rp.find_reason(
        df.query("pay_model == 'cpc'"),
        "group",
        [1, 0],
        compare_metric=("conversion_rate", "sum"),
        weight_metric=("conversion_rate", "count"),
    )
    # result = rp.find_reason(
    #     df,
    #     "pay_model",
    #     ["cpc", "cpm"],
    #     compare_metric=("conversion_rate", "sum"),
    #     weight_metric=("conversion_rate", "count"),
    # )
    print(result)
