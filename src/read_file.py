import sys
import glob


def read_folder(file_list):
    master_list = []
    for file in file_list:
        dba_list, id_list = read_file(file)
        master_list.append((dba_list, id_list))
    return master_list

def read_file(filename):
    """
    docstring
    """ 
    id_list = []
    dba_list = []
    with open(filename, 'r')as file:
        for idx, line in enumerate(file):
            if idx != 0:
                if 'NAN' in line:
                    dba_list.append(line.split(',')[-1].strip())
                    id_list.append('NAN')
                elif 'object' in line:
                    dba_list.append(line.split(",")[-1].strip())
                else:
                    id_list.append(line.split(',')[1].split(" ")[-1].strip())

    return dba_list, id_list

def write_file(master_list):

    """
    docstring
    """

    with open('master_id.csv', 'w', encoding="utf8") as file:
        file.write(u'DBA,fousquare_id\n')
        for element in master_list:
            for dba, id_name in zip(element[0], element[1]):
                print(dba, id_name)
                file.write(u'{},{}\n'.format(dba, id_name))

def main():
    """
    docstring
    """
    file_list = glob.glob('data/master/*.csv')
    master_list = read_folder(file_list)
    write_file(master_list)


if __name__ == '__main__':
    main()
