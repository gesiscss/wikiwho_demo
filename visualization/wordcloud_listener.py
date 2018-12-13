import pandas as pd
import matplotlib.pyplot as plt

from IPython.display import display, Markdown as md
from .wordclouder import WordClouder

#  WCListener
#wc = WCListener(calculator)
# wc = WCListener(sources = {
#     'All actions': calculator.all_actions,
#     'Elegible Actions': calculator.elegible_actions,
#     'Only Conflicts': calculator.conflicts
# })
# .interact(listen.listen, ..., source=list(wc.sources.keys()),...editor=fixed(..)

#  WCSimpleListener
# df = calculator.elegible_actions
# ...
# wc = WCSimpleListener(df)

# df = calculator.elegible_actions
# ...
# wc = WCListener(sources ={
#     'Elegible Actions': df,
#     'Only Conflicts': df[~df['conflict'].isnull()]
#})
# .interact(listen.listen, ..., source=list(wc.sources.keys()),...


class WCListener():

    def __init__(self, sources, max_words=100):
        # def __init__(self, calculator, max_words=100):

        self.sources = sources
        # self.calculator = calculator
        self.max_words = max_words

    def listen(self, _range, source, action, editor):
        df = self.sources[source]

        df = df[(df.rev_time.dt.date >= _range[0]) &
                (df.rev_time.dt.date <= _range[1])]

        if action == 'Just Insertions':
            df = df[df['action'] == 'in']
        elif action == 'Just Deletions':
            df = df[df['action'] == 'out']

        if editor != 'All':
            df = df[df['name'] == editor]

        if len(df) == 0:
            display(md(f"**There are no words to build the word cloud.**"))
            return 0

        df_in = df[df['action'] == 'in']['token'] + '+'
        df_out = df[df['action'] == 'out']['token'] + '-'
        in_out = pd.concat([df_in, df_out])

        word_counts = in_out.value_counts()[:self.max_words]
        colors = {'+': '#CC3300', '-': '#003399'}

        # Create word cloud
        wc = WordClouder(word_counts, colors, self.max_words)

        try:
            wcr = wc.get_wordcloud()
            display(md(f"**Only top {self.max_words} most frequent words displayed.**"))

            # Revisions involved
            display(md(f"### The below token conflicts ocurred in a total of {len(df['rev_id'].unique())} revisions:"))

            # Plot
            plt.figure(figsize=(14, 7))
            plt.imshow(wcr, interpolation="bilinear")
            plt.axis("off")
            plt.show()

        except ValueError:
            display(
                md("Cannot create the wordcloud, there were zero conflict tokens."))


class SimpleWCListener():

    def __init__(self, df, max_words=100):
        self.df = df
        self.max_words = max_words

    def listen(self, _range, action, editor, only_conflict):
        df = self.df

        df = df[(df.rev_time.dt.date >= _range[0]) &
                (df.rev_time.dt.date <= _range[1])]

        if action == 'Just Insertions':
            df = df[df['action'] == 'in']
        elif action == 'Just Deletions':
            df = df[df['action'] == 'out']

        if editor != 'All':
            df = df[df['name'] == editor]

        if only_conflict:
            df = df[~df['conflict'].isnull()]

        if len(df) == 0:
            display(md(f"**There are no words to build the word cloud.**"))
            return 0

        df_in = df[df['action'] == 'in']['token'] + '+'
        df_out = df[df['action'] == 'out']['token'] + '-'
        in_out = pd.concat([df_in, df_out])

        word_counts = in_out.value_counts()[:self.max_words]
        colors = {'+': '#CC3300', '-': '#003399'}

        # Create word cloud
        wc = WordClouder(word_counts, colors, self.max_words)

        try:
            wcr = wc.get_wordcloud()

            # Revisions involved
            display(md(f"### The below token conflicts ocurred in a total of {len(df['rev_id'].unique())} revisions:"))

            # Plot
            plt.figure(figsize=(14, 7))
            plt.imshow(wcr, interpolation="bilinear")
            plt.axis("off")
            plt.show()

        except ValueError:
            display(
                md("Cannot create the wordcloud, there were zero conflict tokens."))
