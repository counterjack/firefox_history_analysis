import os
import shutil
import sqlite3
import matplotlib.pyplot as plt

from typing import List, Tuple, Dict
import platform


def get_operating_system_name() -> str:
    """
    Returns:
        str -- [Name of the operating system]
    'Linux`: Ubuntu
    'Darwin`: Mac
    """
    platform_name:str = platform.system()
    return platform_name

def get_history_file_path() -> str:
    """
    This function returns the path to the file places.sqlite based on the 
    operating systems.

    Returns:
        str -- [path to places.sqlite file]
    """
    system_name = get_operating_system_name()

    if system_name == "Darwin": # For mac os
        base_path = os.path.expanduser("~")+"/Library/Application Support/Firefox/Profiles/"
        # get the dir ending with .default-release extension
        search_extension = ".default-release"
    elif system_name == "Linux":
        base_path = os.path.expanduser("~") + "/.mozilla/firefox/"
        # get the dir ending with .default
        search_extension = "default"

    _all_items = os.listdir(base_path)
    required_dir = list(filter(lambda x: x.endswith(search_extension), _all_items))
    final_path = base_path + f"{required_dir[0]}"
    # since, this file will be used by firefox, so sqlite will be locked to operate
    # so we will make a copy and return that
    src_file = final_path + "/places.sqlite"
    dest_file = final_path + "/places_copy.sqlite"
    shutil.copyfile(src_file, dest_file)
    return dest_file


def analyse(results: Dict) -> None:
    plt.bar(range(len(results)), list(results.values()))
    plt.xlabel("urls",fontsize=8)
    plt.ylabel("visits", fontsize=8)
    plt.title("Urls with total number of visits")

    y_axis = list(results.values())
    x_axis = list(results.keys())
    colors = ["red", "yellow"]
    for i in range(len(x_axis)):
        plt.text(
            x=i-0.5, y=y_axis[i],
            s=f"({x_axis[i]},  {y_axis[i]} )",
            fontsize=5,
            bbox=dict(facecolor=colors[i%2], alpha=0.5, )
            )
    plt.show()


history_db = get_history_file_path()
c = sqlite3.connect(history_db)
cursor = c.cursor()

select_statement: str = "select url, visit_count from moz_places order by visit_count desc;"
cursor.execute(select_statement)
results: List[Tuple] = cursor.fetchall()[:10]

sites_count_sorted_dict: Dict = {item[0]: item[1] for item in results}
analyse(sites_count_sorted_dict)

"""
select_moz_input_history_statement = "select * from moz_origins";
cursor.execute(select_moz_input_history_statement)
history_results = cursor.fetchall()
for history in history_results:
    print ("History %", history)

"""



