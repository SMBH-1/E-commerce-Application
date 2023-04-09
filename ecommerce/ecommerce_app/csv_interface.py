import csv

class CSV_Interface:

    def __init__(self, filename):
        
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            self.column_names = reader.fieldnames

        self.filename = filename
        self.update_data_from_file()

    @property
    def all_data(self):
        self.update_data_from_file()
        return self.__all_data

    @all_data.setter
    def all_data(self, val):
        self.__all_data = val


    # read data from the file 
    # update the all_data list
    # return the new list
    def update_data_from_file(self):
        
        data = []
        with open(self.filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)

        self.__all_data = data
        return self.__all_data

    # append a singular row to a CSV file
    def append_one_row_to_file(self, new_data_dict):

        with open(self.filename, "a", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.column_names)
            writer.writerow(new_data_dict)

        return self.all_data

    # rewrite the csv file with new data 
    def write_all_rows_to_file(self, data_rows):

        with open(self.filename, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.column_names)
            writer.writeheader()
            writer.writerows(data_rows)

        self.update_data_from_file()
        return self.all_data

    # delete a record of data 
    # -- Takes in a dictionary record, 
    # -- removes that record from the list of all_data
    # -- writes the new list to the file
    # -- updates the all_data list
    def remove_a_row(self, dictionary_of_data_to_be_removed):
        
        self.all_data.remove(dictionary_of_data_to_be_removed)
        self.write_all_rows_to_file(self.__all_data)
        
        self.update_data_from_file()

        return self.all_data