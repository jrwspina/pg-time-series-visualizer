import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'] ,index_col='date')

# Clean data
filter1 = df['value'] >= df['value'].quantile(0.025)
filter2 = df['value'] <= df['value'].quantile(0.975)
df = df[filter1 & filter2]

def draw_line_plot():
    df_line = df.copy(deep=True)
    # Draw line plot
    fig, ax = plt.subplots(figsize=(20,7))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1.5 )
    ax.set_ylim(10000, 200000)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy(deep=True)
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July'
                , 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    months = list(month_names.values())

    df_bar['month'] = df_bar['month'].apply(lambda x: month_names[x])
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=months, ordered=True)
    df_bar.sort_values('month')
    df_bar
    df_bar = df_bar.groupby(['year', 'month'], as_index=False).mean()

    fig, ax = plt.subplots(figsize=(15,13))
    sns.barplot(x='year', y='value', hue='month', data=df_bar)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    plt.legend(title='Months', loc='upper left')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1,2, figsize=(30, 15))

    sns.boxplot(x='year', y='value', data=df_box, ax=ax[0])
    ax[0].set_title('Year-wise Box Plot (Trend)', size=16)
    ax[0].set_xlabel('Year', size=16)
    ax[0].set_ylabel('Page Views', size=16)

    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    sns.boxplot(x='month', y='value',ax=ax[1], order=months, data=df_box)
    ax[1].set_title('Month-wise Box Plot (Seasonality)', size=16)
    ax[1].set_xlabel('Month', size=16)
    ax[1].set_ylabel('Page Views', size=16)

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
