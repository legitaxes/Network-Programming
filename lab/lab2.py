### GLOBAL VARIABLES
FILENAME = 'lab-deliverables/score2.txt'


### FUNCTIONS
def read_file(file_path):
    data_dict = {}
    with open(file_path, 'r') as f:
        # for each row in the file, store the data into a list
        # store the first name and last name combined from the data as the dictionary key
        # store the value as the dictionary value
        for line in f:
            data = line.strip().split()
            if data[2] + ' ' + data[3] in data_dict:
                # check if the name is already in the dictionary, add to existing value if it exists
                data_dict[data[2] + ' ' + data[3]] += int(data[4])
            else:
                # if the name is not in the dictionary, add the name as the key and the value as the value
                data_dict[data[2] + ' ' + data[3]] = int(data[4])
        
        return data_dict
    

### MAIN
def main():
    dictionary_data = read_file(FILENAME)
    # iterate the dictionary and print the key and value
    for key, value in dictionary_data.items():
        print(key, value)

    # sort dictionary by value
    new_dictionary_data = sorted(dictionary_data.items(), key=lambda x:x[1])
    # print(new_dictionary_data)
    
    print(f"Based on the sorted dictionary, the student with the highest score is: {new_dictionary_data[-1][0]} with a score of: {new_dictionary_data[-1][1]} \nAND {new_dictionary_data[-2][0]} with a score of: {new_dictionary_data[-2][1]}")
    ### Kristina Larsson with a score of: 37
    ### AND Maria Johansson with a score of: 37

if __name__ == '__main__':
    main()