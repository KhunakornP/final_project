import csv, os


class Csv_reader:
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

# add in code for a Database class
class Database:
    def __init__(self):
        pass
# add in code for a Table class

# modify the code in the Table class so that it supports the insert operation where an entry can be added to a list of dictionary
if __name__ == "__main__":
    print(Csv_reader("persons.csv").read())