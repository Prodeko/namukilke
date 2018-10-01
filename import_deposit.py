import pandas as pd
import csv
from namu.models import Deposit, User

#df = pd.read_csv('deposit_import.csv')
#for index, row in df.iterrows():
#    d = Deposit(user=User.objects.get(pk=row['id']), amount=row['deposit'])
#    d.save()

with open('deposit_import.csv') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        d = Deposit(user=User.objects.get(pk=row[0]), amount=row[2])
        d.save()
