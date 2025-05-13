import pandas as pd
from datetime import datetime
import pickle5 as pickle
import os

def scale(data):
    df = data
    for index in df.index:
        consum1 = df.loc[index , "PowerConsumption1"]
        consum2 = df.loc[index , "PowerConsumption2"]
        consum3 = df.loc[index , "PowerConsumption3"]
        consum1 = int(round(consum1 , -1))
        consum2 = int(round(consum2 , -1))
        consum3 = int(round(consum3 , -1))
        df.loc[index , "PowerConsumption1"] = consum1
        df.loc[index , "PowerConsumption2"] = consum2
        df.loc[index , "PowerConsumption3"] = consum3
    return df

def read_data(df):
    df = scale(df)
    df.sort_values(by=["Timestamp"])
    tmp = []
    for index in df.index:
        try:
            tmp.append(datetime.fromisoformat(str(df.loc[index , "Timestamp"])))
        except:
            print("time-format-error")
    df["time_formate"] = tmp
    time_pattern = []
    hour = []
    for i in df.index:
        pre = str(df.loc[i,"time_formate"].hour)
        post = str(df.loc[i,"time_formate"].minute)
        second = str(int(int((int(df.loc[i,"time_formate"].second))/10))*10)
        tmp1 = str(int(int((int(df.loc[i,"time_formate"].minute))/15))*15)
        if tmp1 == "0":
            hour.append( str(df.loc[i,"time_formate"].hour) + ":" + "00")
        else:
            hour.append( str(df.loc[i,"time_formate"].hour) + ":" + tmp1)
        for min in range(10):
            if post == str(min):
                post = "0{}".format(min)
                break
        tmp = post
        time_pattern.append(tmp)
    df["time_pattern"] = time_pattern
    df["hour"] = hour
    return df


def create_pattern(data , id):
    pattern_table = pd.DataFrame(columns=data["time_pattern"].unique())
    tmp = []
    for i in data.index:
        first_time = str(data.loc[i,"time_pattern"])
        tmp.append(data.loc[i,"PowerConsumption{}".format(id)])
        if (i+1) in data.index:
            if data.loc[i+1,"time_pattern"] != first_time:
                #transition.append(set(tmp))
                if str(set(tmp)) in pattern_table.index:
                    pattern_table.loc[str(set(tmp)),first_time] += 1
                else:
                    tmp_table = pd.DataFrame(0 ,index=[str(set(tmp))],columns=pattern_table.columns)
                    pattern_table = pattern_table.append(tmp_table)
                    pattern_table.loc[str(set(tmp)),first_time] += 1
                tmp = []
        else:
            if str(set(tmp)) in pattern_table.index:
                pattern_table.loc[str(set(tmp)),first_time] += 1
            else:
                tmp_table = pd.DataFrame(0 ,index=[str(set(tmp))],columns=pattern_table.columns)
                pattern_table = pattern_table.append(tmp_table)
                pattern_table.loc[str(set(tmp)),first_time] += 1
            tmp = []
    return pattern_table


def create_sim(table , frequency_table):
    pattern_table = table
    for period in pattern_table.columns:
        count = 0
        for pattern in pattern_table.index:
            if pattern in frequency_table.index: #pattern in the frequency_table !
                """ fill the slot """
                if pattern_table.loc[pattern,period] == 1:  #pattern appear !
                    max = frequency_table.loc[pattern,period]
                    ind = list(frequency_table.index).index(pattern)
                    col = list(frequency_table.columns).index(period)
                    for index in range(1,7):
                        if max < frequency_table.iloc[ind,col - index]:
                            max = frequency_table.iloc[ind,col - index]
                        if max < frequency_table.iloc[ind,(col + index)%len(frequency_table.columns)]:
                            max = frequency_table.iloc[ind,(col + index)%len(frequency_table.columns)]
                    pattern_table.loc[pattern,period] = max
                else: # pattern_table_0926.loc[i,j] == 0
                    pattern_table.loc[pattern,period] = 0
            else: #pattern doesn't in the pattern table
                pattern_table.loc[pattern,period] = 0
            count += 1
            if count == 12:
                count = 0
    return pattern_table


def create_warning(sim_table):
    count = 0
    times = 0
    max_num = 0
    for i in sim_table.columns:
        for j in sim_table.index:
            if max_num < sim_table.loc[j,i]:
                max_num = sim_table.loc[j,i]
            count += sim_table.loc[j,i]
        times += 1
        if times % 15 == 14 :
            return count / 15


def create_score(min_15_data , frequency , level , id):
    df = read_data(min_15_data)
    pattern = create_pattern(df , id)
    pattern = create_sim(pattern , frequency)
    score = create_warning(pattern)
    return score <= level


def detection(min_15_data, level = "med"):
    ans = []
    with open(f'{os.environ.get("TABLE_PATH")}frequency_table1.pke', 'rb') as f:
        frequency_table1 = pickle.load(f)
    with open(f'{os.environ.get("TABLE_PATH")}frequency_table2.pke', 'rb') as f:
        frequency_table2 = pickle.load(f)
    with open(f'{os.environ.get("TABLE_PATH")}frequency_table3.pke', 'rb') as f:
        frequency_table3 = pickle.load(f)

    tmp = {"low": 0.2 , "med": 0.4 , "high": 0.5}
    con1 = create_score(min_15_data, frequency_table1 , tmp[level] , 1)
    con2 = create_score(min_15_data , frequency_table2 , tmp[level] , 2)
    con3 = create_score(min_15_data, frequency_table3 , tmp[level] , 3)
    ans.append(con1)
    ans.append(con2)
    ans.append(con3)
    return ans
