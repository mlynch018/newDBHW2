import pandas as pd
import time

def hashSearch(hash_table, df):
    start_time = time.time()
    h = hash("Sandman: Dream Hunters 30th Anniversary Edition")
    h_index = hash_table[h]
    record = df.iloc[h_index]
    end_time = time.time()
    search_time = end_time - start_time
    return search_time, record

def createHash(df):
    hash_table = {}
    for index,row in df.iterrows():
        h = hash(row['title'])
        hash_table[h] = index
    return hash_table

def linearSearch(sorted_table):
    start_time = time.time()
    record = None
    for index,row in sorted_table.iterrows():
        if(row['title'] == "Sandman: Dream Hunters 30th Anniversary Edition"):
            record = row
            break

    end_time = time.time()
    search_time = end_time - start_time
    return search_time, record

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
        temp_df = mergeTables(dfs[0], dfs[1])
        dfs.pop(0)
        dfs.pop(0)
        dfs.append(temp_df)
    return dfs[0]

def main():
    files = ['dataset' + str(i+1) + '.csv' for i in range(12)]
    #sorted_table = mergeSort(files)

    dfs = [pd.read_csv(file) for file in files]
    df = pd.concat(dfs)
    sorted_table = df.sort_values(by='title', kind='mergesort')

    linear_search_time, linear_record = linearSearch(sorted_table)
    print(linear_search_time)
    print(linear_record)
    print('\n\n')

    hash_table = createHash(sorted_table)

    hash_search_time, hash_record = hashSearch(hash_table, sorted_table)
    print(hash_search_time)
    print(hash_record)

if __name__ == "__main__":
    main()
