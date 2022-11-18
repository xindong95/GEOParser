#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   DcClass.py
@Time    :   2022/11/09 15:35:19
@Author  :   Xin Dong
@Contact :   xindong9511@gmail.com
@License :   (C)Copyright 2020-2022, XinDong
'''

import pandas as pd
import numpy as np


class DCModel:

    def __init__(self, path):
        self.df = pd.read_csv(path, sep='\t')
        self.name = self.df['name'].tolist()
        self.all_name = self.df['name'].tolist() + self.aliases()

    def __len__(self):
        return self.df.__len__()

    def names(self):
        return self.name

    def aliases(self):
        al = []
        for i in self.df['aliases'].unique():
            if not pd.isna(i):
                al += i.split('|')
        return al

    def has(self, name):
        if name in self.all_names:
            return True
        else:
            return False

    def find(self, keyword):
        # fuzzy match
        r_n = self.df[self.df['name'].str.find(keyword) == 0]
        r_a = self.df[self.df['aliases'].str.find(keyword) == 0]
        if r_n.__len__() != 0:
            return r_n['name'].values[0]
        elif r_a.__len__() != 0:
            return r_a['name'].values[0]
        else:
            return None

    def find_exact(self, keyword):
        # exact match
        r_n = self.df[self.df['name'] == keyword]
        r_a = self.df[self.df['aliases'] == keyword]
        if r_n.__len__() != 0:
            return r_n['name'].values[0]
        elif r_a.__len__() != 0:
            return r_a['name'].values[0]
        else:
            return None

    def add(self, name, status='new', comment=np.nan, aliases=np.nan):
        self.df = self.df.append({'name': str(name),
                                  'status': status,
                                  'comment': comment,
                                  'aliases': aliases
                                  }, ignore_index=True).copy()

    def to_csv(self, path):
        self.df.to_csv(path, sep='\t', index=False)


class DCJournal:

    def __init__(self, path):
        self.df = pd.read_csv(path, sep='\t')
        self.name = self.df['name'].tolist()

    def __len__(self):
        return self.df.__len__()

    def names(self):
        return self.name

    def has(self, name):
        if name in self.name:
            return True
        else:
            return False

    def find(self, keyword):
        # fuzzy match
        r_n = self.df[self.df['name'].str.find(keyword) == 0]
        if r_n.__len__() != 0:
            return r_n['name'].values[0]
        else:
            return None
        
    def find_exact(self, keyword):
        # exact match
        r_n = self.df[self.df['name'] == keyword]
        if r_n.__len__() != 0:
            return r_n['name'].values[0]
        else:
            return None

    def add(self, name, issn=np.nan, impact_factor=np.nan):
        self.df = self.df.append({'name': str(name),
                                  'issn': issn,
                                  'impact_factor': impact_factor
                                  }, ignore_index=True).copy()
    
    def to_csv(self, path):
        self.df.to_csv(path, sep='\t', index=False)


class DCPaper:

    def __init__(self, path):
        self.df = pd.read_csv(path, sep='\t')
        self.pmid = self.df['pmid'].tolist()

    def __len__(self):
        return self.df.__len__()

    def has(self, pmid):
        if pmid in self.pmid:
            return True
        else:
            return False

#     def find(self, keyword):
#         # fuzzy match
#         r_n = self.df[self.df['name'].str.find(keyword) == 0]
#         if r_n.__len__() != 0:
#             return r_n['name'].values[0]
#         else:
#             return None

    def find_exact(self, keyword):
        # exact match
        r_n = self.df[self.df['pmid'] == keyword]
        if r_n.__len__() != 0:
            return list(r_n.T.to_dict().items())[0][1]
        else:
            return None

    def add(self, pmid=np.nan, unique_id=np.nan, title=np.nan,
            reference=np.nan, abstract=np.nan, pub_date=np.nan,
            collect_date=np.nan, authors=np.nan, last_auth_email=np.nan,
            journal=np.nan, status='new', lab=np.nan,
            pub_summary=np.nan, comment=np.nan):
        self.df = self.df.append({'pmid': str(pmid),
                                  'unique_id': unique_id,
                                  'title': title,
                                  'reference': reference,
                                  'abstract': abstract,
                                  'pub_date': pub_date,
                                  'collect_date': collect_date,
                                  'authors': authors,
                                  'last_auth_email': last_auth_email,
                                  'journal': journal,
                                  'status': status,
                                  'lab': lab,
                                  'pub_summary': pub_summary,
                                  'comment': comment,
                                  }, ignore_index=True).copy()

    def to_csv(self, path):
        self.df.to_csv(path, sep='\t', index=False)
 
 
