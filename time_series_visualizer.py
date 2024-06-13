import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv(
    filepath_or_buffer="fcc-forum-pageviews.csv",
    parse_dates=["date"],
)

# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025))
    & (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    df_line = df.copy()

    # Draw line plot
    fig = df_line.plot(
        kind="line",
        x="date",
        y="value",
        xlabel="Date",
        ylabel="Page Views",
        title="Daily freeCodeCamp Forum Page Views 5/2016-12/2019",
        figsize=(16, 5),
    ).get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["year"] = df_bar["date"].dt.year
    df_bar["Months"] = df_bar["date"].dt.month_name()
    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    df_bar["Months"] = pd.Categorical(
        df_bar["Months"], categories=month_order, ordered=True
    )

    avg_daily_views_per_month = (
        df_bar.groupby(["year", "Months"]).mean().reset_index()
    )

    pivot_table = avg_daily_views_per_month.pivot(
        index="year", columns="Months", values="value"
    )

    # Draw bar plot
    fig = pivot_table.plot(
        kind="bar",
        xlabel="Years",
        ylabel="Average Page Views",
        title="Monthly Average Daily Page Views",
        figsize=(10, 6),
    ).get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.strftime("%b") for d in df_box.date]
    month_order = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    df_box["month"] = pd.Categorical(
        df_box["month"], categories=month_order, ordered=True
    )

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(15, 6))

    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0], palette="pastel")
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    sns.boxplot(x="month", y="value", data=df_box, ax=axes[1], palette="pastel")
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig("box_plot.png")
    return fig
