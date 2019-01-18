import pandas as pd
import plotly
from plotly import graph_objs


class OwnedListener():

    def __init__(self, df, editor):
        self.df = df.sort_values(['token_id', 'rev_time'], ascending=True).set_index('token_id')
        self.editor = editor
        self.df_plotted = None

    def listen(self, _range, granularity, trace):
        df = self.df

        df = df[(df.rev_time.dt.date >= _range[0]) &
                (df.rev_time.dt.date <= _range[1])]

        self.doi = df.loc[df['editor'] == self.editor, 'rev_time'].dt.to_period(
            granularity[0]).dt.to_timestamp(granularity[0]).sort_values(ascending=False).unique()

        self.traces = []
        self.is_norm_scale = True
        df = self.__add_trace(df, trace, 'rgba(0, 0, 0, 1)')

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

    def __add_trace(self, df, trace, color):
        _y = []

        if trace == 'Tokens Owned':
            self.is_norm_scale = False
            for rev_time in self.doi:
                df = df[df['rev_time'] <= rev_time]
                last_action = df.groupby('token_id').last()
                surv = last_action[last_action['action'] != 'out']
                _y.append(len(surv[surv['o_editor'] == self.editor]))

        elif trace == 'Tokens Owned (%)':
            for rev_time in self.doi:
                df = df[df['rev_time'] <= rev_time]
                last_action = df.groupby('token_id').last()
                surv = last_action[last_action['action'] != 'out']
                _y.append(
                    100 * len(surv[surv['o_editor'] == self.editor]) / len(surv))

        self.traces.append(
            graph_objs.Scatter(
                x=self.doi, y=_y,
                name=trace,
                marker=dict(color=color))
        )

        return df
