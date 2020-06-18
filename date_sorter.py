import pandas as pd
import numpy as np

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
print(df.shape)
df.head(10)

dates_df = pd.DataFrame(df.copy())

monthDict = {'Apr': 4, 'Aug': 8, 'Dec': 12, 'Feb': 2, 'Jan': 1, 'Jul': 7, 'Jun': 6,
             'Mar': 3, 'May': 5, 'Nov': 11, 'Oct': 10, 'Sep': 9, 'Apr.': 4, 'Aug.': 8,
             'Dec.': 12, 'Feb.': 2, 'Jan.': 1, 'Jul.': 7, 'Jun.': 6, 'Mar.': 3,
             'May': 5, 'Nov.': 11, 'Oct.': 10, 'Sep.': 9, 'April': 4, 'August': 8,
             'December': 12, 'February': 2, 'January': 1, 'July': 7, 'June': 6, 'March': 3,
             'May': 5, 'November': 11, 'October': 10, 'September': 9}

# 04/20/2009; 04/20/09; 4/20/09; 4/3/09
pattern = r'(?P<month>\d{1,2})[-/](?P<day>\d{1,2})[-/](?P<year>\d{2,4})'
first = dates_df.iloc[:, 0].str.extract(pattern)
first.dropna(inplace=True)

# Mar-20-2009; Mar 20, 2009; March 20, 2009; Mar. 20, 2009; Mar 20 2009;
pattern = r'(?P<month>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*).?[ -]{1}(?P<day>\d{1,2}),?[ -]{1}(?P<year>\d{2,4})'
second = dates_df.iloc[:, 0].str.extract(pattern)
second.month = second.month.map(monthDict)
second.dropna(inplace=True)

# 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
pattern = r'(?P<day>\d{1,2}) (?P<month>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*).?,? (?P<year>\d{2,4})'
third = dates_df.iloc[:, 0].str.extract(pattern)
third.month = third.month.map(monthDict)
third.dropna(inplace=True)

# Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
pattern = r'(?P<month>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*).? (?P<day>\d{1,2})[a-z]*,? (?P<year>\d{2,4})'
forth = dates_df.iloc[:, 0].str.extract(pattern)
forth.month = forth.month.map(monthDict)
forth.dropna(inplace=True)

# Feb 2009; Sep 2009; Oct 2010
pattern = r'(?P<day>)(?P<month>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*).? (?P<year>\d{2,4})'
fifth = dates_df.iloc[:, 0].str.extract(pattern)
fifth.month = fifth.month.map(monthDict)
fifth.day = 1
fifth.dropna(inplace=True)

# 6/2008; 12/2009
pattern = r'(?P<day>)(?P<month>\d{1,2})[/|,|.|-](?P<year>[1|2]\d{3})'
sixth = dates_df.iloc[:, 0].str.extract(pattern)
sixth.day = 1
sixth.dropna(inplace=True)

# 2009; 2010
pattern = r'(?P<month>)(?P<day>)(?P<year>[1|2]\d{3})'
seventh = dates_df.iloc[:, 0].str.extract(pattern)
seventh.dropna(inplace=True)
seventh.month = 1
seventh.day = 1

# Adding Date column
subsets = [first, second, third, forth, fifth, sixth, seventh]

dates_df['date'] = np.nan
for sub in subsets:
    sub['date'] = pd.to_datetime(
        sub.month.astype('int').astype('str').str.zfill(2) + sub.day.astype('str').str.zfill(2) + sub.year.astype(
            'str').str[-2:])
    dates_df['date'][dates_df['date'].isnull()] = sub['date']

# Correct Ordering
answer = pd.Series(dates_df[['date']].sort_values(by='date').index, index=dates_df.index)