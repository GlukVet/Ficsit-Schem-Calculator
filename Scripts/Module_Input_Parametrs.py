import sqlite3


try:
    satisfactory_db = sqlite3.connect('Satisfactory_DB.db')
    print("SQLite connection open")
except sqlite3.Error as error:
    print("Error connecting to sqlite", error)
    satisfactory_db.close()


sql_quarry_1 = "SELECT id_recipe FROM recipes WHERE id_prod = :Id_Prod"
sql_quarry_2 = "SELECT * FROM quick_analys WHERE id_recipe = :Id ORDER BY priority_use"
sql_quarry_3 = "SELECT * FROM Recipes WHERE id_recipe = ?"

sql_quarry = {1: sql_quarry_1, 2: sql_quarry_2, 3: sql_quarry_3}
points_of_mat = {1: 1, 2: 3, 3: 1, 4: 2, 5: 7, 6: 4, 7: 4, 8: 5, 9: 6, 10: 8, 11: 9}
id_rawmat_oil = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 43, 44, 76, 8)
Seq_key = [-1]
Scheme_process = {}
Scheme_process_gen_amt = {}
dict_of_sur = {}
Scheme_rawmat = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
dict_of_color = {0: '"gray"', 1: '"deepskyblue"', 2: '"deeppink"', 3: '"green2"', 4: '"firebrick1"',
                 6: '"darkorchid1"', 7: '"darkslategray2"', 8: '"lightcoral"', 9: '"darkgoldenrod2"',
                 10: '"aquamarine"', 11: '"aquamarine"', 12: '"khaki1"'}
dict_of_color_raw_mat = {1: '"blue"', 2: '"brown4"', 3: '"crimson"', 4: '"tan"', 5: '"azure4"', 6: '"yellow"',
                         7: '"x11purple"', 8: '"gold"', 9: '"violet"', 10: '"tomato1"', 11: '"gray"',
                         12: '"springgreen2"'}
list_of_repeat = []
MJ_Total = [0]

list_of_exception_key = []
dict_of_check_key = {}

total_img = None

dict_of_equip = {1: [False, 'Constructor'], 2: [False, 'Smelter'], 3: [False, 'Assembler'],
                 4: [False, 'Foundry'],
                 6: [False, 'Refinery'], 7: [False, 'Packager'], 8: [False, 'Manufacturer'],
                 9: [False, 'Blender'],
                 10: [False, 'Particle Accelerator'], 11: [False, 'Particle Accelerator'],
                 12: [False, 'Nuclear Power Plant']}