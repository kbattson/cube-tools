import psycopg2
from collections import defaultdict
import json
import os

DB_URL = os.environ.get("DATABASE_URL")

def get_similarity(target_id):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute("SELECT * FROM cubes WHERE id = %s", (target_id,))
    target_cube = cur.fetchone()
    target_set = set(target_cube[1])

    cur.execute("SELECT * FROM cubes")
    all_cubes = cur.fetchall()

    res = []
    for cube in all_cubes:
        curr_set = set(cube[1])
        jaccard = len(target_set & curr_set) / len(target_set | curr_set)
        res.append((jaccard, cube[0]))

    cur.close()
    conn.close()

    return sorted(res, key=lambda x: x[0], reverse=True)

def get_recs(target_id):
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM cubes WHERE id = %s", (target_id,))
            target_cube = cur.fetchone()
            target_set = set(target_cube[1])

            sim = get_similarity(target_id)            
            
            top_100 = []
            for i in range(100):
                cur.execute("SELECT * FROM cubes WHERE id = %s", (sim[i][1],))
                card_list = cur.fetchone()[1]
                top_100.append((sim[i][0], card_list))
                
            scores = defaultdict(float)
            for jaccard, card_list in top_100:
                for card in card_list:
                    if card not in target_set:
                        scores[card] += jaccard
                        
            top_card_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)

            with open("data/indexToOracleMap.json") as f1:
                with open("data/simpleCardDict.json") as f2:
                    oracle_map = json.load(f1)
                    card_dict = json.load(f2)

                    res = []
                    for id, score in top_card_ids:
                        card_info = card_dict[oracle_map[str(id)]]
                        res.append((card_info, score))

                    return res

def get_recs_sql(target_id):
    with open("data/indexToOracleMap.json") as f1:
        oracle_map = json.load(f1)
    with open("data/simpleCardDict.json") as f2:
        card_dict = json.load(f2)

    with (psycopg2.connect(DB_URL)) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT cards FROM cubes WHERE id = %s", (target_id,))
            target_cards = set(cur.fetchone()[0])

            cur.execute("""
               SELECT c.id, c.cards,
                   cardinality(c.cards & target.cards)::float / cardinality(c.cards | target.cards) AS jaccard
                FROM cubes c, (SELECT cards FROM cubes WHERE id = %s) AS target
                WHERE c.id != %s
                ORDER BY jaccard DESC
                LIMIT 100
            """, (target_id, target_id))

            top_100 = cur.fetchall()

            scores = defaultdict(float)
            for cube_id, card_list, jaccard in top_100:
                for card in card_list:
                    if card not in target_cards:
                        scores[card] += jaccard

            top_card_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)

            res = []
            for card_id, score in top_card_ids:
                oracle_id = oracle_map.get(str(card_id))
                if oracle_id and oracle_id in card_dict:
                    res.append((card_dict[oracle_id], score))
            return res
                    
            

                    
                

if __name__ == "__main__":
    print(get_recs_sql("4b903895-7f8f-45d4-8fb8-978021e17c8e"))
    # print(get_similarity("4b903895-7f8f-45d4-8fb8-978021e17c8e"))
    # print(get_recs("4b903895-7f8f-45d4-8fb8-978021e17c8e"))
