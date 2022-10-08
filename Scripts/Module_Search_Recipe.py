import Module_Input_Parametrs
from Module_GUI import *
from Module_Input_Parametrs import id_rawmat_oil, dict_of_equip, sql_quarry


def search_recipe(id_prod_fun, requirements_fun, sql_quarry_fun, amount_fun, type_work_fun, mother_key):
    """The purpose of this function is to fill in the "Scheme_process" dictionary
        in order to build a scheme based on it."""
    Scheme_process = Module_Input_Parametrs.Scheme_process
    Scheme_rawmat = Module_Input_Parametrs.Scheme_rawmat
    dict_of_sur = Module_Input_Parametrs.dict_of_sur
    Seq_key = Module_Input_Parametrs.Seq_key

    append_to_dict_of_amount(int(id_prod_fun), round(amount_fun, 2))
    try:
        """For raw materials, sulfuric acid, plastic and rubber, a special order is defined, the recursion is exited"""
        if id_prod_fun in id_rawmat_oil:
            if id_prod_fun == 43 or id_prod_fun == 44:
                Seq_key.append(Seq_key[-1] + 1)
                if type_work_fun == 1:
                    Scheme_process[int(Seq_key[-1])] = [mother_key, int(id_prod_fun) * -1,
                                                        amount_fun, 'sur', 0, id_prod_fun, 6]
                else:
                    Scheme_process[int(Seq_key[-1])] = [mother_key, int(id_prod_fun) * -1,
                                                        amount_fun, 'MJ', 0, id_prod_fun, 6]
                dict_of_equip[6][0] = True
                return
            if id_prod_fun == 76:
                Seq_key.append(Seq_key[-1] + 1)
                if type_work_fun == 1:
                    process_multiply = 5
                    k_amount = get_k_amount(amount_fun, process_multiply)
                    Scheme_process[Seq_key[-1]] = [mother_key, 141, amount_fun,
                                                   'surplus: ' + str(k_amount * 5 - int(amount_fun)), 0, 76, 6]
                    mother_key = Seq_key[-1]
                    Seq_key.append(Seq_key[-1] + 1)
                    Scheme_process[Seq_key[-1]] = [mother_key, -6, k_amount * process_multiply, 0, 0, 6, 0]
                    Seq_key.append(Seq_key[-1] + 1)
                    Scheme_process[Seq_key[-1]] = [mother_key, -1, k_amount * process_multiply, 0, 0, 1, 0]
                else:
                    process_multiply = 50
                    k_amount = get_k_amount_per_min(amount_fun, 5, 6)
                    Scheme_process[Seq_key[-1]] = [mother_key, 141, round(amount_fun, 3), str(round(k_amount * 50)) + 'MJ', 0, 76,
                                                   6]
                    mother_key = Seq_key[-1]
                    Seq_key.append(Seq_key[-1] + 1)
                    Scheme_process[Seq_key[-1]] = [mother_key, -6, round(k_amount * process_multiply, 3), 0, 0, 6, 0]
                    Seq_key.append(Seq_key[-1] + 1)
                    Scheme_process[Seq_key[-1]] = [mother_key, -1, round(k_amount * process_multiply, 3), 0, 0, 1, 0]
                Scheme_rawmat[6] += k_amount * process_multiply
                Scheme_rawmat[1] += k_amount * process_multiply
                append_to_dict_of_amount(6, Scheme_process[Seq_key[-2]][2])
                append_to_dict_of_amount(1, Scheme_process[Seq_key[-1]][2])
                dict_of_equip[6][0] = True
                return
            if 1 <= int(id_prod_fun) <= 12:
                Seq_key.append(Seq_key[-1] + 1)
                Scheme_process[Seq_key[-1]] = [mother_key, id_prod_fun * (-1), round(amount_fun, 3), 0, 0,
                                               int(id_prod_fun), 0]
                Scheme_rawmat[int(id_prod_fun)] += round(amount_fun, 3)
                return
    except TypeError:
        return
    cursor = satisfactory_db.cursor()
    id_search_recipes = cursor.execute(sql_quarry_fun[1], {'Id_Prod': id_prod_fun}).fetchall()
    """Choosing the optimal recipe"""
    if len(id_search_recipes) == 1:
        best_id_recipe = int(str(id_search_recipes).translate({ord(iterat): None for iterat in '[](),'}))
    else:
        max_recipe_points = 0
        for id_recipe in id_search_recipes:
            id_recipe = int(id_recipe[0])
            analysis = cursor.execute(sql_quarry_fun[2], {'Id': id_recipe}).fetchone()
            recipe_points = analysis_recipe(analysis, requirements_fun, id_prod_fun)
            if max_recipe_points == 0 or recipe_points < max_recipe_points:
                max_recipe_points = recipe_points
                best_id_recipe = int(analysis[1])

    """Filling out the dictionary"""
    input_ID = cursor.execute(sql_quarry[3], [best_id_recipe]).fetchone()

    Seq_key.append(Seq_key[-1] + 1)
    if type_work_fun == 1:
        # k_amount = get_k_amount(amount_fun, input_ID[7])
        surplus_fun = append_to_dict_of_surplus(id_prod_fun)
        amount_surplus = amount_fun - surplus_fun
        k_amount_surplus = get_k_amount(amount_surplus, input_ID[7])
        dict_of_sur[id_prod_fun] = k_amount_surplus * input_ID[7] - amount_surplus

        Scheme_process[int(Seq_key[-1])] = [mother_key, best_id_recipe, amount_fun, 'sur_' + str(amount_surplus),
                                            0, id_prod_fun, int(input_ID[-1])]

        if input_ID[2] is not None:
            Scheme_process[int(Seq_key[-1])][4] = input_ID[2]

    else:
        k_amount = get_k_amount_per_min(amount_fun, input_ID[7], input_ID[-2])
        Scheme_process[int(Seq_key[-1])] = [mother_key, best_id_recipe, round(amount_fun, 6),
                                            'MJ', 0, id_prod_fun, int(input_ID[-1])]
        if input_ID[2] is not None:
            Scheme_process[int(Seq_key[-1])][4] = input_ID[2]

    dict_of_equip[Scheme_process[int(Seq_key[-1])][6]][0] = True

    """Formation of a new round of recursion"""
    mother_key = Seq_key[-1]
    cursor.close()

    for ind in range(3, 7):
        if input_ID[ind] is None:
            return
        if type_work_fun == 1:
            amount_input = k_amount_surplus * int(input_ID[ind + 6])
        else:
            amount_input = k_amount * (60 * input_ID[ind + 6] / input_ID[-2])
        search_recipe(input_ID[ind], requirements_fun, sql_quarry, amount_input, type_work_fun, mother_key=mother_key)


def get_k_amount_per_min(amount_fun, amount_output, circle_time):
    """The coefficient that allows you to find out the number of products per minute. Mode: 'Automated'."""
    prod_per_min = 60 * amount_output / circle_time
    k_amount = amount_fun / prod_per_min
    return k_amount


def get_k_amount(amount_fun, amount_output):

    """The coefficient that allows you to find out the number of products. Mode: 'Handicraft'."""

    if int(amount_fun) % int(amount_output) == 0:
        k_amount = int(amount_fun) // int(amount_output)
    else:
        k_amount = int(amount_fun) // int(amount_output) + 1
    return k_amount


def append_to_dict_of_amount(id_prod_fun, amount_input_fun):

    """Summation of products with the same ID"""

    Scheme_process_gen_amt = Module_Input_Parametrs.Scheme_process_gen_amt
    if id_prod_fun not in Scheme_process_gen_amt:
        Scheme_process_gen_amt[int(id_prod_fun)] = round(amount_input_fun, 2)
    else:
        Scheme_process_gen_amt[int(id_prod_fun)] = round(amount_input_fun + Scheme_process_gen_amt[int(id_prod_fun)], 2)


def append_to_dict_of_surplus(id_prod_fun):

    """Calculation of the remaining products for the mode 'Handicraft'"""

    dict_of_sur = Module_Input_Parametrs.dict_of_sur
    if id_prod_fun not in dict_of_sur:
        dict_of_sur[id_prod_fun] = 0
        surplus_fun = int(dict_of_sur[id_prod_fun])
        return surplus_fun
    else:
        surplus_fun = int(dict_of_sur[id_prod_fun])
        return surplus_fun


def analysis_recipe(analysis_fun, requirements_fun, id_prod_fun):
    """The recipe selection algorithm is based on a set of points. Each type of resource has its own score: iron has the lowest, uranium has the highest. Points depend on the type of resource, on the level of consumption and on the effectiveness of the recipe.

    For iron ingots, copper ingots, caterium ingots, concrete, quartz crystals and silica determined at consumption level 0 a different algorithm is assigned
    """
    points_of_mat = {1: 1, 2: 3, 3: 1, 4: 2, 5: 7, 6: 4, 7: 4, 8: 5, 9: 6, 10: 8, 11: 9}

    if id_prod_fun in (13, 19, 23, 53, 55, 56):
        #  {id_prod: (index_requirements, id_recipe)}
        dict_of_cheap_mat = {13: (1, 1), 19: (2, 19), 23: (3, 29), 53: (7, 95), 55: (8, 99), 56: (8, 101)}
        if requirements_fun[dict_of_cheap_mat[id_prod_fun][0]] == 0:
            return 1

    k_dominance = int(analysis_fun[15]) * 1000 / 2
    recipe_points_fun = k_dominance
    for ind in range(1, 12):
        if requirements_fun[ind] == 0:
            recipe_points_fun += 1 * int(analysis_fun[ind + 1]) * points_of_mat[ind]
        elif requirements_fun[ind] == 1:
            recipe_points_fun += 10 * int(analysis_fun[ind + 1]) * points_of_mat[ind]
        elif requirements_fun[ind] == 2:
            recipe_points_fun += 100 * int(analysis_fun[ind + 1]) * points_of_mat[ind]
        elif requirements_fun[ind] == 3:
            recipe_points_fun += 1000 * int(analysis_fun[ind + 1]) * points_of_mat[ind]
    return recipe_points_fun


def oil_prod(id_prod_oil_fun, amount_oil_fun, requirements_oil_fun, type_work_oil_fun):
    """The formation scheme for the production of plastic and rubber is somewhat different from the rest. Depends on 'Oil Level'.
       The scheme will be built manually according to the given parameters (this is due to the infinite recursion)"""
    Scheme_rawmat = Module_Input_Parametrs.Scheme_rawmat
    if type_work_oil_fun == 1:
        if requirements_oil_fun == 0:
            process_multiply = 2
            k = get_k_amount(int(amount_oil_fun), process_multiply)
            Scheme_process_oil = str(0) + '_' + str(k) + '_' + str(process_multiply)
            Scheme_rawmat[7] += k * 3

        elif requirements_oil_fun == 1:
            process_multiply = 12
            k = get_k_amount(int(amount_oil_fun), process_multiply)
            Scheme_process_oil = str(1) + '_' + str(k) + '_' + str(process_multiply)
            if id_prod_oil_fun == 43:
                Scheme_rawmat[1] += k * 12
            else:
                Scheme_rawmat[1] += k * 6
            Scheme_rawmat[7] += k * 9

        elif requirements_oil_fun == 2 and id_prod_oil_fun == 43:
            process_multiply = 18
            k = get_k_amount(int(amount_oil_fun), process_multiply)
            # Seq_key.append(Seq_key[-1] + 1)
            Scheme_process_oil = str(2) + '_' + str(k) + '_' + str(process_multiply)
            Scheme_rawmat[1] += k * 12
            Scheme_rawmat[7] += k * 9

        else:
            # requirements_oil_fun == 3 or id_prod_oil_fun == 44:
            process_multiply = 54
            k = get_k_amount(int(amount_oil_fun), process_multiply)
            # Seq_key.append(Seq_key[-1] + 1)
            Scheme_process_oil = str(3) + '_' + str(k) + '_' + str(process_multiply)
            Scheme_rawmat[1] += k * 60
            Scheme_rawmat[7] += k * 18
        # append_to_dict_of_amount(id_prod_oil_fun * -1, k * process_multiply)

    else:
        k = amount_oil_fun
        if requirements_oil_fun == 0:
            Scheme_process_oil = str(0) + '_' + str(k / 2) + '_' + str(0)
            Scheme_rawmat[7] += round(k / 2 * 3, 3)
        elif requirements_oil_fun == 1:
            Scheme_process_oil = str(1) + '_' + str(k/12) + '_' + str(0)
            if id_prod_oil_fun == 43:
                Scheme_rawmat[1] += k
                Scheme_rawmat[7] += round(3 * k / 4, 3)
            else:
                Scheme_rawmat[1] += round(k / 2, 3)
                Scheme_rawmat[7] += round(3 * k / 4, 3)

        elif requirements_oil_fun == 2 and id_prod_oil_fun == 43:
            # [pl, pl, refinery, rub,refinery, pl-, rub_rubber, refinery, refinery_fuel, blender_fuel, MJ]
            Scheme_process_oil = str(2) + '_' + str(k/18) + '_' + str(0)
            Scheme_rawmat[1] += round(4 * k / 3, 3)
            Scheme_rawmat[7] += round(k / 2, 3)
        elif requirements_oil_fun == 3 or id_prod_oil_fun == 44:
            Scheme_process_oil = str(3) + '_' + str(k/54) + '_' + str(0)
            Scheme_rawmat[1] += round(10 * k / 9, 3)
            Scheme_rawmat[7] += round(k / 3, 3)
        # append_to_dict_of_amount(id_prod_oil_fun * -1, k)
    return Scheme_process_oil


