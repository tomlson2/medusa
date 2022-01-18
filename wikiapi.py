import requests
import pandas as pd

class Price:

    def __init__(self):
        r = requests.get("https://prices.runescape.wiki/api/v1/osrs/5m")

        df = pd.read_json(r.text)
        mapping_df = pd.read_json('ge/mapping.json')

        avgHighPrice = [d.get('avgHighPrice') for d in df.data]
        avgLowPrice = [e.get('avgLowPrice') for e in df.data]
        avgPrice = [int((int(b if a is None else a) + int(a if b is None else b)) / 2) for a, b in zip(avgHighPrice,avgLowPrice)]

        df['avgHighPrice'] = avgHighPrice
        df['avgLowPrice'] = avgLowPrice
        df['data'] = avgPrice

        df.reset_index(inplace=True)
        df = df.rename(columns = {'index' : 'id'})
        df.drop('timestamp', axis=1, inplace=True)

        mapping_df = mapping_df[['id','name']]

        df = pd.merge(df, mapping_df, on=['id'], how='inner')

        self.df = df

    def load_price(self, item_name : str):
        item_row = self.df.loc[self.df['name'] == item_name]
        price = item_row.iloc[-1]['data']
        return price
