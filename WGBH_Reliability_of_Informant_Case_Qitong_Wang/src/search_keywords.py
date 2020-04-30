#-*- coding: utf-8 -*-
import os
import csv
import json
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']


def result_visualization(num_affirmed, num_part, num_reversed,
                         num_affirmed_noKeywords, num_part_noKeywords, num_reversed_noKeywords, state):
    """
        :param: all kinds of statistics numbers.

        final result visualization using four pie graphs.
        edited by Qitong Wang; Apr 6th, 2020.
    """
    # 1
    plt.figure(figsize=(9, 6))
    labels = [u'affirmed', u'partly affirmed', u'reversed']
    sizes = [num_affirmed, num_part, num_reversed]
    colors = ['darkcyan', 'turquoise', 'paleturquoise']
    explode = (0, 0, 0)
    patches, text1, text2 = plt.pie(sizes,
                                    explode=explode,
                                    labels=labels,
                                    colors=colors,
                                    autopct='%3.2f%%',
                                    shadow=False,
                                    startangle=90,
                                    pctdistance=0.6)
    plt.title('Statistics of criminal cases containing keywords("informant" and "CI"); classification for affirmation')
    plt.axis('equal')
    plt.savefig('pie_pic/' + state + '_KW_affirm.jpg')
    # 2
    plt.figure(figsize=(9, 6))
    labels = [u'affirmed', u'partly affirmed', u'reversed']
    sizes = [num_affirmed_noKeywords, num_part_noKeywords, num_reversed_noKeywords]
    colors = ['darkcyan', 'turquoise', 'paleturquoise']
    explode = (0, 0, 0)
    patches, text1, text2 = plt.pie(sizes,
                                    explode=explode,
                                    labels=labels,
                                    colors=colors,
                                    autopct='%3.2f%%',
                                    shadow=False,
                                    startangle=90,
                                    pctdistance=0.6)
    plt.title('Statistics of criminal cases not containing keywords("informant" and "CI"); classification for affirmation')
    plt.axis('equal')
    plt.savefig('pie_pic/' + state + '_NKW_affirm.jpg')
    # 3
    # plt.figure(figsize=(9, 6))
    # labels = [u'remanded', u'not remanded']
    # sizes = [num_remanded, num_nonremanded]
    # colors = ['yellowgreen', 'cadetblue']
    # explode = (0, 0)
    # patches, text1, text2 = plt.pie(sizes,
    #                                 explode=explode,
    #                                 labels=labels,
    #                                 colors=colors,
    #                                 autopct='%3.2f%%',
    #                                 shadow=False,
    #                                 startangle=90,
    #                                 pctdistance=0.6)
    # plt.title('Statistics of criminal cases containing keywords("informant" and "CI"); classification for remand')
    # plt.axis('equal')
    # plt.savefig('pie_pic/KW_remand.jpg')
    # # 4
    # plt.figure(figsize=(9, 6))
    # labels = [u'remanded', u'not remanded']
    # sizes = [num_remanded_noKeywords, num_nonremanded_noKeywords]
    # colors = ['yellowgreen', 'cadetblue']
    # explode = (0, 0)
    # patches, text1, text2 = plt.pie(sizes,
    #                                 explode=explode,
    #                                 labels=labels,
    #                                 colors=colors,
    #                                 autopct='%3.2f%%',
    #                                 shadow=False,
    #                                 startangle=90,
    #                                 pctdistance=0.6)
    # plt.title('Statistics of criminal cases not containing keywords("informant" and "CI"); classification for remand')
    # plt.axis('equal')
    # plt.savefig('pie_pic/NKW_remand.jpg')

def search_keywords_ri(state, keywords):
    """
        :param: state: ma, nh, ri
        :param: keywords: a list of keywords to be searched

        cases_ma is a list of dictionary each of which represents a case
            keys: case, headnote, text

        cases_nh is a list of dictionary each of which represents a case
            keys: file name, title, type, decision, text
        """
    cases = load_cases(state)
    criminal_cases = get_criminal_cases(state, cases)

    case_pool = set([])
    cases_keywords = []

    """counting the numbers"""
    """edited by Qitong Wang; Apr 6th, 2020."""
    num_affirmed = 0
    num_part = 0
    num_reversed = 0
    num_remanded = 0
    num_nonremanded = 0

    num_affirmed_N = 0
    num_part_N = 0
    num_reversed_N = 0
    num_remanded_N = 0
    num_nonremanded_N = 0
    for i, case in enumerate(criminal_cases):
        for key in case:
            for text in case[key]:
                words = text.split(" ")
                for word in words:
                    for keyword in keywords:
                        if keyword in word.lower():
                            if i not in case_pool:
                                # print(case['decision'].lower())
                                """calculation of the classification labels"""
                                """edited by Qitong Wang; Apr 6th, 2020."""
                                if (case['decision'].lower() == 'affirmed'):
                                    num_affirmed += 1
                                if (case['decision'].lower() == 'affirm in part'):
                                    num_part += 1
                                if (case['decision'].lower() == 'not affirmed'):
                                    num_reversed += 1
                                # if ('remanded' in case['decision'].lower()):
                                #     num_remanded += 1
                                # else:
                                #     num_nonremanded += 1
                                cases_keywords.append(case)
                            case_pool.add(i)
    """calculating the total number of cases, so if we want to get cases without the number of keywords, we could minus the number of cases containing keywords"""
    """edited by Qitong Wang; Apr 6th, 2020."""
    for case in criminal_cases:
        # print(case['decision'].lower())
        if (case['decision'].lower() == 'affirmed'):
            num_affirmed_N += 1
        if (case['decision'].lower() == 'affirm in part'):
            num_part_N += 1
        if (case['decision'].lower() == 'not affirmed'):
            num_reversed_N += 1
        # if ('remanded' in case['decision'].lower()):
        #     num_remanded_N += 1
        # else:
        #     num_nonremanded_N += 1

    print(str(len(case_pool)) + " cases contain keywords")
    print(str(len(criminal_cases) - len(case_pool)) + " cases do not contain keywords")

    """show the results"""
    """edited by Qitong Wang; Apr 6th, 2020."""
    print("******************************************************")
    print('In cases containing keywords:')
    print('Affirmed case number: ' + str(num_affirmed))
    print('Partly affirmed case number: ' + str(num_part))
    print('Reversed case number: ' + str(num_reversed))
    # print("------------------------------------------------------")
    # print('Remanded case number: ' + str(num_remanded))
    # print('Nonremanded case number: ' + str(num_nonremanded))
    print("******************************************************")
    print('In cases not containing keywords:')
    print('Affirmed case number: ' + str(num_affirmed_N - num_affirmed))
    print('Partly affirmed case number: ' + str(num_part_N - num_part))
    print('Reversed case number: ' + str(num_reversed_N - num_reversed))
    # print("------------------------------------------------------")
    # print('Remanded case number: ' + str(num_remanded_N - num_remanded))
    # print('Nonremanded case number: ' + str(num_nonremanded_N - num_nonremanded))
    print("******************************************************")

    result_visualization(num_affirmed, num_part, num_reversed,
                         num_affirmed_N - num_affirmed, num_part_N - num_part, num_reversed_N - num_reversed, state)

    return cases_keywords

def search_keywords_nh(state, keywords):
    """
    :param: state: ma, nh, ri
    :param: keywords: a list of keywords to be searched

    cases_ma is a list of dictionary each of which represents a case
        keys: case, headnote, text

    cases_nh is a list of dictionary each of which represents a case
        keys: file name, title, type, decision, text
    """
    cases = load_cases(state)
    criminal_cases = get_criminal_cases(state, cases)

    case_pool = set([])
    cases_keywords = []

    """counting the numbers"""
    """edited by Qitong Wang; Apr 6th, 2020."""
    num_affirmed = 0
    num_part = 0
    num_reversed = 0
    num_remanded = 0
    num_nonremanded = 0

    num_affirmed_N = 0
    num_part_N = 0
    num_reversed_N = 0
    num_remanded_N = 0
    num_nonremanded_N = 0
    for i, case in enumerate(criminal_cases):
        for key in case:
            for text in case[key]:
                words = text.split(" ")
                for word in words:
                    for keyword in keywords:
                        if keyword in word.lower():
                            if i not in case_pool:
                                """calculation of the classification labels"""
                                """edited by Qitong Wang; Apr 6th, 2020."""
                                # if ('affirmed' in case['decision'].lower() and 'part' not in case['decision'].lower()):
                                #     num_affirmed += 1
                                # if ('part' in case['decision'].lower()):
                                #     num_part += 1
                                # if ('reversed' in case['decision'].lower() and 'part' not in case['decision'].lower()):
                                #     num_reversed += 1
                                # print(case['decision'].lower())
                                if (case['decision'].lower() == 'affirmed'):
                                    num_affirmed += 1
                                elif (case['decision'].lower() == 'affirmed in part'):
                                    num_part += 1
                                elif (case['decision'].lower() == 'not affirmed'):
                                    num_reversed += 1
                                # if ('remanded' in case['decision'].lower()):
                                #     num_remanded += 1
                                # else:
                                #     num_nonremanded += 1
                                cases_keywords.append(case)
                            case_pool.add(i)
    """calculating the total number of cases, so if we want to get cases without the number of keywords, we could minus the number of cases containing keywords"""
    """edited by Qitong Wang; Apr 6th, 2020."""
    for case in criminal_cases:
        # print(case['decision'].lower())
        if (case['decision'].lower() == 'affirmed'):
            num_affirmed_N += 1
        elif (case['decision'].lower() == 'affirmed in part'):
            num_part_N += 1
        elif (case['decision'].lower() == 'not affirmed'):
            num_reversed_N += 1
        # if ('remanded' in case['decision'].lower()):
        #     num_remanded_N += 1
        # else:
        #     num_nonremanded_N += 1

    print(str(len(case_pool)) + " cases contain keywords")
    print(str(len(criminal_cases) - len(case_pool)) + " cases do not contain keywords")

    """show the results"""
    """edited by Qitong Wang; Apr 6th, 2020."""
    print("******************************************************")
    print('In cases containing keywords:')
    print('Affirmed case number: ' + str(num_affirmed))
    print('Partly affirmed case number: ' + str(num_part))
    print('Reversed case number: ' + str(num_reversed))
    # print("------------------------------------------------------")
    # print('Remanded case number: ' + str(num_remanded))
    # print('Nonremanded case number: ' + str(num_nonremanded))
    print("******************************************************")
    print('In cases not containing keywords:')
    print('Affirmed case number: ' + str(num_affirmed_N - num_affirmed))
    print('Partly affirmed case number: ' + str(num_part_N - num_part))
    print('Reversed case number: ' + str(num_reversed_N - num_reversed))
    # print("------------------------------------------------------")
    # print('Remanded case number: ' + str(num_remanded_N - num_remanded))
    # print('Nonremanded case number: ' + str(num_nonremanded_N - num_nonremanded))
    print("******************************************************")

    result_visualization(num_affirmed, num_part, num_reversed,
                         num_affirmed_N - num_affirmed, num_part_N - num_part, num_reversed_N - num_reversed, state)

    return cases_keywords


def load_cases(state):

    path_data = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data"
    if state == "ma":
        path = [path_data + "/cases.json", path_data + "/cases_appeals.json"]
    elif state == "nh":
        path = [path_data + "/cases_nh.json"]
    elif state == "ri":
        path = [path_data + "/cases_ri.json"]

    cases = []
    for file in path:
        with open(file, 'r') as f:
            cases += json.load(f)

    print(str(len(cases))+" cases loaded")
    return cases


def get_criminal_cases(state, cases):
    criminal_cases = []
    for i, case in enumerate(cases):
        for key in case:

            if state == "ma" and key == "headnote":
                for headnote in case[key]:
                    if "Criminal" in headnote:
                        criminal_cases.append(cases[i])

            elif state == "nh" and key == "type":
                if case[key] == "criminal":
                    criminal_cases.append(cases[i])

            elif state == "ri" and key == "type":
                if case[key] == "criminal":
                    criminal_cases.append(cases[i])

    print(str(len(criminal_cases))+" criminal cases found")
    return criminal_cases


def save_result(path, fmt, cases):
    if fmt == "json":
        # write to a json file
        with open(path + '.json', 'w') as fout:
            json.dump(cases, fout)
    elif fmt == "csv":
        # write to a csv file
        keys = cases[0].keys()
        with open(path + '.csv', 'w') as fout:
            dict_writer = csv.DictWriter(fout, keys)
            dict_writer.writeheader()
            dict_writer.writerows(cases)
    else:
        print("Invalid format")


if __name__ == "__main__":

    # enter "ma", "nh" or "ri"
    # m_state = "nh"
    m_state = "ri"
    m_keywords = ["informant", "CI"]
    # m_result = "affirmed"

    if (m_state == "nh"):
        result = search_keywords_nh(m_state, m_keywords)
    else:
        result = search_keywords_ri(m_state, m_keywords)

    # save to ../data
    save_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/result/cases_" + m_state + "_result"
    # save_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/result/cases_" + m_state + "_" + m_result + "_result"
    # save as json or csv
    save_result(save_path, "json", result)



