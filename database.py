import csv, os
import copy


class csv_Reader:
    def __init__(self, name):
        self.data = []
        self.name = name

    def read(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        with open(os.path.join(__location__, self.name)) as f:
            rows = csv.DictReader(f)
            for row in rows:
                self.data.append(dict(row))
        return self.data


class Database:
    def __init__(self):
        self.database = []

    def insert(self, data):
        self.database.append(data)


# add in code for a Table class
class Table:
    def __init__(self, name, table):
        self.table_name = name
        self.table = table

    def insert(self, data):
        for item in data:
            self.table.append(item)
        return self.table

    def join(self, other_table, common_key):
        joined_table = Table(
            self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table

    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            temps.append(float(item1[aggregation_key]))
        return function(temps)

    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def update(self, index, key, value):
        self.table[index][key] = value
        return self.table

    def __str__(self):
        return self.table_name + ':' + str(self.table)


if __name__ == "__main__":
    print(csv_Reader("persons.csv").read())
    print()
    print(Table("persons", csv_Reader("persons.csv").read()))
    print()
    print(Table("persons", csv_Reader("persons.csv").read())
          .insert([{'friend': 'joe'}, {'animal' : "duck"}]))
    print()
    print(Table("persons", csv_Reader("persons.csv").read())
          .update(0,"ID", 1))

