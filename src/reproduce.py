"""Later review implementation; not historical employer code."""
from pathlib import Path
import argparse
import ast
import json
import sqlite3
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

def dealer_demo():
    # Grain is dealer x month. Aggregate transactions BEFORE joining the dimension.
    sales = pd.DataFrame({'dealer':['D01','D01','D02','D03'],
                          'month':['2025-01']*4,'units':[2,3,4,1]})
    dim = pd.DataFrame({'dealer':['D01','D02'],'city':['City A','City B']})
    totals=sales.groupby(['dealer','month'],as_index=False).units.sum()
    joined=totals.merge(dim,on='dealer',how='left',validate='many_to_one',indicator=True)
    assert joined.units.sum()==sales.units.sum() and len(joined)==len(totals)
    with sqlite3.connect(':memory:') as con:
        sales.to_sql('sales',con,index=False);dim.to_sql('dealers',con,index=False)
        sql=pd.read_sql_query('''WITH s AS (SELECT dealer, month, SUM(units) AS units
          FROM sales GROUP BY dealer, month)
          SELECT s.*,d.city FROM s LEFT JOIN dealers d ON s.dealer=d.dealer
          ORDER BY s.dealer''',con)
    assert sql.units.sum()==sales.units.sum()
    try:
        totals.merge(pd.concat([dim,dim.iloc[:1]]),on='dealer',validate='many_to_one')
    except pd.errors.MergeError:
        duplicate_rejected=True
    else: raise AssertionError('Duplicate dimension key was not rejected')
    return {'synthetic':True,'raw_rows':len(sales),'joined_rows':len(joined),
            'units_preserved':int(joined.units.sum()),'unmatched_dealers':int((joined._merge=='left_only').sum()),
            'duplicate_key_rejected':duplicate_rejected,'sql_matches_pandas':True}
if __name__ == '__main__':
    print(json.dumps(dealer_demo(),indent=2))
