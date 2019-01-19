import pandas as pd
import plotly
from plotly import graph_objs
import datetime

class OwnedListener():

    def __init__(self, df, editor):
        self.df = df.sort_values(['token_id', 'rev_time'], ascending=True).set_index('token_id')
        self.editor = editor
        self.days = days = pd.Series(df.loc[df['o_editor'] == editor, 'rev_time'].dt.to_period('D').unique()).sort_values(ascending=False)

        days = self.days.dt.to_timestamp('D') + pd.DateOffset(1)

        _all = []
        _abs = []
        df = self.df
        for rev_time in days:
            df = df[df['rev_time'] <= rev_time]
            last_action = df.groupby('token_id').last()
            surv = last_action[last_action['action'] != 'out']
            _abs.append(sum(surv['o_editor'] == self.editor))
            _all.append(len(surv))

        self.summ = pd.DataFrame({
            'day': days,
            'abs': _abs,
            'all': _all
            })
        self.summ['res'] = 100 * self.summ['abs'] / self.summ['all']

        self.df_plotted = None

    def listen(self, _range, granularity, trace):
        df = self.df

        df = df[(df.rev_time.dt.date >= _range[0]) &
                (df.rev_time.dt.date <= _range[1] + datetime.timedelta(days=1))]

        self.doi = pd.Series(self.days.dt.to_timestamp(granularity[0]).unique()) + pd.DateOffset(1)
        self.traces = []
        self.is_norm_scale = True

        if trace == 'Tokens Owned':
            self.is_norm_scale = False
            _df = self.summ
            _df['time'] = _df['day'].dt.to_period(granularity[0]).dt.to_timestamp(granularity[0])
            _df = _df[~_df.duplicated(subset='time', keep='first')]
            _y = _df['abs']

        elif trace == 'Tokens Owned (%)':
            _df = self.summ
            _df['time'] = _df['day'].dt.to_period(granularity[0]).dt.to_timestamp(granularity[0])
            _df = _df[~_df.duplicated(subset='time', keep='first')]
            _y = _df['res']
            
        self.traces.append(
            graph_objs.Scatter(
                x=_df['time'], y=_y,
                name=trace,
                marker=dict(color='rgba(255, 0, 0, .5)'))
        )

        self.__add_trace(df, trace, 'rgba(0,0,255, .5)')

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
