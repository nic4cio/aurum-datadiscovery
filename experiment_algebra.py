from main import init_system
from api.apiutils import Relation
from collections import namedtuple
from algebra import API, DRS

api, reporting = init_system("./test/testmodel/", create_reporting=False)

# help(api)

drs0 = api.search_table(kw='banklist', max_results=10)
drs1 = api.search_content(kw='New City Bank', max_results=10)
drs2 = api.content_similar_to(drs0)
drs3 = api.content_similar_to(drs1)
drs4 = api.search_table(kw='forbes-global', max_results=10)
drs5 = api.content_similar_to(drs4)
drs6 = api.schema_similar_to(drs4)
drs7 = api.search_table(kw='banklist2', max_results=10)
drs8 = api.intersection(a=drs0, b=drs7)
drs9 = api.intersection(a=drs0, b=drs4)


print(str(drs0.__dict__()))

# print("\nnext result...")
# print(str(drs1.__dict__()))

# print("\nnext result...")
# print(str(drs2.__dict__()))

# print(str(drs3.__dict__()))

# print(str(drs4.__dict__()))

# print(str(drs5.__dict__()))

# print(str(drs6.__dict__()))

# print(str(drs7.__dict__()))
# print(str(drs8.__dict__()))
# print(str(drs9.__dict__()))