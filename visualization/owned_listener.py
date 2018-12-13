import pandas as pd
import plotly
from plotly import graph_objs


class OwnedListener():

    def __init__(self, df, editor):
        self.df = df.sort_values(['token_id', 'rev_time'], ascending=True)
        self.editor = editor
        self.df_plotted = None

    def listen(self, _range, granularity, black):
        df = self.df

        df = df[(df.rev_time.dt.date >= _range[0]) &
                (df.rev_time.dt.date <= _range[1])]

        self.doi = df.loc[df['editor'] == self.editor, 'rev_time'].dt.to_period(
            granularity[0]).dt.to_timestamp(granularity[0]).sort_values(ascending=False).unique()

        self.traces = []
        self.is_norm_scale = True
        df = self.__add_trace(df, black, 'rgba(0, 0, 0, 1)')

        _range = None
        if self.is_norm_scale:
            _range = [0, 100]

        layout = graph_objs.Layout(hovermode='closest',
                                   xaxis=dict(title=granularity, ticklen=5,
                                              zeroline=True, gridwidth=2),
                                   yaxis=dict(
                                       ticklen=5, gridwidth=2, range=_range),
                                   legend=dict(x=0.5, y=1.2),
                                   showlegend=True, barmode='group')

        self.df_plotted = df

        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot({"data": self.traces, "layout": layout})

    def __add_trace(self, df, metric, color):
        _x = []
        _y = []

        if metric == 'Tokens Owned':
            self.is_norm_scale = False
            for rev_time in self.doi:
                df = df[df['rev_time'] <= rev_time]
                last_action = df.groupby('token_id').last()
                surv = last_action[last_action['action'] != 'out']

                _x.append(rev_time)
                _y.append(len(surv[surv['o_editor'] == self.editor]))

        elif metric == 'Tokens Owned (%)':
            for rev_time in self.doi:
                df = df[df['rev_time'] <= rev_time]
                last_action = df.groupby('token_id').last()
                surv = last_action[last_action['action'] != 'out']

                _x.append(rev_time)
                _y.append(
                    100 * len(surv[surv['o_editor'] == self.editor]) / len(surv))

        self.traces.append(
            graph_objs.Scatter(
                x=pd.Series(_x), y=_y,
                name=metric,
                marker=dict(color=color))
        )

        return df
