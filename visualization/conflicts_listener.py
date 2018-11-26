import pandas as pd
import plotly
from plotly import graph_objs


class ConflictsListener():

    def __init__(self, df):
        self.df = df
        self.df_plotted = None

    def listen(self, begin, end, granularity, black, red):
        df = self.df

        # time diff to seconds
        df['diff_secs'] = df['time_diff'].dt.total_seconds()

        # dates filter
        df = df[(df.rev_time >= begin) & (df.rev_time <= end)]


        # calculate the aggreated values
        df = df.groupby(pd.Grouper(
            key='rev_time', freq=granularity[0])).agg({'conflict': ['sum', 'count'],
                                    'action': ['count'],
                                    'diff_secs':['count', 'sum']}).reset_index()


        self.traces=[]
        df = self.add_trace(df, black, 'rgba(0, 0, 0, 1)')
        df = self.add_trace(df, red, 'rgba(255, 0, 0, .8)')


        # if red != 'None':
        #     data.append(graph_objs.Scatter(
        #         x=list(df['rev_time']), y=list(df[red]),
        #         name=red,
        #         marker=dict(color='rgba(255, 0, 0, .8)')))

        # if blue != 'None':
        #     data.append(graph_objs.Scatter(
        #         x=list(df['rev_time']), y=list(df[blue]),
        #         name=blue,
        #         marker=dict(color='rgba(0, 128, 43, 1)')))

        # if green != 'None':
        #     data.append(graph_objs.Scatter(
        #         x=list(df['rev_time']), y=list(df[green]),
        #         name=green,
        #         marker=dict(color='rgba(0, 153, 255, .8)')))

        layout = graph_objs.Layout(hovermode='closest',
                                   xaxis=dict(title=granularity, ticklen=5,
                                              zeroline=True, gridwidth=2),
                                   yaxis=dict(
                                              ticklen=5, gridwidth=2),
                                   showlegend=True, barmode='group')

        self.df_plotted = df

        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot({"data": self.traces, "layout": layout})

    def add_trace(self, df, metric, color):
        if metric == 'None': 
            return df

        elif metric == 'Conflict Score':          
            df['conflict_score'] = df[('conflict', 'sum')] / df[('diff_secs', 'count')]
            y = df.loc[~df['conflict_score'].isnull(), 'conflict_score']

        elif metric == 'Conflict Ratio':  
            df['conflict_ratio'] = df[('conflict', 'count')] / df[('diff_secs', 'count')]
            y = df.loc[~df['conflict_ratio'].isnull(), 'conflict_ratio']

        elif metric == 'Total Conflicts': 
            y = df[('conflict', 'count')]

        elif metric == 'Total Elegible Actions': 
            y = df[('diff_secs', 'count')]

        elif metric == 'Total Actions': 
            y = df[('action', 'count')]

        elif metric == 'Total Time': 
            y = df[('diff_secs', 'sum')]

        elif metric == 'Time per Elegible Action': 
            df['time_per_elegible_action'] = df[('diff_secs', 'sum')] / df[('diff_secs', 'count')]
            y = df.loc[~df['time_per_elegible_action'].isnull(), 'time_per_elegible_action']

        self.traces.append(
            graph_objs.Scatter(
                x=df['rev_time'], y=y,
                name=metric,
                marker=dict(color=color))
        )

        return df

