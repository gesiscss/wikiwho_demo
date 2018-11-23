
import numpy as np
import pandas as pd

from wikiwho_wrapper import WikiWho


class ConflictCalculator:

    def __init__(self, page, wikiwho):
        self.wikiwho = wikiwho
        self.page = page

    def calculate(self):

        print('Downloading and preparing revisions')
        revisions = self.prepare_revisions()

        print('Downloading and preparing tokens')
        tokens = self.prepare_tokens()

        print('Merge tokens and revisions')
        df = self.merge_tokens_and_revisions(tokens, revisions)

        print('Calculate time differences of undos')
        df = self.calculate_time_diffs(df)

        print('Get the conflicts')
        self.conflicts = self.get_conflicts(df)

        print('Calculate the token conflict')
        self.df = self.calculate_token_conflict_score(df, self.conflicts)

        return self.df

    def prepare_revisions(self):
        revisions = self.wikiwho.dv.rev_ids_of_article(self.page)
        revisions = revisions.rename(columns={'o_editor': 'editor'})
        revisions['rev_time'] = pd.to_datetime(revisions['rev_time'])
        return revisions

    def prepare_tokens(self):
        tokens = self.wikiwho.dv.all_content(self.page)
        tokens = self.fill_first_insertion(tokens)
        tokens = self.remove_unique_rows(tokens)
        tokens = self.remove_stopwords(tokens)
        tokens = self.wide_to_long(tokens)
        return tokens

    def fill_first_insertion(self, tokens):
        """The 'in' column only contains reinsertions, the first insertion is indicated
        with -1. Nevertheless, the first insertion of the token is equal to the original 
        revision id, so here the -1s are replaced by the original revision id"""
        tokens.loc[tokens['in'] == -1,
                   'in'] = tokens.loc[tokens['in'] == -1, 'o_rev_id']
        return tokens

    def remove_unique_rows(self, tokens):
        """ A token that just have one row will nor cause any conflict neither the insertions
        or deletions can be undos, so they are removed. In order for a conflict to exist,
        there should be at least three actions, and tokens with on row only have maximum two: 
        the first insertion and a possible deletion.

        """
        return tokens[tokens.duplicated(subset=['token_id'], keep=False)]

    def remove_stopwords(self, tokens, stopwords_fn='data/stopword_list.txt'):
        """Open a list of stop words and remove the from the dataframe the tokens that 
        belong to this list.
        """
        stop_words = open(stopwords_fn, 'r').read().split()
        return tokens[~tokens['token'].isin(stop_words)]

    def wide_to_long(self, tokens):
        """ Each row in the tokens data frame has an in and out column. This method
        transforms those two columns in two rows. The new dataframe will contain a column
        `action` that indicates if it is an `in` or an `out`, and a column `rev_id` that
        contains the revision id in which it happens (the revision ids were the values
        orginally present in the `in` and `out` columns)
        """
        return pd.wide_to_long(
            tokens.rename(columns={
                'in': 'rev_id_in',
                'out': 'rev_id_out'
            }).reset_index(),
            'rev_id', 'index', 'action', sep='_', suffix='.+').reset_index(
        ).drop(columns='index').sort_values('token_id')

    def merge_tokens_and_revisions(self, tokens, revisions):
        """ Here the tokens are merged with the revisions so that we have information about
        the time and the editor that executed the action in the token. This also returns the
        data sorted by token_id and rev_time, so it can be used to calculate time differences.
        """
        return pd.merge(tokens, revisions[['rev_time', 'rev_id', 'editor']],
                        how='left', on='rev_id').sort_values(['token_id', 'rev_time'])

    def calculate_time_diffs(self, df):

        # first calculate the times for all cases. This will produce some errors because
        # the shift is not aware of the tokens (revision times should belong to the same
        # token). This errors are removed in the next lines
        df['time_diff'] = df['rev_time'] - df.shift(2)['rev_time']

        # the errors are produced in the first two actions (first insertion and deletion) of
        # each token. The first insertion and deletion are guaranteed to exist because duplicates
        # were removed.
        to_delete = (
            # First row of each token
            (df['o_rev_id'] == df['rev_id']) |
            # Second row of each token
            (df.shift(1)['o_rev_id'] == df.shift(1)['rev_id']))

        # delete but keep the row
        df.loc[to_delete, 'time_diff'] = np.nan

        # For testing the above
        if False:
            # this line is equivalent and clearer to the above 3 but much
            # slower)
            df['time_diff2'] = df.groupby('token_id').apply(
                lambda group: group['rev_time'] - group.shift(2)['rev_time']).values

            # this is for testing the two methods
            if (df['time_diff'].fillna(-1) == df['time_diff2'].fillna(-1)).all():
                print('Group by is equivalent to flat operations')

        return df

    def get_conflicts(self, df):
        """ This return a selector (boolean vector) of the actions that classify as conflicts, i.e.
        1. insertion-deletion-insertion of the same token, where the editor is the same for the
        insertions but different from the deletions.
        2. delection-insertion-deletion of the same token, where the editor is the same for the
        deletions but different from the insertions.
        """
        return ((df['token_id'] == df.shift(1)['token_id']) &
                (df['token_id'] == df.shift(2)['token_id']) &
                (df['editor'] != df.shift(1)['editor']) &
                (df['editor'] == df.shift(2)['editor']))

    def get_elegible_actions(self, df):
        """ Since the difference of time is calculated based on the 2nd previous row 
        (because  we  are looking to undos in the form of insertion-delection-insertion or 
        deletion-insertion-deletion), this means that the first two action per tokens are
        expected to be NaN (as the 2nd previous row does not exist for that token). Similarly,
        this actions should not be elegible as they have no chance of producing conflicts.
        """
        return df['time_diff'].notnull()

    def calculate_token_conflict_score(self, df, conflicts, base=3600):
        """  Although the time difference is a good indicator of conflicts, i.e. undos that take years
        are probably not very relevant, there are two important transformations in order for it to
        make sense, let t be the time difference in seconds:
        1. It needs to be the inverse of the time (i.e. 1/t), so higher value srepresent higher 
        conflicts.
        2. Calculating the log(t, base=3600) soften the curve so that the values are not so extreme. 
        Moreover, it sets 1 hour (3600 secs) as the decisive point in which an undo is more relevant.
        """
        df['conflict'] = np.log(
            base) / np.log(df.loc[conflicts, 'time_diff'].astype('timedelta64[s]') + 2)
        return df

    def get_all_conflicts(self):
        return self.df[self.conflicts]

    def get_page_conflict_score(self):
        """ This calculates a total conflict score for the page. It adds all the conflicts 
        and divide them by the summ of all elegible actions (i.e. actions that have the potential
        of being undos)
        """
        return (self.df.loc[self.conflicts, 'conflict'].sum() /
                self.df[self.get_elegible_actions(self.df)].shape[0])

    def get_page_conflict_score2(self):
        return (self.df.loc[self.conflicts, 'conflict'].sum() /
                len(self.df['rev_id'] == self.df['o_rev_id']))

    def get_conflict_score_per_editor(self):
        """ This calculates an score per editor. It adds all the conflicts per editor, and 
        divide them by the summ of all elegible actions that belong to each editor( i.e. 
        actions that have the potential of being undos)
        """


        # calculate the number of conflicts per editor
        confs_n = self.df.loc[self.conflicts, [
            'editor', 'conflict']].groupby('editor').count().rename(
                columns={'conflict': 'conflict_n'})
        # calculate the accumulated conflict per editor
        confs_ed = self.df.loc[self.conflicts, [
            'editor', 'conflict']].groupby('editor').sum()
        # calculate the 'elegible' actions per editor
        actions = self.df.loc[self.get_elegible_actions(
            self.df), ['editor', 'action']].groupby('editor').count()

        # join the dataframes
        joined = confs_n.join(confs_ed).join(actions)

        # calculate the score of the editor dividing conflicts / actions
        joined['conflict_score'] = joined['conflict'] / joined['action']
        joined['conflict_ratio'] = joined['conflict_n'] / joined['action']

        # return the result sorted in descending order
        return joined.sort_values('conflict_score', ascending=False)

    # c_t = np.log(3600) / (
    #     np.log(
    #         dups_dated.loc[conflicts,['token_id','time_diff']].groupby(
    #             'token_id').sum().astype('timedelta64[s]') + 2
    #     ))

    # c_t.sum()
