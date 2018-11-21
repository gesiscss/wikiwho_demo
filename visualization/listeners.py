#import matplotlib.pyplot as plt
import pandas as pd
import plotly
#import plotly.plotly as py
from plotly import graph_objs
#from wordcloud import WordCloud


class DFListener():

    def __init__(self, df):
        self.df = df
        self.df_plotted = None

    def views_per_period(self, begin, end, granularity):
        df = self.df

        if begin < end or begin == end:
            variable = 0

        elif begin > end:
            variable = end
            end = begin
            begin = variable
        else:
            variable = 1
            print('Can not be the case!')

        filtered_df = df[(df.timestamp >= begin) & (df.timestamp <= end)]
        groupped_df = filtered_df.groupby(pd.Grouper(
            key='timestamp', freq=granularity[0])).sum().reset_index()

        # Plot Graph
        views = list(groupped_df.views)
        month = list(groupped_df.timestamp)

        trace1 = graph_objs.Scatter(
            x=month, y=views,
            mode='lines+markers', name='Adds',
            marker=dict(color='rgba(0, 128, 43, .8)')
        )

        layout = graph_objs.Layout(hovermode='closest',
                                   xaxis=dict(title=granularity, ticklen=5,
                                              zeroline=True, gridwidth=2),
                                   yaxis=dict(title='Actions',
                                              ticklen=5, gridwidth=2),
                                   showlegend=True)

        data = [trace1]

        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot({"data": data, "layout": layout})

        self.df_plotted = groupped_df

    def editions_per_month(self, begin, end, granularity, first_action, second_action):
        df = self.df

        df = df[(df.year_month >= begin) & (df.year_month <= end)]

        df = df.groupby(pd.Grouper(
            key='year_month', freq=granularity[0])).sum().reset_index()

        # if actions == 'Additions':
        #     df_sel = df.loc[:,'adds':'adds_stopword_count']
        # elif actions == 'Reinsertions':
        #     df_sel = df.loc[:,'reins':'reins_stopword_count']
        # elif actions == 'Deletions':
        #     df_sel = df.loc[:,'dels':'dels_stopword_count']
        # elif actions == 'All Actions':
        #     df_sel = df.loc[:,'actions':'actions_stopword_count']

        # data = [
        #     graph_objs.Bar(
        #         x=df.year_month, y=ser,
        #         name=name,
        #         marker=dict(color=f'rgba(0, 128, 43, {i/4.0})'))
        #     for i, (name, ser) in enumerate(df_sel.iteritems(), 1)
        # ]

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

        # trace3 = graph_objsBar(
        #     x=list(df['year_month']), y=list(df.total_dels),
        #     name='Total dels',
        #     marker=dict(color='rgba(255, 0, 0, .8)'))

        # trace4 = graph_objsBar(
        #     x=list(df['year_month']), y=list(df.dels_surv_48h),
        #     name='48h survived',
        #     marker=dict(color='rgba(255, 102, 102, .8)'))

        # trace5 = graph_objsBar(
        #     x=list(df['year_month']), y=list(df.total_reins),
        #     name='Total reinserts',
        #     marker=dict(color='rgba(0, 51, 153, .8)'))

        # trace6 = graph_objsBar(
        #     x=list(df['year_month']), y=list(df.reins_surv_48h),
        #     name='48h survived',
        #     marker=dict(color='rgba(0, 153, 255, .8)'))

        layout = graph_objs.Layout(hovermode='closest',
                                   xaxis=dict(title=granularity, ticklen=5,
                                              zeroline=True, gridwidth=2),
                                   yaxis=dict(title='Actions',
                                              ticklen=5, gridwidth=2),
                                   showlegend=True, barmode='group')

        #data = [trace1, trace2, trace3, trace4, trace5, trace6]

        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot({"data": data, "layout": layout})


class Graph():

    def __init__(self, df):
        self.df = df

    def activityOverview(self, begin, end):

        df4 = self.df

        df4 = df4[(df4.ym >= begin) & (df4.ym <= end)]

        trace1 = graph_objs.Scatter(x=list(df4['ym']), y=list(df4.total_adds),
                                    mode='lines+markers', name='Adds',
                                    marker=dict(color='rgba(0, 128, 43, .8)'))

        trace2 = graph_objs.Scatter(
            x=list(df4['ym']), y=list(df4.total_dels),
            mode='lines+markers', name='Dels',
            marker=dict(color='rgba(255, 0, 0, .8)'))

        trace3 = graph_objs.Scatter(
            x=list(df4['ym']), y=list(df4.total_reins),
            mode='lines+markers', name='Reins',
            marker=dict(color='rgba(0, 51, 153, .8)'))

        layout = graph_objs.Layout(hovermode='closest',
                                   xaxis=dict(title='Month', ticklen=5,
                                              zeroline=True, gridwidth=2),
                                   yaxis=dict(title='Actions',
                                              ticklen=5, gridwidth=2),
                                   showlegend=True)

        data = [trace1, trace2, trace3]

        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot({"data": data, "layout": layout})

    def addRatio(self, begin, end):

        df4 = self.df
        df4['ym'] = pd.to_datetime(df4['ym'])

        df4 = df4[(df4.ym >= begin) & (df4.ym <= end)]

        trace1 = graph_objs.Bar(
            x=list(df4['ym']), y=list(df4.total_adds),
            name='Total adds',
            marker=dict(color='rgba(0, 128, 43, .8)'))

        trace2 = graph_objs.Bar(
            x=list(df4['ym']), y=list(df4.adds_surv_48h),
            name='48h survived',
            marker=dict(color='rgba(0, 230, 77, .8)'))

        data = [trace1, trace2]

        layout = graph_objs.Layout(hovermode='closest',
                                   xaxis=dict(title='Month', ticklen=5,
                                              zeroline=True, gridwidth=2),
                                   yaxis=dict(title='Actions',
                                              ticklen=5, gridwidth=2),
                                   showlegend=True, barmode='group')

        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot({"data": data, "layout": layout})

    def delRatio(self, begin, end):
        df4 = self.df
        df4['ym'] = pd.to_datetime(df4['ym'])

        df4 = df4[(df4.ym >= begin) & (df4.ym <= end)]

        trace1 = graph_objs.Bar(
            x=list(df4['ym']), y=list(df4.total_dels),
            name='Total dels',
            marker=dict(color='rgba(255, 0, 0, .8)'))

        trace2 = graph_objs.Bar(
            x=list(df4['ym']), y=list(df4.dels_surv_48h),
            name='48h survived',
            marker=dict(color='rgba(255, 102, 102, .8)'))

        layout = graph_objs.Layout(hovermode='closest',
                                   xaxis=dict(title='Month', ticklen=5,
                                              zeroline=True, gridwidth=2),
                                   yaxis=dict(title='Actions',
                                              ticklen=5, gridwidth=2),
                                   showlegend=True, barmode='group')

        data = [trace1, trace2]

        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot({"data": data, "layout": layout})

    def reinsRatio(self, begin, end):
        df4 = self.df
        df4['ym'] = pd.to_datetime(df4['ym'])

        df4 = df4[(df4.ym >= begin) & (df4.ym <= end)]

        trace1 = graph_objs.Bar(
            x=list(df4['ym']), y=list(df4.total_reins),
            name='Total reinserts',
            marker=dict(color='rgba(0, 51, 153, .8)'))

        trace2 = graph_objs.Bar(
            x=list(df4['ym']), y=list(df4.reins_surv_48h),
            name='48h survived',
            marker=dict(color='rgba(0, 153, 255, .8)'))

        data = [trace1, trace2]

        layout = graph_objs.Layout(hovermode='closest',
                                   xaxis=dict(title='Month', ticklen=5,
                                              zeroline=True, gridwidth=2),
                                   yaxis=dict(title='Actions',
                                              ticklen=5, gridwidth=2),
                                   showlegend=True, barmode='group')

        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot({"data": data, "layout": layout})

    def views_per_period(self, begin, end, granularity):
        df = self.df

        if begin < end or begin == end:
            variable = 0

        elif begin > end:
            variable = end
            end = begin
            begin = variable
        else:
            variable = 1
            print('Can not be the case!')

        filteredDF = df[(df.timestamp >= begin) & (df.timestamp <= end)]

        # Show Statistics

        print('')
        print('--------------------')
        print('Statistics')
        print('--------------------')
        print('Total Amount of views within timeline: {}'.format(
            filteredDF['views'].sum()))
        print('Avg.  Amount of views within timeline: {}'.format(
            filteredDF['views'].mean()))
        print('Max.  Amount of views within timeline: {}'.format(
            filteredDF['views'].max()))
        print('Min.  Amount of views within timeline: {}'.format(
            filteredDF['views'].min()))

        # Plot Graph

        views = list(filteredDF.views)
        month = list(filteredDF.timestamp)

        trace1 = graph_objs.Scatter(
            x=month, y=views,
            mode='lines+markers', name='Adds',
            marker=dict(color='rgba(0, 128, 43, .8)')
        )

        layout = graph_objs.Layout(hovermode='closest',
                                   xaxis=dict(title='Month', ticklen=5,
                                              zeroline=True, gridwidth=2),
                                   yaxis=dict(title='Actions',
                                              ticklen=5, gridwidth=2),
                                   showlegend=True)

        data = [trace1]

        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot({"data": data, "layout": layout})

    # notebook3

    def mActivity(self, begin, end):

        df4 = self.df
        df4 = df4[(df4.ym >= begin) & (df4.ym <= end)]

        trace1 = graph_objs.Scatter(
            x=list(df4['ym']), y=list(df4.total_adds),
            mode='lines+markers', name='Adds',
            marker=dict(color='rgba(0, 128, 43, .8)'))

        trace2 = graph_objs.Scatter(
            x=list(df4['ym']), y=list(df4.total_dels),
            mode='lines+markers', name='Dels',
            marker=dict(color='rgba(255, 0, 0, .8)'))

        trace3 = graph_objs.Scatter(
            x=list(df4['ym']), y=list(df4.total_reins),
            mode='lines+markers', name='Reins',
            marker=dict(color='rgba(0, 51, 153, .8)'))

        layout = graph_objs.Layout(hovermode='closest',
                                   xaxis=dict(title='Month', ticklen=5,
                                              zeroline=True, gridwidth=2),
                                   yaxis=dict(title='Actions',
                                              ticklen=5, gridwidth=2),
                                   showlegend=True)

        data = [trace1, trace2, trace3]

        plotly.offline.init_notebook_mode(connected=True)
        plotly.offline.iplot({"data": data, "layout": layout})

    def filterAdds(self, begin, end, Stopwords, survived_48h_ind, head):

        add_df = self.df

        if begin < end or begin == end:

            if Stopwords == 0 or Stopwords == 1:
                if survived_48h_ind == 0 or survived_48h_ind == 1:
                    add_df = add_df[(add_df.rev_ts >= begin) & (add_df.rev_ts <= end) & (
                        add_df.survived_48h_ind == survived_48h_ind) & (add_df.is_stopword_ind == Stopwords)]
                elif survived_48h_ind == 2:
                    add_df = add_df[
                        (add_df.rev_ts >= begin) & (add_df.rev_ts <= end) & (add_df.is_stopword_ind == Stopwords)]
                else:
                    print(
                        'Can not be the case! surviveR not 0,1 or 2 at Stopwords 0 or 1!')

            elif Stopwords == 2:
                if survived_48h_ind == 0 or survived_48h_ind == 1:
                    add_df = add_df[(add_df.rev_ts >= begin) & (add_df.rev_ts <= end) & (
                        add_df.survived_48h_ind == survived_48h_ind)]
                elif survived_48h_ind == 2:
                    add_df = add_df[(add_df.rev_ts >= begin)
                                    & (add_df.rev_ts <= end)]
                else:
                    print('Can not be the case! surviveR not 0,1 or 2 at Stopwords 2!')

            else:
                print('Can not be the case! Stopwords not 0,1 or 2!')

        elif end < begin:
            variable = end
            end = begin
            begin = variable

            if Stopwords == 0 or Stopwords == 1:
                if survived_48h_ind == 0 or survived_48h_ind == 1:
                    add_df = add_df[(add_df.rev_ts >= begin) & (add_df.rev_ts <= end) & (
                        add_df.survived_48h_ind == survived_48h_ind) & (add_df.is_stopword_ind == Stopwords)]
                elif survived_48h_ind == 2:
                    add_df = add_df[
                        (add_df.rev_ts >= begin) & (add_df.rev_ts <= end) & (add_df.is_stopword_ind == Stopwords)]
                else:
                    print(
                        'Can not be the case! surviveR not 0,1 or 2 at Stopwords 0 or 1!')

            elif Stopwords == 2:
                if survived_48h_ind == 0 or survived_48h_ind == 1:
                    add_df = add_df[(add_df.rev_ts >= begin) & (add_df.rev_ts <= end) & (
                        add_df.survived_48h_ind == survived_48h_ind)]
                elif survived_48h_ind == 2:
                    add_df = add_df[(add_df.rev_ts >= begin)
                                    & (add_df.rev_ts <= end)]
                else:
                    print('Can not be the case! surviveR not 0,1 or 2 at Stopwords 2!')

            else:
                print('Can not be the case! Stopwords not 0,1 or 2!')
        else:
            print('Date Filter Error!')

        a = add_df.groupby('string').size().reset_index().rename(
            columns={0: 'count'})
        a = a.sort_values(by='count', ascending=False).head(head)
        print(a)

        try:

            text = ' '.join(list(a['string']))

            wc = WordCloud(max_words=100, width=800, height=400, background_color='black', max_font_size=50,
                           colormap="Greens").generate(text)
            plt.figure(figsize=(10, 5))
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.show()
        except ValueError:
            print('It is not possible to create a WordCloud with this filter!')

    def filterDel(self, begin, end, Stopwords, survived_48h_ind, head):

        del_df = self.df

        if begin < end or begin == end:

            if Stopwords == 0 or Stopwords == 1:
                if survived_48h_ind == 0 or survived_48h_ind == 1:
                    del_df = del_df[(del_df.rev_ts >= begin) & (del_df.rev_ts <= end) & (
                        del_df.survived_48h_ind == survived_48h_ind) & (del_df.is_stopword_ind == Stopwords)]
                elif survived_48h_ind == 2:
                    del_df = del_df[
                        (del_df.rev_ts >= begin) & (del_df.rev_ts <= end) & (del_df.is_stopword_ind == Stopwords)]
                else:
                    print(
                        'Can not be the case! surviveR not 0,1 or 2 at Stopwords 0 or 1!')

            elif Stopwords == 2:
                if survived_48h_ind == 0 or survived_48h_ind == 1:
                    del_df = del_df[(del_df.rev_ts >= begin) & (del_df.rev_ts <= end) & (
                        del_df.survived_48h_ind == survived_48h_ind)]
                elif survived_48h_ind == 2:
                    del_df = del_df[(del_df.rev_ts >= begin)
                                    & (del_df.rev_ts <= end)]
                else:
                    print('Can not be the case! surviveR not 0,1 or 2 at Stopwords 2!')

            else:
                print('Can not be the case! Stopwords not 0,1 or 2!')

        elif end < begin:
            variable = end
            end = begin
            begin = variable

            if Stopwords == 0 or Stopwords == 1:
                if survived_48h_ind == 0 or survived_48h_ind == 1:
                    del_df = del_df[(del_df.rev_ts >= begin) & (del_df.rev_ts <= end) & (
                        del_df.survived_48h_ind == survived_48h_ind) & (del_df.is_stopword_ind == Stopwords)]
                elif survived_48h_ind == 2:
                    del_df = del_df[
                        (del_df.rev_ts >= begin) & (del_df.rev_ts <= end) & (del_df.is_stopword_ind == Stopwords)]
                else:
                    print(
                        'Can not be the case! surviveR not 0,1 or 2 at Stopwords 0 or 1!')

            elif Stopwords == 2:
                if survived_48h_ind == 0 or survived_48h_ind == 1:
                    del_df = del_df[(del_df.rev_ts >= begin) & (del_df.rev_ts <= end) & (
                        del_df.survived_48h_ind == survived_48h_ind)]
                elif survived_48h_ind == 2:
                    del_df = del_df[(del_df.rev_ts >= begin)
                                    & (del_df.rev_ts <= end)]
                else:
                    print('Can not be the case! surviveR not 0,1 or 2 at Stopwords 2!')

            else:
                print('Can not be the case! Stopwords not 0,1 or 2!')
        else:
            print('Date Filter Error!')

        a = del_df.groupby('string').size().reset_index().rename(
            columns={0: 'count'})
        a = a.sort_values(by='count', ascending=False).head(head)
        print(a)

        try:
            text = ' '.join(list(a['string']))

            wc = WordCloud(max_words=100, width=800, height=400, background_color='white', max_font_size=50,
                           colormap="Reds").generate(text)
            plt.figure(figsize=(10, 5))
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.show()
        except ValueError:
            print('It is not possible to create a WordCloud with this filter!')
