import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from IPython.display import display, Markdown as md


class WCListener():

    def __init__(self, df):
        self.df = df

    def tokens_wordcloud(self, begin, end, action, only_conflict: True):
        """Summary
        
        Args:
            begin (TYPE): Description
            end (TYPE): Description
            action (TYPE): in or out or both
            only_conflict (True): Description
        
        
        """
        df = self.df

        df = df[(df.rev_time >= begin) & (df.rev_time <= end)]


        # Create the rest of the filters with the other parameters
        bow = df.groupby('token').size()



        # Revisions involved
        display(md(f"### The below token conflicts ocurred in a total of {len(df['rev_id'].unique())} revisions:"))


        # Create word cloud
        wc = WordCloud(width=800, height=400,background_color='white',
                       max_font_size = 50,collocations=False).generate_from_frequencies(bow)

        # Plot

        plt.figure(figsize=(14,7))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()