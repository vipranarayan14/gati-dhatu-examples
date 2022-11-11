import json
import csv


def get_data(file_path):
    with open(file_path) as file:
        data = json.load(file)
        return data


def extract_gati_dhatus(dhatus):
    gati_dhatus = []

    for dhatu in dhatus:
        if "गतौ" in dhatu["artha"]:
            gati_dhatus.append(dhatu)

    return gati_dhatus


def extract_examples(dhatus, prayogas):
    examples = []

    for dhatu in dhatus:
        baseindex = dhatu["baseindex"]

        empty_prayoga = {"": [{"book": "", "num": "", "text": "", "external": ""}]}

        prayoga = prayogas.get(baseindex, empty_prayoga) or empty_prayoga

        # if not prayoga:
        #     print(dhatu["i"])

        for word in prayoga.values():
            for ref in word:
                examples.append(
                    {
                        "id": dhatu["baseindex"],
                        "dhatu": dhatu["dhatu"],
                        "aupadeshik": dhatu["aupadeshik"],
                        "artha": dhatu["artha"],
                        "gana": dhatu["gana"],
                        "karma": dhatu["karma"],
                        "text": ref["text"],
                        "ref": f'{ref["book"]} {ref["num"]}' if ref["book"] else "",
                    }
                )

    return examples


def write_examples(output_file_path, examples):
    with open(output_file_path, "w") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=examples[0].keys())

        writer.writeheader()
        writer.writerows(examples)


data_file_path = "dhatu/data.txt"
dhatuprayogas_file_path = "dhatu/dhatuprayogas.txt"
output_file_path = "gati_dhatu_examples.csv"

dhatus = get_data(data_file_path)["data"]
prayogas = get_data(dhatuprayogas_file_path)
gati_dhatus = extract_gati_dhatus(dhatus)
examples = extract_examples(gati_dhatus, prayogas)

write_examples(output_file_path, examples)
