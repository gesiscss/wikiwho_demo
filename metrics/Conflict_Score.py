"""
import api.getArticleRevs as getArticleRevs
import api.getTotalArticleContent as getTotalArticleContent
editor_id = 12797839
revisions = getArticleRevs('5290021')
article = getTotalArticleContent('5290021')
print(conflictScore_token_list (article, editor_id,revisions ))
"""


from datetime import datetime
from collections import defaultdict
import numpy as np
import pandas as pd
import math


# input article = (dataframe) getTotalArticleContent , editor = editor_id, revisions = (dataframe) getArticleRevs
# output (dataframe) editor_token_list with columns=['token_id', 'str',
# 'conflictscore','actions' ]
def conflictScore_token_list(article, editor, revisions):
    editor = str(editor)

    revisions.loc[:, "timestamp"] = pd.to_datetime(
        revisions.loc[:, ("rev_time")])
    revisions1 = [w["rev_id"]
                  for index, w in revisions.iterrows() if w["o_editor"] == editor]

    tokens = article

    stop_words = open('data/stopword_list.txt', 'r').read().split()

    tokens = [row for index, row in tokens.iterrows() if not row[
        "token"] in stop_words]

    editor_tokens = list()
    for token in tokens:

        if token["o_editor"] == editor:
            editor_tokens.append(token)
        else:

            for out_ in token["out"]:

                if out_ in revisions1:
                    editor_tokens.append(token)
                    break
            for in_ in token["in"]:
                if in_ in revisions1:
                    editor_tokens.append(token)
                    break

    editor_token_list = []
    for editor_token in editor_tokens:
        conflict_revisions = list()
        actions = 0
        orev = editor_token["o_rev_id"]
        if orev in revisions1:
            actions = actions + 1
        try:

            out_ = editor_token['out'][0]

        except IndexError:
            in_ = 0
            out_ = 0

        if orev in revisions1 and out_ not in revisions1:
            for i, in_ in enumerate(editor_token['in']):
                if in_ in revisions1:

                    time_orev = revisions[revisions['id'] == orev]['timestamp'].tolist()[
                        0]

                    time_out = revisions[revisions['id'] == out_]['timestamp'].tolist()[
                        0]

                    age1 = time_out - time_orev

                    Conflict_score1 = 1 / \
                        (math.log(age1.total_seconds() + 2, 3600))

                    conflict_revisions.append(float(Conflict_score1))

                    time_re_in = revisions[revisions['id'] == in_]['timestamp'].tolist()[
                        0]

                    age2 = time_re_in - time_out

                    Conflict_score2 = 1 / \
                        (math.log(age2.total_seconds() + 2, 3600))

                    conflict_revisions.append(float(Conflict_score2))
                    break
        out_list = editor_token["out"]
        for i, out_ in enumerate(out_list):

            if out_ in revisions1:
                actions = actions + 1

            try:

                in_ = editor_token['in'][i]

            except IndexError:
                in_ = 0

            if out_ in revisions1 and not in_ in revisions1 and in_ != 0:
                for j in range(i + 1, len(out_list)):
                    out_2 = out_list[j]

                    if out_2 in revisions1:

                        #print(out_, in_, out_2)

                        time_out = revisions[revisions['id'] == out_]['timestamp'].tolist()[
                            0]
                        # print(time_out)

                        time_in = revisions[revisions['id'] == in_]['timestamp'].tolist()[
                            0]
                        # print(time_in)
                        age1 = time_in - time_out

                        Conflict_score1 = 1 / \
                            (math.log(age1.total_seconds() + 2, 3600))

                        conflict_revisions.append(float(Conflict_score1))

                        time_re_out = revisions[revisions['id'] == out_2]['timestamp'].tolist()[
                            0]

                        age2 = time_re_out - time_in

                        Conflict_score2 = 1 / \
                            (math.log(age2.total_seconds() + 2, 3600))

                        conflict_revisions.append(float(Conflict_score2))
                        break

        in_list = editor_token['in']

        for i, in_ in enumerate(in_list):

            if in_ in revisions1:
                actions = actions + 1

            try:
                out_ = editor_token['out'][i]
            except IndexError:
                out_ = 0

            if in_ in revisions1 and not out_ in revisions1 and out_ != 0:

                for j in range(i + 1, len(in_list)):
                    in_2 = in_list[j]

                    if in_2 in revisions1:

                        #print(in_, out_, in_2)

                        time_in = revisions[revisions['id'] == in_]['timestamp'].tolist()[
                            0]

                        time_out = revisions[revisions['id'] == out_]['timestamp'].tolist()[
                            0]

                        age1 = time_in - time_out

                        Conflict_score1 = 1 / \
                            (math.log(age1.total_seconds() + 2, 3600))

                        conflict_revisions.append(float(Conflict_score1))

                        time_re_in = revisions[revisions['id'] == in_2]['timestamp'].tolist()[
                            0]

                        age2 = time_re_in - time_out

                        Conflict_score2 = 1 / \
                            (math.log(age2.total_seconds() + 2, 3600))

                        conflict_revisions.append(float(Conflict_score2))
                        break

        summe = sum(conflict_revisions)
        conflictscore = 0
        if summe != 0:
            conflictscore = summe / actions

        editor_token_list.append([editor_token['token_id'], editor_token[
                                 'str'], conflictscore, actions])

    editor_token_list_df = pd.DataFrame(editor_token_list, columns=[
                                        'token_id', 'str', 'conflictscore', 'actions'])

    return editor_token_list_df
# input article = (dataframe) getTotalArticleContent , editor = editor_id, revisions = (dataframe) getTotalArticleContent
# output (double) conflictscore


def conflictScore(article, editor, revisions):
    editor = str(editor)
    token_list = conflictScore_token_list(article, editor, revisions)

    sum_conflictscore = token_list['conflictscore'].sum()
    sum_actions = token_list['actions'].sum()

    conflictscore = 0

    if sum_conflictscore != 0:
        conflictscore = sum_conflictscore / sum_actions

    return conflictscore
