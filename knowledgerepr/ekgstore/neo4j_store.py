from neo4j import GraphDatabase
from tqdm import tqdm
import sys
import os

script_dir = os.path.dirname(__file__)
api_dir = os.path.join( script_dir, '..','..','api')
sys.path.append(api_dir)

knowledgerepr_dir = os.path.join( script_dir, '..','..')
sys.path.append(knowledgerepr_dir)
#for p in sys.path:
#    print(p)
# from api.apiutils import Relation 
from apiutils import Relation 
from knowledgerepr import fieldnetwork


class Neo4jExporter(object):
    def __init__(self,
                 host='localhost',
                 port=7687,
                 user="neo4j",
                 pwd="aurumaurum"):
        self._server = "bolt://{}:{}".format(host, port) #python3.5 format
        self._user = user
        self._pwd = pwd

        self._driver = GraphDatabase.driver(self._server, auth=(user, pwd))

    def export(self, path_to_model):
        field_network = fieldnetwork.deserialize_network(path_to_model)
        #print(field_network.__dict__)
        #print(dir(field_network))

        # Create index to speed up MATCHes
        with self._driver.session() as session:
            # session.run("CREATE INDEX ON :Node(nid)") # <- 
            session.run("CREATE INDEX FOR (n:Node) ON (n.nid)") # neo4j newr version syntax
        test_relation_label = Relation.SCHEMA
        relation_hits = list(field_network.enumerate_relation(test_relation_label, as_str=True))
        print("Test Relation Hits for {}: {}".format(test_relation_label, relation_hits))

        
        for relation_label in Relation:
            # print(relation_label)

            # relation_hits is a generator. We could consume it to a list and then iterate over it,
            # but this would probably consume too much memory in most scenarios
            relation_hits = list(field_network.enumerate_relation(relation_label, as_str=True))
            print("Relation Hits for {}: {}".format(relation_label, relation_hits))  # Log the hits

            
            for a, b in tqdm(relation_hits, desc="Storing {} relations to Neo4j".format(relation_label), unit='relation'): #python3.5 supported syntax
            

                # 1. Transaction Handling
                #Neo4j queries should ideally be handled in transactions to ensure consistency. 
                #Each session.run() creates a new session and may not properly link the nodes and relationships. 
                # You can try bundling queries in transactions:
                with self._driver.session() as session:
                    # Step 1: add nodes
                    with session.begin_transaction() as tx:
                        tx.run("CREATE (n:Node {nid:$nid,db_name:$db_name,source:$source,field:$field,score:$score}) RETURN id(n)",
                            nid=a.nid, db_name=a.db_name, source=a.source_name, field=a.field_name, score=a.score)
                        tx.run("CREATE (n:Node {nid:$nid,db_name:$db_name,source:$source,field:$field,score:$score}) RETURN id(n)",
                            nid=b.nid, db_name=b.db_name, source=b.source_name, field=b.field_name, score=b.score)

                        tx.run(
                            "MATCH (a:Node),(b:Node) "
                            "WHERE a.nid=$nid_a AND b.nid=$nid_b "
                            "CREATE (a)-[r:{relation_label}]->(b) RETURN type(r)".format(
                                relation_label=str(relation_label).replace('Relation.', '')),
                            nid_a=a.nid, nid_b=b.nid)
                        tx.commit()
            
if __name__ == '__main__':
    exporter = Neo4jExporter()
    exporter.export("../../test/testmodel/")
    
