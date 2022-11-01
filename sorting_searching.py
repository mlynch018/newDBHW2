# Programmer: Midori Lynch
# CS 5300 HW 2 Merge-sort, linear search, and hash 

import pandas as pd
import time

def hashSearch(table, df):
    initial_time = time.time()
    h = hash("Sandman: Dream Hunters 30th Anniversary Edition")
    hash_i = table[h]
    row = df.iloc[hash_i]
    final_time = time.time()
    actual_time = final_time - initial_time
    return actual_time, row

def createTable(df):
    table = {}
    for index,row in df.iterrows():
        h = hash(row['title'])
        table[h] = index
    return table

def linearSearch(sorted_table):
    initial_time = time.time()
    row = None
    for index,row in sorted_table.iterrows():
        if(row['title'] == "Sandman: Dream Hunters 30th Anniversary Edition"):
            row = row
            break
    final_time = time.time()
    actual_time = final_time - initial_time
    return actual_time, row

def mergeTables(df1, df2):
    df = pd.DataFrame(columns=list(df1.columns))
    d1g = df1.iterrows()
    d2g = df2.iterrows()
    t1 = next(d1g)[1]
    t2 = next(d2g)[1]

    while(1):
        if(t1['title'] < t2['title']):
            try:
                df = pd.concat([df, t1.to_frame().T], ignore_index=True)
                t1 = next(d1g)[1]
            except StopIteration as e:
                while(1):
                    try:
                        df = pd.concat([df, t2.to_frame().T], ignore_index=True)
                        t2 = next(d2g)[1]
                    except StopIteration as e:
                        break
                break
        else:
            try:
                df = pd.concat([df, t2.to_frame().T], ignore_index=True)
                t2 = next(d2g)[1]
            except StopIteration as e:
                while(1):
                    try:
                        df = pd.concat([df, t1.to_frame().T], ignore_index=True)
                        t1 = next(d1g)[1]
                    except StopIteration as e:
                        break
                break
    return df

def mergeSort(files):
    dfs = []
    for file in files:
        dfs.append(pd.read_csv(file).sort_values(by='title', kind='mergesort'))
    while(len(dfs) > 1):
        temp = mergeTables(dfs[0], dfs[1])
        dfs.pop(0)
        dfs.pop(0)
        dfs.append(temp)
    return dfs[0]

def main():
    files = ['dataset' + str(i+1) + '.csv' for i in range(12)]
    
    #real world merge sort, takes hours to run
    #sorted_table = mergeSort(files)
    #modeled merge sort
    dfs = [pd.read_csv(file) for file in files]
    df = pd.concat(dfs)
    sorted_table = df.sort_values(by='title', kind='mergesort')

    linear_search_time, linear_row = linearSearch(sorted_table)
    print(linear_search_time)
    print(linear_row)
    print('\n\n')

    table = createTable(sorted_table)
    hash_search_time, hash_row = hashSearch(table, sorted_table)
    print(hash_search_time)
    print(hash_row)

if __name__ == "__main__":
    main()
