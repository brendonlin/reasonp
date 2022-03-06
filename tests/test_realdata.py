import pandas as pd
import reasonp as rp
import pytest


@pytest.mark.skip
def test_x_orders():
    data_path = "tests/data/x_orders.csv"
    df = pd.read_csv(data_path, nrows=10000)
    df.head()
    df["datetime"] = pd.to_datetime(df["event_time"])

    df = df.assign(date=df["datetime"].map(lambda x: x.strftime("%Y-%m-%d")))

    result = rp.find_reason(
        df, "date", ["2020-05-11", "2020-05-10"], compare_metric=("product_id", "count")
    )
    print(result)
