#!/usr/bin/python

import pandas as pd
import os
import sys
import xml.etree.ElementTree as ET
import urllib.request
import time
import re
import gzip


def merge_extract_result(result_table, name, index, col):
    ori_value = result_table.loc[index, col]
    result = result_table.copy()
    if isinstance(ori_value,str):
        result.loc[index,col] = ori_value + ",[RAW]%s" % name
    else:
        result.loc[index,col] = "[RAW]%s" % name
    return result

def findSuppleDataXml(xml):
    root = ET.fromstring(xml)
    file_list = []
    for file in root.iter('file'):
        filename = file.text.strip()
        file_list.append(filename)
    return file_list

parser_result_table = "/fs/home/dongxin/Projects/parser/single_cell/parse_gse.txt"
folder = "20210829_collection"
series_list = ['GSE145410', 'GSE139495', 'GSE154778']
table = pd.read_csv(parser_result_table, sep="\t")
result = table[table["gseid"].isin(series_list)]

# download function
# some series only provided bw files, and too large to download
# so I changed to get gse from web page
for i in result.index:
    gseid = result.loc[i,"gseid"]
    path = "%s/%s" % (folder,gseid)
    print(path)
    url_list = result.loc[i,:].tolist()
    url_group = []
    for url_str in url_list:
        if isinstance(url_str,str):
            url_item = url_str.split(",")
            url_group = url_group + url_item
        else:
            continue
    url_group = url_group[1:]
    print(url_group)
    try:
        os.makedirs(path)
    except:
        print("%s has created!" % path)
    for url in url_group:
        filename = url.split("/")[-1]
        if not os.path.exists("%s/%s" %  (path, filename)):
            os.system("wget %s -O %s/%s" % (url, path, filename))
            print("finish download")
        else:
            print("file existed!")
    # download series matrix
    id_cut = gseid.__len__() - 3
    series_matrix_link = "https://ftp.ncbi.nlm.nih.gov/geo/series/%snnn/%s/matrix/%s_series_matrix.txt.gz" % (gseid[0:id_cut],gseid,gseid)
    series_matrix_name = series_matrix_link.split("/")[-1]
    if not os.path.exists("%s/%s" % (path, series_matrix_name)):
        os.system("wget %s -O %s/%s" % (series_matrix_link, path, series_matrix_name))
    try:
        filesize = os.path.getsize("%s/%s" % (path, series_matrix_name))
        if filesize == 0:
            os.system("rm %s/%s" % (path, series_matrix_link.split("/")[-1]))
            page_url = 'https://ftp.ncbi.nlm.nih.gov/geo/series/%snnn/%s/matrix/' % (gseid[0:id_cut],gseid)
            html = urllib.request.urlopen(page_url).read().decode('utf-8')
            link_group = re.compile(r'<a href=".*series_matrix\.txt\.gz"').findall(html)
            for link in link_group:
                series_matrix_name = link.rstrip('"').lstrip('<a href="')
                os.system("wget %s%s -O %s/%s" % (page_url, series_matrix_name, path, series_matrix_name))
    except:
        # in case no file
        time.sleep(10)
        page_url = 'https://ftp.ncbi.nlm.nih.gov/geo/series/%snnn/%s/matrix/' % (gseid[0:id_cut],gseid)
        html = urllib.request.urlopen(page_url).read().decode('utf-8')
        link_group = re.compile(r'<a href=".*series_matrix\.txt\.gz"').findall(html)
        for link in link_group:
            series_matrix_name = link.rstrip('"').lstrip('<a href="')
            os.system("wget %s%s -O %s/%s" % (page_url, series_matrix_name, path, series_matrix_name))
    with open('%s/genome_build.txt' % folder, 'a+') as build_file:
        with gzip.open('%s/%s' % (path, series_matrix_name), 'rb') as f:
            file_content = f.read()
            if b'hg38' in file_content or b'GRCh38' in file_content:
                build_version = 'hg38'
            if b'hg19' in file_content or b'GRCh37' in file_content:
                build_version = 'hg19'
            build_file.write('%s\t%s\n' % (gseid, build_version))



# result.to_csv("single_cell_supplementary_file_after_extraction.txt", index=None, sep="\t")
            
    
