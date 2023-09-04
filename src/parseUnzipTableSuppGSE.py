import pandas as pd
import os
import sys
import xml.etree.ElementTree as ET
import urllib.request
import time

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

table = pd.read_csv("parse_gse.txt",sep="\t")

human_cancer_list = ["GSE100337","GSE102130","GSE103224","GSE103322","GSE103591","GSE103866","GSE103867","GSE104379","GSE104406","GSE104869","GSE104985","GSE104987","GSE105142","GSE105451","GSE107646","GSE107747","GSE108378","GSE108383","GSE108394","GSE108397","GSE108699","GSE108989","GSE109308","GSE110499","GSE110626","GSE110680","GSE110686","GSE110791","GSE111014","GSE111015","GSE111065","GSE111108","GSE111360","GSE111458","GSE111672","GSE111894","GSE111896","GSE112271","GSE112274","GSE113046","GSE113099","GSE113127","GSE113196","GSE113198","GSE113336","GSE113616","GSE114161","GSE114397","GSE114459","GSE114460","GSE114461","GSE114724","GSE114725","GSE115007","GSE115032","GSE115389","GSE115501","GSE115978","GSE116254","GSE116256","GSE116481","GSE116621","GSE117156","GSE117410","GSE117450","GSE117480","GSE117599","GSE117617","GSE117618","GSE117988","GSE118056","GSE118389","GSE118704","GSE118706","GSE118828","GSE118900","GSE119139","GSE119926","GSE120145","GSE120221","GSE120575","GSE121107","GSE121309","GSE121560","GSE122582","GSE122583","GSE122703","GSE122743","GSE123139","GSE123192","GSE123476","GSE123812","GSE123813","GSE123837","GSE123902","GSE123903","GSE123904","GSE123926","GSE124898","GSE124989","GSE124992","GSE125449","GSE125449","GSE125587","GSE125881","GSE126030","GSE126068","GSE126158","GSE126906","GSE126908","GSE127266","GSE127298","GSE127471","GSE127813","GSE127888","GSE128531","GSE128822","GSE128933","GSE130001","GSE130019","GSE130020","GSE130021","GSE130022","GSE130023","GSE130024","GSE130025","GSE130346","GSE131099","GSE131135","GSE131778","GSE131882","GSE131907","GSE131928","GSE131983","GSE131984","GSE132172","GSE132257","GSE132396","GSE132465","GSE132509","GSE132566","GSE132649","GSE133022","GSE133094","GSE134269","GSE134520","GSE135437","GSE135461","GSE135564","GSE136394","GSE136805","GSE136867","GSE137026","GSE137029","GSE137391","GSE137545","GSE137912","GSE138267","GSE138418","GSE138536","GSE138693","GSE138794","GSE138892","GSE139249","GSE139324","GSE139448","GSE139829","GSE140312","GSE140430","GSE141299","GSE141832","GSE141946","GSE141982","GSE142016","GSE142116","GSE142286","GSE142750","GSE143423","GSE144357","GSE144735","GSE145165","GSE145281","GSE146221","GSE146771","GSE148190","GSE148345","GSE148842","GSE55343","GSE70630","GSE74639","GSE75688","GSE76312","GSE81383","GSE81547","GSE81812","GSE81861","GSE83142","GSE84465","GSE89567","GSE90683","GSE92432","GSE93156","GSE93562","GSE93722","GSE94979","GSE97168","GSE97679","GSE97681","GSE97693","GSE97726","GSE98638","GSE98644","GSE99254","GSE99255","GSE99305","GSE99330","GSE99795","GSE86104","GSE86103","GSE86102","GSE86101","GSE75367","GSE85183","GSE74207","GSE83533","GSE82070","GSE75384","GSE74246","GSE80297","GSE76314","GSE72056","GSE77308","GSE72631","GSE69471","GSE73121","GSE67980","GSE52717","GSE52716","GSE52715","GSE51827","GSE57872","GSE46817","GSE46805"]

# human_cancer_list = ["GSE123837","GSE102130","GSE103224","GSE103322"]


result = table[table["gseid"].isin(human_cancer_list)]


for i in result.index:
    url_str = result.loc[i,"raw"]
    if isinstance(url_str,str):
        url_group = url_str.split(",")
    else:
        continue
    for url in url_group:
        if url.endswith("RAW.tar"):
            filename = url.split("/")[-1]
            gseid = result.loc[i,"gseid"]
            print("get %s file list in RAW.tar files from website" % gseid)
            web_file = urllib.request.urlopen("https://www.ncbi.nlm.nih.gov/geo/download/?format=xml&acc=%s" % gseid)
            web_data = web_file.read().decode("utf-8")
            time.sleep(5)
            file_list = findSuppleDataXml(web_data)
            print("finished parsing infomation")
            for name in file_list:
                if name != filename:
                    print(name)
                    if "barcode" in name.lower():
                        result = merge_extract_result(result,name,i,"barcode")
                        # print(result.loc[i,"barcode"])
                    elif "count" in name.lower():
                        result = merge_extract_result(result,name,i,"count")
                        # print(result.loc[i,"count"])
                    elif "tpm" in name.lower() or "matrix" in name.lower() or "fpkm" in name.lower():
                        result = merge_extract_result(result,name,i,"tpm")
                        # print(result.loc[i,"tpm"])
                    elif "gene" in name.lower():
                        result = merge_extract_result(result,name,i,"gene")
                        # print(result.loc[i,"gene"])
                    elif "raw" in name.lower():
                        result = merge_extract_result(result,name,i,"raw")
                        # print(result.loc[i,"raw"])
                    else:
                        result = merge_extract_result(result,name,i,"other")
                        # print(result.loc[i,"other"])
        else:
            continue


# # download function
# # some series only provided bw files, and too large to download
# # so I changed to get gse from web page
# for i in result.index:
#     path = "GSE_Download/%s" % result.loc[i,"gseid"]
#     print(path)
#     url_str = result.loc[i,"raw"]
#     if isinstance(url_str,str):
#         url_group = url_str.split(",")
#         print(url_group)
#     else:
#         continue
#     try:
#         os.makedirs(path)
#     except:
#         print("%s has created!" % path)
#     for url in url_group:
#         if url.endswith("tar"):
#             filename = url.split("/")[-1]
#             os.system("wget %s -O %s/%s" % (url, path, filename))
#             print("finish download")
#             print("extracting")
#             os.system("cd %s; tar xvf %s; cd ../.." % (path,filename))
#             file_list = os.listdir(path)
#             print(file_list)
#             for name in file_list:
#                 if name != filename:
#                     print(name)
#                     if "barcode" in name.lower():
#                         result = merge_extract_result(result,name,i,"barcode")
#                         print(result.loc[i,"barcode"])
#                     elif "count" in name.lower():
#                         result = merge_extract_result(result,name,i,"count")
#                         print(result.loc[i,"count"])
#                     elif "tpm" in name.lower() or "matrix" in name.lower():
#                         result = merge_extract_result(result,name,i,"tpm")
#                         print(result.loc[i,"tpm"])
#                     elif "gene" in name.lower():
#                         result = merge_extract_result(result,name,i,"gene")
#                         print(result.loc[i,"gene"])
#                     elif "raw" in name.lower():
#                         result = merge_extract_result(result,name,i,"raw")
#                         print(result.loc[i,"raw"])
#                     else:
#                         result = merge_extract_result(result,name,i,"other")
#                         print(result.loc[i,"other"])
#         else:
#             continue



result.to_csv("single_cell_supplementary_file_after_extraction.txt", index=None, sep="\t")
            
    