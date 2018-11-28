
import pandas as pd
import plotly
from plotly import graph_objs


class OwnedListener():

    def __init__(self, df, editor):
        self.df = df.sort_values(['token_id', 'rev_time'], ascending=True)
        self.editor = editor
        self.df_plotted = None

    def listen(self, _range, granularity, trace):
        df = self.df

        df = df[(df.rev_time.dt.date >= _range[0]) &
                (df.rev_time.dt.date <= _range[1])]

        doi = df.loc[df['editor'] == self.editor, 'rev_time'].dt.to_period(
            granularity[0]).dt.to_timestamp(granularity[0]).sort_values(ascending=False).unique()

        _x = []
        _y = []
        if trace == 'Tokens Owned':
            for rev_time in doi:
                df = df[df['rev_time'] <= rev_time]
                last_action = df.groupby('token_id').last()
                surv = last_action[last_action['action'] != 'out']

                _x.append(rev_time)
                _y.append(len(surv[surv['o_editor'] == self.editor]))
        elif trace == 'Tokens Owned (%)':
            for rev_time in doi:
                df = df[df['rev_time'] <= rev_time]
                last_action = df.groupby('token_id').last()
                surv = last_action[last_action['action'] != 'out']

                _x.append(rev_time)
                _y.append(
                    100 * len(surv[surv['o_editor'] == self.editor]) / len(surv))

        data = [
            graph_objs.Scatter(
                x=pd.Series(_x), y=_y,
                marker=dict(color='rgba(0, 0, 0, 1)'))
        ]

        layout = graph_objs.Layout(hovermode='closest',
                                   xaxis=dict(title='Time', ticklen=5,
                                              zeroline=True, gridwidth=2),
                                   yaxis=dict(title=trace,
                                              ticklen=5, gridwidth=2),
                                   legend=dict(x=0.5, y=1.2),
                                   barmode='group')

        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot({"data": data, "layout": layout})
