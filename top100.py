import json
import psychopg2
from collections import defaultdict

excluded_card_ids = [-1, 42, 175, 1, 84, 14] # ? id and all basic lands

def main():
    top_100 = get_top_100()
    with open('mydata/top100.json', 'w') as f:
        json.dump(top_100, f)
    
def get_top_100():
    with open('data/cubes.json') as f:
        with open('data/indexToOracleMap.json') as f2, open('data/simpleCardDict.json') as f3:
            cubes = json.load(f)
            oracle_map = json.load(f2)
            card_dict = json.load(f3)

            counts = defaultdict(int)
            for cube in cubes:
                for card_index in cube['cards']:
                    if card_index not in excluded_card_ids:
                        counts[card_index] += 1

            top_100 = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:100]

            res = []
            for tup in top_100:
                print(tup)
                oracle_id = oracle_map[str(tup[0])]
                card = card_dict[oracle_id]
                card["count"] = tup[1]
                res.append(card)
                print(card)

            return res












if __name__ == '__main__':
    main()
