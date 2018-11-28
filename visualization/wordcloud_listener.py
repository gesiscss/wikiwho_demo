import pandas as pd
import matplotlib.pyplot as plt

from IPython.display import display, Markdown as md
from .wordclouder import WordClouder


class WCListener():

    def __init__(self, calculator, max_words=100):
        self.calculator = calculator
        self.max_words = max_words

    def listen(self, _range, action, source):
        if source == 'All actions':
            df = self.calculator.all_actions
        elif source == 'Elegible Actions':
            df = self.calculator.elegible_actions
        elif source == 'Only Conflicts':
            df = self.calculator.conflicts

        df = df[(df.rev_time.dt.date >= _range[0]) &
                (df.rev_time.dt.date <= _range[1])]

        if action == 'Just Insertions':
            df = df[df['action'] == 'in']
        elif action == 'Just Deletions':
            df = df[df['action'] == 'out']

        if len(df) == 0:
            display(md(f"**There is zero cases to build the wordcloud**"))
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
            display(md("Cannot create the wordcloud, there were zero conflict tokens."))



class WCConflictingListener():

    def __init__(self, df, max_words=100):
        self.df = df
        self.max_words = max_words

    def listen(self, _range, action, only_conflict):
        df = self.df

        df = df[(df.rev_time.dt.date >= _range[0]) &
                (df.rev_time.dt.date <= _range[1])]

        if action == 'Just Insertions':
            df = df[df['action'] == 'in']
        elif action == 'Just Deletions':
            df = df[df['action'] == 'out']

        if only_conflict:
            df = df[~df['conflict'].isnull()]

        if len(df) == 0:
            display(md(f"**There is zero cases to build the wordcloud**"))
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
            display(md("Cannot create the wordcloud, there were zero conflict tokens."))
