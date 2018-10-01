import pandas as pd
from namu.models import User

df = pd.read_csv('name_import.csv')
for index, row in df.iterrows():
    u = User(name=row['name'], is_active=True)
    u.save()
