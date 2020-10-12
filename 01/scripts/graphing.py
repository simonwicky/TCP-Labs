import pandas as pd
import os

def load_pings():
    df = pd.DataFrame(columns=['time','source', 'dest', 'N', 'topo'])

    files = [f for f in os.listdir('./') if f.endswith('.txt')]
    for file in files:
        pc1, pc2, N, topo, _ = file.replace('.', '-').split('-')
        df2 = pd.read_csv(file, header=None)
        df2['source'] = pc1
        df2['dest'] = pc2
        df2['N'] = int(N)
        df2['topo'] = topo
        df2.columns = ['time', 'source','dest', 'N', 'topo']
        df2['time'] = df2['time'].apply(lambda x: x.split('time=')[1])
        df2['time'] = pd.to_timedelta(df2['time'])
        df = df.append(df2)
    print(df)


"main Function: This is called when the Python file is run"
if __name__ == '__main__':
    load_pings()