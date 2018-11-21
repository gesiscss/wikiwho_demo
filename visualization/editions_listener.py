import pandas as pd
import plotly
from plotly import graph_objs


class DFListener():

    def __init__(self, df):
        self.df = df
        self.df_plotted = None

    def editions_per_month(self, begin, end, granularity, first_action, second_action):
        df = self.df

        df = df[(df.year_month >= begin) & (df.year_month <= end)]

        df = df.groupby(pd.Grouper(
            key='year_month', freq=granularity[0])).sum().reset_index()


        data = [
            graph_objs.Bar(
                x=list(df['year_month']), y=list(df[first_action]),
                name=first_action,
                marker=dict(color='rgba(0, 128, 43, 1)')),
            graph_objs.Bar(
                x=list(df['year_month']), y=list(df[second_action]),
                name=second_action,
                marker=dict(color='rgba(0, 230, 77, 1)'))
        ]
        layout = graph_objs.Layout(hovermode='closest',
                                   xaxis=dict(title=granularity, ticklen=5,
                                              zeroline=True, gridwidth=2),
                                   yaxis=dict(title='Actions',
                                              ticklen=5, gridwidth=2),
                                   showlegend=True, barmode='group')


        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot({"data": data, "layout": layout})
