from find_yz import Getter_files

t = Getter_files(path_dir=r"Data\dos_file", suffix="")
for x in t.search_files():
    print(x)
