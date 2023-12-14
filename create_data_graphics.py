from utils import read_data_from_json, write_data_to_json
from tqdm import tqdm
def align_characters(a, b):
    result_b = []
    for i,item_a in enumerate(tqdm(a, desc='converting')):
        # Find the corresponding item in b based on fort attribute
        matching_items_b = [item_b for item_b in b
                            if item_b.get("character") == item_a["fort"]]
        matching_items_b[0]["image_id"] = "{:04d}".format(i+1)
        # Append the first matching item (if any) to the result lists
        if matching_items_b:
            result_b.append(matching_items_b[0])

    return result_b


fort = read_data_from_json("fort_annotation.json")
graphics = read_data_from_json("graphics.json")
new_graphics = align_characters(fort,graphics)
write_data_to_json("data_graphics.json", new_graphics)
