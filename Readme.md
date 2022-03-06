# Reasonp: data analysis tool for finding reasons for changes in data

Reasonp is a data analysis tool for finding reasons for changes in data. You can use it to explore the reasons for the decline in metrics, and you can also use it to analyze the differences in metrics between different objects. With a simple operation, it can automatically search for potential causes and find inspiration for your analysis.

You need to provide a fine-grained data so that you can find the reasons for you through segmentation. For example, to analyze the fluctuation of traffic, data of various fields of each visit is required.

Example:

```sh
pip install reasonp
```

```python
import reasonp as rp

traffic_data = [
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


df = pd.DataFrame(traffic_data, columns=["source", "platform", "date", "orders"])

# You want to find the reason for the change in traffic between March 3rd and March 2nd
rdf = rp.find_reason(
        df,
        compare_column="date",
        compare_values=["2021-03-03","2021-03-02"],
        compare_metric=("orders", "sum"),
    )
print(rdf)
```

Check the result

| search_column | target_column_value | compare_column_value | target_metric_value | compare_metric_value | metric_change | reason_coef |
| :------------ | :------------------ | :------------------- | ------------------: | -------------------: | ------------: | ----------: |
| platform      | P1                  | P1                   |                   7 |                    2 |             5 |    0.714286 |
| source        | B                   | B                    |                   6 |                    2 |             4 |    0.571429 |
| source        | A                   | A                    |                   4 |                    2 |             2 |    0.285714 |
| platform      | P2                  | P2                   |                   4 |                    2 |             2 |    0.285714 |
| source        | C                   | nan                  |                   1 |                    0 |             1 |    0.142857 |

The traffic change of platform P1 may be the main reason.Because it had 5 more traffic on March 3rd than on March 2nd.

$$

reason\_coef = metric\_change / total\_change


$$

## Commands

Build

```
python -m build
twine upload dist/*
```
