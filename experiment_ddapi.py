from main import init_system
from api.apiutils import Relation
from collections import namedtuple
from ddapi import API, DRS

api, reporting = init_system("./test/testmodel/", create_reporting=False)

table = "imdb_top_1000.csv"
table_drs = api.drs_from_table(table)

keyword_to_be_searched = "Titanic 666"
ncb_search = api.keyword_search(keyword_to_be_searched)
#for res in ncb_search:
#    print(res)

content_similar = api.similar_content_to(table_drs)
for res in content_similar:
    print(res)

schema_similar = api.similar_schema_name_to(table_drs)
#for res in schema_similar:
#    print(res)

pkfk_tab = api.pkfk_table(table_drs)
#for res in pkfk_tab:
#    print(res)

pkfk_campo = api.pkfk_field(("csv_repository","imdb_top_1000.csv","Meta_score"))
#for res in pkfk_campo:
#    print(res)

keyword_to_be_searched2 = "Vintage"
tbg_search = api.keyword_search(keyword_to_be_searched2)
#for el in tbg_search:
#    print(str(el))

res_inter = ncb_search.intersection(tbg_search)
#for el in res_inter:
#    print(str(el))

# print("--*--")

keyword_to_be_searched3 = "Royal Bank of Canada"
rbcan_search = api.keyword_search(keyword_to_be_searched3)
#for el in rbcan_search:
#    print(str(el))

res2_inter = ncb_search.intersection(rbcan_search)
#for el in res2_inter:
#    print(str(el))

# print("--*--")

# table intersection

#table2 = "forbes-global.csv"
#table2_drs = api.drs_from_table(table2)
#for el in table2_drs:
#    print(el)

#tables_inter = table_drs.intersection(table2_drs)
#for el in tables_inter:
#    print(el)

#similar_res = api.similar_content_to(table2_drs)
#print("Similar content to {}".format(table2))
#for el in similar_res:
#    print(el)

similar_table = api.similar_content_to_table(table)
#for el in similar_table:
#    print(el)

similar_schema_name_table = api.similar_schema_name_to_table(table)
#for el in similar_schema_name_table:
#    print(el)

#source_name = "csv_repository"
#keyword_to_be_searched4 = "lero"
#exception error to be treated when keyword for filed does not match the table
#similar_content_field = api.similar_content_to_field((source_name,"banklist.csv", keyword_to_be_searched4))
#for el in similar_content_field:
#    print(el)


