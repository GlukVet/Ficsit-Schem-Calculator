import graphviz

import Module_Input_Parametrs
from Module_Search_Recipe import oil_prod, get_k_amount, get_k_amount_per_min
from Module_Input_Parametrs import satisfactory_db, dict_of_color, dict_of_color_raw_mat


def energy_node_label():

    """single node label 'Energy' """

    MJ_Total = Module_Input_Parametrs.MJ_Total
    label_fun = '<<TABLE border="0" cellpadding="5"><TR><TD><IMG SCALE="true" SRC="icons/Energy.png"/></TD></TR>' \
                '<TR><TD border="1" STYLE="rounded" BGCOLOR="darkorange1">' \
                'Total Energy:<BR/>' + str(round(MJ_Total[0])) + '  MJ</TD></TR></TABLE>>'
    return label_fun


def bauxite_process_cluster(key_start_fun):

    """Defines the processing of bauxite"""

    Scheme_process = Module_Input_Parametrs.Scheme_process
    list_of_bau = [key_start_fun]
    key_fun = key_start_fun + 1
    print(key_fun)
    while True:
        try:
            if Scheme_process[key_fun][0] in list_of_bau:
                list_of_bau.append(key_fun)
                key_fun += 1
                continue
            else:
                key_finish_fun = key_fun
                list_of_bau.clear()
                return key_finish_fun
        except KeyError:
            key_finish_fun = key_fun
            list_of_bau.clear()
            return key_finish_fun


def edge_label_not_oil(amount_fun, color_fun, adv='', image=False, id_prod_fun=0):
    cursor = satisfactory_db.cursor()
    sql_answer = cursor.execute('SELECT image FROM Raw_mat_and_products WHERE id_rmp = :id_prod',
                                {'id_prod': id_prod_fun}).fetchone()
    cursor.close()
    if image is False:
        label_fun = '<<TABLE border="0"><TR><TD PORT="in" FIXEDSIZE="true"  WIDTH="20" HEIGHT="20"><IMG SCALE="TRUE" SRC="' \
                    + str(sql_answer[0]) + '"/>' \
                    '</TD><TD BGCOLOR=' + str(color_fun) + ' STYLE="rounded">' \
                    + str(amount_fun) + str(adv) + \
                    '</TD><TD PORT="out" FIXEDSIZE="true"  WIDTH="1" HEIGHT="1"></TD></TR></TABLE>>'
        return label_fun
    else:
        label_str_1 = '<<TABLE border="0" cellpadding="2">'
        label_str_2 = '<TR><TD width="45" height="15" fixedsize="true" border="1" style="rounded" BGCOLOR= ' \
                      + str(color_fun) + '><FONT face="Comic Sans MS">' + str(amount_fun) + '</FONT></TD></TR>'
        label_str_3 = '<TR><TD cellpadding="5" width="30" height="30" fixedsize="true" border="1" style="rounded" ' \
                      'port="here"><IMG SCALE="TRUE" SRC="' + str(sql_answer[0]) + '"/></TD></TR></TABLE>>'
        label_fun = label_str_1 + label_str_2 + label_str_3
        return label_fun


def edge_label(ind_fun, adv=''):

    """Label for small intermediate nodes (just for fuel)"""

    label_fun = '<<TABLE border="0"><TR><TD PORT="in" FIXEDSIZE="true"  WIDTH="1">' \
                '</TD><TD STYLE="rounded" BGCOLOR="orange">' + str(ind_fun) + str(adv) + \
                '</TD><TD PORT="out" FIXEDSIZE="true"  WIDTH="1"></TD></TR></TABLE>>'
    return label_fun


def label_construct_oil(oil_product_fun, oil_amount_fun, type_work_fun, surplus_fun, MJ_fun, name_recipe_fun):

    """Label for small intermediate nodes (not for fuel)"""

    MJ_Total = Module_Input_Parametrs.MJ_Total
    # type_work_fun is TRUE ===> type work is amount
    sql_quarry_prod = 'SELECT image FROM Raw_mat_and_products WHERE id_rmp = :id_prod'

    cursor = satisfactory_db.cursor()
    sql_answer = cursor.execute(sql_quarry_prod, {'id_prod': oil_product_fun}).fetchone()
    cursor.close()

    # ================================================ LABEL CONSTRUCT CODE ============================================

    label_str_1 = '<<TABLE border="0" cellpadding="2">'
    if type_work_fun == 2:
        oil_amount_fun = round(oil_amount_fun, 2)
    if oil_product_fun == 7 or oil_amount_fun == 1:
        label_str_2 = '<TR><TD width="60" height="15" fixedsize="true" border="1" style="rounded">' \
                      '<FONT face="Comic Sans MS, bold"><U>' + str(oil_amount_fun) + '</U></FONT></TD></TR>'
    else:
        label_str_2 = '<TR><TD width="60" height="15" fixedsize="true" border="1" bgcolor="darkorchid1" ' \
                      'style="rounded"><FONT face="Comic Sans MS">' + str(oil_amount_fun - surplus_fun) + \
                      '</FONT></TD></TR>'

    label_str_3 = '<TR><TD cellpadding="5" width="60" height="60" fixedsize="true" border="1" style="rounded" ' \
                  'port="here"><IMG SCALE="true" SRC="' + str(sql_answer[0]) + '"/></TD></TR>'

    if surplus_fun != 0 and type_work_fun == 1:
        label_str_4 = '<TR><TD width="60" height="15" fixedsize="true" border="1" style="rounded">' + \
                      'surplus: ' + str(surplus_fun) + '</TD></TR>'
    elif type_work_fun == 2 and MJ_fun == 'by':
        label_str_4 = '<TR><TD width="60" height="15" fixedsize="true" border="1" style="rounded">' + \
                      str('by-product') + '</TD></TR>'
    elif type_work_fun == 2 and MJ_fun != 0:
        MJ_Total[0] += MJ_fun
        label_str_4 = '<TR><TD width="60" height="15" fixedsize="true" border="1" style="rounded">' + \
                      str(round(MJ_fun, 2)) + ' MJ</TD></TR>'
    else:
        label_str_4 = ''

    if oil_product_fun == 7 or oil_product_fun == 1:
        label_str_5 = '</TABLE>>'
    else:
        label_str_5 = '<TR><TD border="1" style="rounded">' \
                      '<FONT point-size="6">' + str(name_recipe_fun) + '</FONT></TD></TR></TABLE>>'

    label_oil_fun = label_str_1 + label_str_2 + label_str_3 + label_str_4 + label_str_5
    return label_oil_fun


def label_construct_raw_mat(id_raw_mat_fun, amount_fun):

    """Label for nodes in the cluster 'Raw Materials' """

    sql_quarry_prod = 'SELECT image, name FROM Raw_mat_and_products WHERE id_rmp = :id_prod'

    cursor = satisfactory_db.cursor()
    sql_answer = cursor.execute(sql_quarry_prod, {'id_prod': id_raw_mat_fun}).fetchone()
    cursor.close()

    # ================================================ LABEL CONSTRUCT CODE ============================================

    label_str_1 = '<<TABLE border="0" cellpadding="2">'
    label_str_2 = '<TR><TD width="60" height="15" fixedsize="true" border="1" style="rounded">' \
                  '<FONT face="Comic Sans MS, bold"><U>' + str(round(amount_fun, 2)) + '</U></FONT></TD></TR>'
    label_str_3 = '<TR><TD cellpadding="5" width="60" height="60" fixedsize="true" border="1" style="rounded" ' \
                  'port="here"><IMG SCALE="true" SRC="' + str(sql_answer[0]) + '"/></TD></TR>'
    if int(id_raw_mat_fun) != 11 and int(id_raw_mat_fun) != 8:
        label_str_4 = '<TR><TD width="60" height="15" fixedsize="true" ' \
                      'border="1" style="rounded">' + str(sql_answer[1]).replace('_', ' ') + '</TD></TR></TABLE>>'
    else:
        label_str_4 = '<TR><TD width="60" height="15" fixedsize="true" ' \
                      'border="1" style="rounded"><FONT point-size="9">' + str(sql_answer[1]).replace('_', ' ') + \
                      '</FONT></TD></TR></TABLE>>'

    label_fun = label_str_1 + label_str_2 + label_str_3 + label_str_4
    return label_fun


def label_construct_waste(recipe_id, prod_amount, waste_id, type_fun):

    """Label for nodes with waste product """

    sql_quarry_image = 'SELECT image FROM Raw_mat_and_products WHERE id_rmp = :id_waste'
    sql_quarry_data = 'SELECT output_prod, output_waste, circle_duration FROM Recipes WHERE id_recipe = :recipe_id'

    cursor = satisfactory_db.cursor()
    image = cursor.execute(sql_quarry_image, {'id_waste': waste_id}).fetchone()
    data = cursor.execute(sql_quarry_data, {'recipe_id': recipe_id}).fetchone()
    cursor.close()

    if str(type_fun).count('MJ') > 0:
        waste_amount = round((prod_amount / (60 * data[0] / data[2])) * (60 * data[1] / data[2]), 2)
    else:
        waste_amount = int(get_k_amount(prod_amount, data[0]) * data[1])

    # ================================================ LABEL CONSTRUCT CODE ============================================

    label_str_1 = '<<TABLE border="0" cellpadding="2">'
    label_str_2 = '<TR><TD width="60" height="15" fixedsize="true" border="1" bgcolor=' \
                  + str(dict_of_color[12]) + ' style="rounded">' \
                                             '<FONT face="Comic Sans MS">' + str(waste_amount) + '</FONT></TD></TR>'
    label_str_3 = '<TR><TD cellpadding="5" width="60" height="60" fixedsize="true" border="1" style="rounded" ' \
                  'port="here"><IMG SCALE="true" SRC="' + str(image[0]) + '"/></TD></TR>'
    label_str_4 = '<TR><TD width="60" height="15" fixedsize="true" ' \
                  'border="1" style="rounded">by-product</TD></TR></TABLE>>'

    label_fun = label_str_1 + label_str_2 + label_str_3 + label_str_4
    return label_fun


def label_construct_mj(id_eq_fun, amount_prod_fun, out_prod_fun, circle_dur_fun, is_cluster=False):

    """Calculation of power consumption for a node"""

    MJ_Total = Module_Input_Parametrs.MJ_Total
    cursor = satisfactory_db.cursor()
    k_mj = cursor.execute('SELECT MJ FROM Equipment WHERE id_equip = :id_eq_fun', {'id_eq_fun': id_eq_fun}).fetchone()
    cursor.close()
    mj = round((float(amount_prod_fun) * int(circle_dur_fun) / (60 * float(out_prod_fun)) * float(k_mj[0])), 2)
    if is_cluster is False:
        MJ_Total[0] += mj
    return mj


def label_construct_new(ind_fun, amount_prod_fun, is_cluster=False):

    """Label for large node"""

    Scheme_process = Module_Input_Parametrs.Scheme_process

    sql_quarry_recipe = """
                    SELECT Recipes.id_equp, Raw_mat_and_products.image, Quick_analys.name_recipe, Recipes.output_prod, 
                    Recipes.circle_duration FROM Recipes
                    INNER JOIN Raw_mat_and_products ON Raw_mat_and_products.id_rmp = Recipes.id_prod
                    INNER JOIN Quick_analys ON Quick_analys.id_recipe = Recipes.id_recipe
                    WHERE Recipes.id_recipe = :id_recipe"""
    sql_quarry_recipe_none = """
                    SELECT Recipes.id_equp, Raw_mat_and_products.image, Raw_mat_and_products.name, Recipes.output_prod, 
                    Recipes.circle_duration FROM Recipes
                    INNER JOIN Raw_mat_and_products ON Raw_mat_and_products.id_rmp = Recipes.id_prod
                    WHERE Recipes.id_recipe = :id_recipe"""
    sql_quarry_prod = 'SELECT image FROM Raw_mat_and_products WHERE id_rmp = :id_prod'

    # ================================================ LABEL CONSTRUCT CODE ============================================
    label_str_1 = '<<TABLE border="0" cellpadding="2">'
    cursor = satisfactory_db.cursor()
    if Scheme_process[ind_fun][1] > 0:
        sql_answer = cursor.execute(sql_quarry_recipe, {'id_recipe': Scheme_process[ind_fun][1]}).fetchone()
        if sql_answer is None:
            sql_answer = cursor.execute(sql_quarry_recipe_none, {'id_recipe': Scheme_process[ind_fun][1]}).fetchone()
        if str(Scheme_process[ind_fun][3]).count('MJ') > 0:
            label_mj = label_construct_mj(str(sql_answer[0]), amount_prod_fun, sql_answer[3], sql_answer[4], is_cluster)
            label_str_2 = '<TR><TD width="60" height="15" fixedsize="true" border="1" bgcolor=' \
                          + str(dict_of_color[int(sql_answer[0])]) + ' style="rounded"><FONT>' \
                          + str(amount_prod_fun) + '</FONT></TD></TR>'
            label_str_4 = '<TR><TD width="60" height="15" fixedsize="true" border="1" style="rounded">' \
                          '<FONT POINT-SIZE="9">' + str(label_mj) + ' MJ' + '</FONT></TD></TR>'
        else:
            label_surplus = get_k_amount(amount_prod_fun, sql_answer[3]) * sql_answer[3] - int(amount_prod_fun)
            label_str_2 = '<TR><TD width="60" height="15" fixedsize="true" border="1" bgcolor=' \
                          + str(dict_of_color[int(sql_answer[0])]) + ' style="rounded"><FONT>' \
                          + str(int(amount_prod_fun)) + '</FONT></TD></TR>'
            if label_surplus == 0:
                label_str_4 = ''
            else:
                label_str_4 = '<TR><TD width="60" height="15" fixedsize="true" border="1" style="rounded">' + \
                              'surplus: ' + str(label_surplus) + '</TD></TR>'

        label_str_3 = '<TR><TD cellpadding="5" width="60" height="60" fixedsize="true" border="1" style="rounded" ' \
                      'port="here"><IMG SCALE="true" SRC="' + str(sql_answer[1]) + '"/></TD></TR>'

        label_str_5 = '<TR><TD border="1" style="rounded">' \
                      '<FONT point-size="6">' + str(sql_answer[2]).replace('_', '  ') + '</FONT></TD></TR></TABLE>>'
    else:
        sql_answer = cursor.execute(sql_quarry_prod, {'id_prod': Scheme_process[ind_fun][1] * -1}).fetchone()
        label_str_2 = '<TR><TD width="60" height="15" fixedsize="true" border="1" style="rounded">' \
                      '<FONT face="Comic Sans MS, bold"><U>' + str(amount_prod_fun) + '</U></FONT></TD></TR>'
        label_str_3 = '<TR><TD cellpadding="5" width="60" height="60" fixedsize="true" border="1" style="rounded" ' \
                      'port="here"><IMG SRC="' + str(sql_answer[0]) + '"/></TD></TR></TABLE>>'
        label_str_4 = ''
        label_str_5 = ''
    cursor.close()
    label_fun = label_str_1 + label_str_2 + label_str_3 + label_str_4 + label_str_5
    return label_fun


def scheme_node_new(type_work, oil_level):

    """This function creates five schemas"""

    dict_of_check_key = {}
    list_of_repeat = []
    list_of_exception_key = []
    dict_of_prod = {}
    Scheme_process = Module_Input_Parametrs.Scheme_process
    Scheme_rawmat = Module_Input_Parametrs.Scheme_rawmat
    Scheme_process_gen_amt = Module_Input_Parametrs.Scheme_process_gen_amt

    dict_of_cluster = {43: ['oil_cluster_p', "", 0], 44: ['oil_cluster_r', "", 0], 39: ['cluster_fuel', 'Fuel Production', 0],
                       23: ['cluster_con', 'Concrete Production', 0], 65: ['cluster_al', 'Bauxite Processing', 0],
                       55: ['cluster_cry', 'Quartz Crystal Processing', 0],
                       56: ['cluster_s', 'Silica Production', 0],
                       53: ['cluster_c', 'Caterium Processing', 0], 19: ['cluster_copper', 'Copper Processing', 0],
                       24: ['cluster_steel', 'Steal Processing', 0], 13: ['cluster_iron', 'Iron Processing', 0]}

    list_of_simple_clusters = (13, 19, 53, 55, 56, 23, 24)

    sql_quarry_recipe = 'SELECT id_input_1, id_input_2, output_prod, input_1, input_2, circle_duration ' \
                        'FROM Recipes WHERE id_recipe = :id_rec'

    s_node = graphviz.Digraph('Scheme', node_attr={'shape': "plaintext", 'fontname': "Comic Sans MS", 'fontsize': "10"})
    s_node.attr(splines="polyline", overlap="false", rankdir="LR", dpi="300", concentrate='true', layout='dot',
                style='filled', bgcolor='gray50')

    clust = graphviz.Digraph('Adv', node_attr={'shape': "plaintext", 'fontname': "Comic Sans MS", 'fontsize': "10"})
    clust.attr(splines="true", overlap="false", rankdir="TB", dpi="300", concentrate='true', layout='dot',
               newrank='true', style='filled', bgcolor='gray50')

    oil_graph = graphviz.Digraph('Adv', node_attr={'shape': "plaintext", 'fontname': "Comic Sans MS", 'fontsize': "10"})
    oil_graph.attr(splines="true", overlap="false", rankdir="LR", dpi="300", concentrate='true', layout='dot',
                   newrank='true', style='filled', bgcolor='gray50')

    bau_fuel_graph = graphviz.Digraph('Adv', node_attr={'shape': "plaintext", 'fontname': "Comic Sans MS", 'fontsize': "10"})
    bau_fuel_graph.attr(splines="true", overlap="false", rankdir="LR", dpi="300", concentrate='true', layout='dot',
                   newrank='true', style='filled', bgcolor='gray50')

    top_graph = graphviz.Digraph('Adv', node_attr={'shape': "plaintext", 'fontname': "Comic Sans MS", 'fontsize': "10"})
    top_graph.attr(splines="polyline", overlap="false", rankdir="LR", dpi="300", concentrate='true', layout='dot',
                   style='filled', bgcolor='gray50')

    # --- Make Cluster Nodes ---
    """Definition of products and creation of nodes related to side schemes."""

    for key in Scheme_process:
        key_parent = int(Scheme_process[key][5])
        if key_parent in dict_of_check_key:
            ind_limit = 1 + int(dict_of_check_key[key_parent])
            if ind_limit == 0:
                continue
            for ind in range(1, ind_limit):
                list_of_exception_key.append(key + ind)
            continue
        elif key_parent in dict_of_cluster:
            # Clusters process
            if key_parent == 24 and Scheme_process[key][1] == 34:
                with clust.subgraph(name=str(dict_of_cluster[key_parent][0]),
                                    edge_attr={'arrowhead': "diamond", 'arrowtail': "odiamond", 'arrowsize': "0.5",
                                               'dir': "both"}) as node_cluster:
                    node_cluster.attr(fontname="Comic Sans MS", fontsize='12',
                                      label=str(dict_of_cluster[key_parent][1]), style='rounded, filled',
                                      concentrate='true', rank='same', color='gray10', fillcolor="gray80:gray90",
                                      gradientangle='315')

                    dict_of_cluster[key_parent][2] = 1

                    node_cluster.node('cl_node_' + str(key_parent),
                                      label_construct_new(key, Scheme_process_gen_amt[key_parent]))
                    rec_data = [2, 41, 20, 15, 15, 12]
                    if type_work == 1:
                        k_amount = get_k_amount(Scheme_process_gen_amt[key_parent], rec_data[2])
                        prod_iron = k_amount * rec_data[3]
                        prod_coke = k_amount * rec_data[4]
                        k_amount_coke = get_k_amount(prod_coke, 12)
                        prod_Hoil = k_amount_coke * 4
                        prod_oil = prod_Hoil // 4 * 3
                    else:
                        k_amount = get_k_amount_per_min(Scheme_process_gen_amt[key_parent], rec_data[2], rec_data[5])
                        prod_iron = round(k_amount * 60 * rec_data[3] / rec_data[5], 2)
                        prod_coke = round(k_amount * 60 * rec_data[4] / rec_data[5], 2)
                        k_amount_coke = get_k_amount_per_min(prod_coke, 12, 6)
                        prod_Hoil = round(k_amount_coke * 60 * 4 / 6, 2)
                        prod_oil = round(prod_Hoil / 4 * 3, 2)

                    rec_data = [prod_iron, prod_coke, prod_Hoil, prod_oil]

                    with node_cluster.subgraph(name='cluster_inner_' + str(key_parent)) as inner_cl_gr:
                        inner_cl_gr.attr(rank='max', label='')

                        inner_cl_gr.node('cl_node_iron_' + str(key_parent), label_construct_new(key + 1, prod_iron))
                        inner_cl_gr.node('cl_node_coke_' + str(key_parent), label_construct_new(key + 2, prod_coke))
                        inner_cl_gr.node('cl_node_Hoil_' + str(key_parent), label_construct_new(key + 3, prod_Hoil))
                        inner_cl_gr.node('cl_node_oil_' + str(key_parent), label_construct_new(key + 4, prod_oil))
                        inner_cl_gr.node('cl_node_poly_waste' + str(key_parent), label_construct_waste(66, prod_Hoil,
                                                                                                       42, type_work))
                    """node_cluster.edge('cl_node_iron_' + str(key_parent) + ':here',
                                      'cl_node_' + str(key_parent) + ':here')
                    node_cluster.edge('cl_node_coke_' + str(key_parent) + ':here',
                                      'cl_node_' + str(key_parent) + ':here')
                    node_cluster.edge('cl_node_Hoil_' + str(key_parent) + ':here',
                                      'cl_node_coke_' + str(key_parent) + ':here')
                    node_cluster.edge('cl_node_oil_' + str(key_parent) + ':here',
                                      'cl_node_Hoil_' + str(key_parent) + ':here')
                    node_cluster.edge('cl_node_oil_' + str(key_parent) + ':here',
                                      'cl_node_poly_waste' + str(key_parent) + ':here')"""
                    for ind in range(1, 5):
                        Scheme_process_gen_amt[Scheme_process[key + ind][5]] -= rec_data[ind - 1]
                        list_of_exception_key.append(key + ind)
                dict_of_check_key[key_parent] = 4

            elif key_parent in list_of_simple_clusters:
                with clust.subgraph(name=str(dict_of_cluster[key_parent][0]),
                                    edge_attr={'arrowhead': "diamond", 'arrowtail': "odiamond", 'arrowsize': "0.5",
                                               'dir': "both"}) as node_cluster:
                    node_cluster.attr(fontname="Comic Sans MS", fontsize='12',
                                      label=str(dict_of_cluster[key_parent][1]), style='rounded, filled',
                                      concentrate='true', rank='same', color='gray10', fillcolor="gray80:gray90",
                                      gradientangle='315')

                    node_cluster.node('cl_node_' + str(key_parent),
                                      label_construct_new(key, Scheme_process_gen_amt[key_parent]))

                    dict_of_cluster[key_parent][2] = 1

                    cursor = satisfactory_db.cursor()
                    rec_data = cursor.execute(sql_quarry_recipe, {'id_rec': Scheme_process[key][1]}).fetchone()
                    cursor.close()

                    if type_work == 1:
                        k_amount = get_k_amount(Scheme_process_gen_amt[key_parent], rec_data[2])
                    else:
                        k_amount = get_k_amount_per_min(Scheme_process_gen_amt[key_parent], rec_data[2], rec_data[5])

                    for ind in range(1, 3):
                        if rec_data[2 + ind] is None:
                            ind = ind - 1
                            break

                        if type_work == 1:
                            prod = k_amount * rec_data[2 + ind]
                        else:
                            prod = round(k_amount * 60 * rec_data[2 + ind] / rec_data[5], 2)

                        with node_cluster.subgraph(name='cluster_inner_' + str(key_parent)) as inner_cl_gr:
                            inner_cl_gr.attr(rank='max', label='')
                            inner_cl_gr.node('cl_node_' + str(ind) + '_' + str(key_parent),
                                             label_construct_new(key + ind, prod, is_cluster=True))

                        if Scheme_process[key + ind][1] < 0 and (Scheme_process[key + ind][1] != -44):
                            Scheme_process_gen_amt[Scheme_process[key + ind][5]] -= prod
                            list_of_exception_key.append(key + ind)
                        else:
                            ind -= 1

                    dict_of_check_key[key_parent] = ind
                    # list_of_repeat.append(key_parent)
                    # continue
                # Oil process

            elif key_parent == 39:
                with bau_fuel_graph.subgraph(name=str(dict_of_cluster[key_parent][0]),
                                             edge_attr={'arrowhead': "diamond", 'arrowtail': "odiamond",
                                                        'arrowsize': "0.5", 'dir': "both"}) as node_cluster:
                    node_cluster.attr(fontname="Comic Sans MS", fontsize='12',
                                      label=str(dict_of_cluster[key_parent][1]), style='rounded, filled',
                                      concentrate='true', color='gray10', fillcolor="gray80:gray90", gradientangle='315')

                    node_cluster.node('cl_node_' + str(key_parent),
                                      label_construct_new(key, Scheme_process_gen_amt[key_parent]))

                    dict_of_cluster[key_parent][2] = 2

                    if type_work == 1:
                        k_amount = get_k_amount(Scheme_process_gen_amt[key_parent], 2)
                        prod_Hoil = k_amount
                        prod_water = k_amount * 2
                        prod_oil = k_amount // 4 * 3
                    else:
                        prod_Hoil = round(Scheme_process_gen_amt[key_parent] / 2, 2)
                        prod_oil = round(prod_Hoil / 40 * 30, 2)
                        prod_water = round(prod_Hoil * 2, 2)

                    node_cluster.node('cl_node_Hoil_' + str(key_parent), label_construct_new(key + 1, prod_Hoil))
                    node_cluster.node('cl_node_water_' + str(key_parent), label_construct_new(key + 3, prod_water))
                    node_cluster.node('cl_node_oil_' + str(key_parent), label_construct_new(key + 2, prod_oil))
                    node_cluster.node('cl_node_poly_waste' + str(key_parent), label_construct_waste(66, prod_Hoil,
                                                                                                    42, type_work))
                    node_cluster.edge('cl_node_Hoil_' + str(key_parent) + ':here',
                                      'cl_node_' + str(key_parent) + ':here')
                    node_cluster.edge('cl_node_water_' + str(key_parent) + ':here',
                                      'cl_node_' + str(key_parent) + ':here')
                    node_cluster.edge('cl_node_oil_' + str(key_parent) + ':here',
                                      'cl_node_Hoil_' + str(key_parent) + ':here')
                    node_cluster.edge('cl_node_oil_' + str(key_parent) + ':here',
                                      'cl_node_poly_waste' + str(key_parent) + ':here')

                    Scheme_process_gen_amt[Scheme_process[key + 1][5]] -= prod_Hoil
                    Scheme_process_gen_amt[Scheme_process[key + 2][5]] -= prod_oil
                    Scheme_process_gen_amt[Scheme_process[key + 3][5]] -= prod_water

                    list_of_exception_key.append(key + 1)
                    list_of_exception_key.append(key + 2)
                    list_of_exception_key.append(key + 3)

                dict_of_check_key[key_parent] = 3

            elif key_parent == 44 or key_parent == 43:
                oil = str(oil_prod(key_parent, Scheme_process_gen_amt[key_parent], oil_level,
                                   type_work)).split('_')
                with oil_graph.subgraph(name='cluster_oil_node_' + str(key_parent),
                                        edge_attr={'arrowhead': "diamond", 'arrowtail': "odiamond", 'arrowsize': "0.5",
                                                   'dir': "both",
                                                   'fontname': "Comic Sans MS", 'fontsize': "8"}) as oil_node:
                    oil_node.attr(label='Oil Refining\n' + 'level: ' + str(oil[0]), concentrate='true',
                                  fontname="Comic Sans MS", fontsize='12', style='rounded, filled', color='gray10',
                                  fillcolor="gray80:gray90", gradientangle='315')

                    dict_of_cluster[key_parent][2] = 3

                    if int(oil[2]) != 0:
                        k_oil = int(oil[1])
                        s_oil = k_oil * int(oil[2]) - Scheme_process_gen_amt[key_parent]
                        k_mj = 0
                    else:
                        k_oil = float(oil[1])
                        s_oil = 0
                        k_mj = 1
                    ind = key
                    dict_of_check_key[key_parent] = -1

                    # -------------------------------- Plastic --------------------------------------
                    if Scheme_process[ind][1] == -43 and int(oil[0]) == 0:
                        # --------------------Type_work = 1 Requirements_oil_fun = 0 --------------------
                        label = label_construct_oil(43, k_oil * 2, type_work, s_oil, k_mj * k_oil * 3, 'Plastic')
                        oil_node.node('node_' + str(key_parent), label=label)

                        label = label_construct_oil(38, k_oil * 1, type_work, 0, 'by', 'Heavy  Oil  Residue')
                        oil_node.node('node_heavy_oil_' + str(ind), label=label)

                        label = label_construct_oil(7, k_oil * 3, type_work, 0, 0, '')
                        oil_node.node('node_oil_' + str(ind), label=label)
                        #           --------------------Edge --------------------
                        oil_node.edge('node_oil_' + str(ind) + ':here',
                                      'node_' + str(key_parent) + ':here')
                        oil_node.edge('node_oil_' + str(ind) + ':here',
                                      'node_heavy_oil_' + str(ind) + ':here')

                    elif Scheme_process[ind][1] == -43 and int(oil[0]) == 1:
                        # --------------------Type_work = 1 Requirements_oil_fun = 1 --------------------

                        label = label_construct_oil(43, k_oil * 12, type_work, s_oil, k_mj * k_oil * 6, 'Recycled  Plastic')
                        oil_node.node('node_' + str(key_parent), label=label)

                        label = label_construct_oil(44, k_oil * 6, type_work, 0, k_mj * k_oil * 9, 'Rubber')
                        oil_node.node('node_oil_rubber_' + str(ind), label=label)

                        label = label_construct_oil(39, k_oil * 12, type_work, 0, k_mj * k_oil * 6, 'Diluted  Fuel')
                        oil_node.node('node_oil_fuel_' + str(ind), label=label)

                        label = label_construct_oil(39, k_oil * 6, type_work, 0, 0, 'Surplus: Fuel')
                        oil_node.node('node_oil_fuel_surplus_' + str(ind), label=label)

                        label = label_construct_oil(38, k_oil * 6, type_work, 0, 'by', 'Heavy  Oil  Residue')
                        oil_node.node('node_heavy_oil_' + str(ind), label=label)

                        label = label_construct_oil(7, k_oil * 9, type_work, 0, 0, '')
                        oil_node.node('node_oil_' + str(ind), label=label)

                        label = label_construct_oil(1, k_oil * 12, type_work, 0, 0, '')
                        oil_node.node('node_water_' + str(ind), label=label)
                        #           --------------------Edge --------------------
                        """oil_node.edge('node_oil_final_' + str(ind) + ':here',
                                      'node_' + str(Scheme_process[ind][0]) + ':here')"""
                        oil_node.edge('node_oil_rubber_' + str(ind) + ':here',
                                      'node_' + str(key_parent) + ':here')
                        oil_node.edge('node_oil_fuel_' + str(ind) + ':here',
                                      'node_' + str(key_parent) + ':here')
                        oil_node.edge('node_water_' + str(ind) + ':here', 'node_oil_fuel_' + str(ind) + ':here')
                        oil_node.edge('node_heavy_oil_' + str(ind) + ':here', 'node_oil_fuel_' + str(ind) + ':here')
                        oil_node.edge('node_oil_fuel_' + str(ind) + ':here',
                                      'node_oil_fuel_surplus_' + str(ind) + ':here')
                        oil_node.edge('node_oil_' + str(ind) + ':here', 'node_oil_rubber_' + str(ind) + ':here')
                        oil_node.edge('node_oil_' + str(ind) + ':here', 'node_heavy_oil_' + str(ind) + ':here')

                    elif Scheme_process[ind][1] == -43 and int(oil[0]) == 2:
                        # --------------------Type_work = 1 Requirements_oil_fun = 2 --------------------
                        label = label_construct_oil(43, k_oil * 18, type_work, s_oil, 0, 'Plastic')
                        oil_node.node('node_' + str(key_parent), label=label)

                        label = label_construct_oil(43, k_oil * 10, type_work, 0, 0, 'Plastic')
                        oil_node.node('node_o_pl_1_pt_' + str(ind), label=label)
                        label = label_construct_oil(43, k_oil * 2, type_work, 0, 0, 'Plastic')
                        oil_node.node('node_oil_pl_1_' + str(ind), label=label)

                        label = label_construct_oil(43, k_oil * 12, type_work, 0, k_oil * 6, 'Recycled  Plastic')
                        oil_node.node('node_oil_pl_0_pt_' + str(ind), label=label)

                        label = label_construct_oil(44, k_oil * 4, type_work, 0, k_oil * 2, 'Recycled  Rubber')
                        oil_node.node('node_oil_rub_0_' + str(ind), label=label)

                        label = label_construct_oil(43, k_oil * 8, type_work, 0, k_oil * 4, 'Recycled  Plastic')
                        oil_node.node('node_oil_pl_2_pt_' + str(ind), label=label)

                        label = label_construct_oil(44, k_oil * 6, type_work, 0, k_oil * 9, 'Rubber')
                        oil_node.node('node_oil_rubber_' + str(ind), label=label)

                        label = label_construct_oil(38, k_oil * 6, type_work, 0, 'by', 'Heavy  Oil  Residue')
                        oil_node.node('node_heavy_oil_' + str(ind), label=label)
                        label = label_construct_oil(39, k_oil * 12, type_work, 0, k_oil * 6, 'Diluted  Fuel')
                        oil_node.node('node_fuel_' + str(ind), label=label)

                        label = label_construct_oil(1, k_oil * 12, type_work, 0, 0, '')
                        oil_node.node('node_water_' + str(ind), label=label)
                        label = label_construct_oil(7, k_oil * 9, type_work, 0, 0, '')
                        oil_node.node('node_crude_oil_' + str(ind), label=label)
                        if type_work == 2:
                            oil_node.node('fuel_k2' + str(ind), label=str(edge_label(round(k_oil * 2, 2), adv=' Fuel')))
                            oil_node.node('fuel_k4' + str(ind), label=str(edge_label(round(k_oil * 4, 2), adv=' Fuel')))
                            oil_node.node('fuel_k6' + str(ind), label=str(edge_label(round(k_oil * 6, 2), adv=' Fuel')))
                        else:
                            oil_node.node('fuel_k2' + str(ind), label=str(edge_label(k_oil * 2, adv=' Fuel')))
                            oil_node.node('fuel_k4' + str(ind), label=str(edge_label(k_oil * 4, adv=' Fuel')))
                            oil_node.node('fuel_k6' + str(ind), label=str(edge_label(k_oil * 6, adv=' Fuel')))

                        #           --------------------Edge --------------------
                        oil_node.edge('node_o_pl_1_pt_' + str(ind) + ':here',
                                      'node_' + str(key_parent) + ':here')
                        oil_node.edge('node_oil_pl_2_pt_' + str(ind) + ':here',
                                      'node_' + str(key_parent) + ':here')
                        oil_node.edge('node_oil_rub_0_' + str(ind) + ':here',
                                      'node_oil_pl_2_pt_' + str(ind) + ':here')
                        oil_node.edge('node_oil_pl_1_' + str(ind) + ':here', 'node_oil_rub_0_' + str(ind) + ':here')
                        oil_node.edge('node_oil_pl_0_pt_' + str(ind) + ':here',
                                      'node_oil_pl_1_' + str(ind) + ':here')
                        oil_node.edge('node_oil_pl_0_pt_' + str(ind) + ':here',
                                      'node_o_pl_1_pt_' + str(ind) + ':here')
                        oil_node.edge('node_oil_rubber_' + str(ind) + ':here',
                                      'node_oil_pl_0_pt_' + str(ind) + ':here',
                                      _attributes={'constraint': "false"})

                        oil_node.edge('node_fuel_' + str(ind) + ':here', 'fuel_k6' + str(ind) + ':in',
                                      _attributes={'color': 'orange'})
                        oil_node.edge('fuel_k6' + str(ind) + ':out', 'node_oil_pl_0_pt_' + str(ind) + ':here',
                                      _attributes={'color': 'orange'})

                        oil_node.edge('node_fuel_' + str(ind) + ':here', 'fuel_k2' + str(ind) + ':in',
                                      _attributes={'color': 'orange'})
                        oil_node.edge('fuel_k2' + str(ind) + ':out', 'node_oil_rub_0_' + str(ind) + ':here',
                                      _attributes={'color': 'orange'})

                        oil_node.edge('node_fuel_' + str(ind) + ':here', 'fuel_k4' + str(ind) + ':in',
                                      _attributes={'color': 'orange'})
                        oil_node.edge('fuel_k4' + str(ind) + ':out', 'node_oil_pl_2_pt_' + str(ind) + ':here',
                                      _attributes={'color': 'orange'})

                        oil_node.edge('node_crude_oil_' + str(ind) + ':here',
                                      'node_oil_rubber_' + str(ind) + ':here')
                        oil_node.edge('node_crude_oil_' + str(ind) + ':here',
                                      'node_heavy_oil_' + str(ind) + ':here')
                        oil_node.edge('node_heavy_oil_' + str(ind) + ':here', 'node_fuel_' + str(ind) + ':here')
                        oil_node.edge('node_water_' + str(ind) + ':here', 'node_fuel_' + str(ind) + ':here')

                    elif Scheme_process[ind][1] == -43 and int(oil[0]) == 3:
                        # --------------------Type_work = 1 Requirements_oil_fun = 3 --------------------
                        label = label_construct_oil(43, k_oil * 54, type_work, s_oil, 0, 'Plastic')
                        oil_node.node('node_' + str(key_parent), label=label)

                        label = label_construct_oil(43, k_oil * 46, type_work, 0, 0, 'Plastic')
                        oil_node.node('node_o_pl_1_pt_' + str(ind), label=label)

                        label = label_construct_oil(43, k_oil * 8, type_work, 0, k_oil * 4, 'Recycled  Plastic')
                        oil_node.node('node_o_pl_2_pt_' + str(ind), label=label)

                        label = label_construct_oil(44, k_oil * 4, type_work, 0, k_oil * 2, 'Recycled  Rubber')
                        oil_node.node('node_o_rub_2_' + str(ind), label=label)

                        label = label_construct_oil(43, k_oil * 2, type_work, 0, 0, 'Plastic')
                        oil_node.node('node_o_pl_2_' + str(ind), label=label)

                        label = label_construct_oil(43, k_oil * 48, type_work, 0, k_oil * 24, 'Recycled  Plastic')
                        oil_node.node('node_o_pl_main_' + str(ind), label=label)

                        label = label_construct_oil(44, k_oil * 24, type_work, 0, k_oil * 12, 'Recycled  Rubber')
                        oil_node.node('node_o_rub_m1_' + str(ind), label=label)

                        label = label_construct_oil(43, k_oil * 12, type_work, 0, k_oil * 6, 'Recycled  Plastic')
                        oil_node.node('node_o_pl_m1_' + str(ind), label=label)

                        label = label_construct_oil(44, k_oil * 6, type_work, 0, k_oil * 9, 'Residual  Rubber')
                        oil_node.node('node_o_rub_m2_' + str(ind), label=label)

                        label = label_construct_oil(42, k_oil * 12, type_work, 0, 'by', 'Polymer  Resin')
                        oil_node.node('node_o_poly_' + str(ind), label=label)

                        label = label_construct_oil(38, k_oil * 24, type_work, 0, k_oil * 18, 'Heavy  Oil  Residue')
                        oil_node.node('node_o_heavy_' + str(ind), label=label)

                        label = label_construct_oil(39, k_oil * 48, type_work, 0, k_oil * 24, 'Diluted  Fuel')
                        oil_node.node('node_o_fuel_' + str(ind), label=label)

                        label = label_construct_oil(1, k_oil * 48, type_work, 0, 0, '')
                        oil_node.node('node_o_water_f_' + str(ind), label=label)
                        label = label_construct_oil(1, k_oil * 12, type_work, 0, 0, '')
                        oil_node.node('node_o_water_p_' + str(ind), label=label)
                        label = label_construct_oil(7, k_oil * 18, type_work, 0, 0, '')
                        oil_node.node('node_oil_crude_' + str(ind), label=label)

                        if type_work == 1:
                            oil_node.node('fuel_k12' + str(ind), label=str(edge_label(k_oil * 12, adv=' Fuel')))
                            oil_node.node('fuel_k24' + str(ind), label=str(edge_label(k_oil * 24, adv=' Fuel')))
                            oil_node.node('fuel_k2' + str(ind), label=str(edge_label(k_oil * 2, adv=' Fuel')))
                            oil_node.node('fuel_k6' + str(ind), label=str(edge_label(k_oil * 6, adv=' Fuel')))
                            oil_node.node('fuel_k4' + str(ind), label=str(edge_label(k_oil * 4, adv=' Fuel')))
                        else:
                            oil_node.node('fuel_k12' + str(ind), label=str(edge_label(round(k_oil * 12, 2), adv=' Fuel')))
                            oil_node.node('fuel_k24' + str(ind), label=str(edge_label(round(k_oil * 24, 2), adv=' Fuel')))
                            oil_node.node('fuel_k2' + str(ind), label=str(edge_label(round(k_oil * 2, 2), adv=' Fuel')))
                            oil_node.node('fuel_k6' + str(ind), label=str(edge_label(round(k_oil * 6, 2), adv=' Fuel')))
                            oil_node.node('fuel_k4' + str(ind), label=str(edge_label(round(k_oil * 4, 2), adv=' Fuel')))
                        #           --------------------Edge --------------------
                        oil_node.edge('node_o_pl_1_pt_' + str(ind) + ':here',
                                      'node_' + str(key_parent) + ':here')
                        oil_node.edge('node_o_pl_2_pt_' + str(ind) + ':here',
                                      'node_' + str(key_parent) + ':here')
                        oil_node.edge('node_o_rub_2_' + str(ind) + ':here', 'node_o_pl_2_pt_' + str(ind) + ':here')
                        oil_node.edge('node_o_pl_2_' + str(ind) + ':here', 'node_o_rub_2_' + str(ind) + ':here')
                        oil_node.edge('node_o_pl_main_' + str(ind) + ':here', 'node_o_pl_2_' + str(ind) + ':here')
                        oil_node.edge('node_o_pl_main_' + str(ind) + ':here',
                                      'node_o_pl_1_pt_' + str(ind) + ':here')
                        oil_node.edge('node_o_rub_m1_' + str(ind) + ':here', 'node_o_pl_main_' + str(ind) + ':here')
                        oil_node.edge('node_o_rub_m2_' + str(ind) + ':here', 'node_o_pl_m1_' + str(ind) + ':here')
                        oil_node.edge('node_o_pl_m1_' + str(ind) + ':here', 'node_o_rub_m1_' + str(ind) + ':here')
                        oil_node.edge('node_o_poly_' + str(ind) + ':here', 'node_o_rub_m2_' + str(ind) + ':here')
                        oil_node.edge('node_o_water_p_' + str(ind) + ':here', 'node_o_rub_m2_' + str(ind) + ':here')
                        oil_node.edge('node_oil_crude_' + str(ind) + ':here', 'node_o_poly_' + str(ind) + ':here')
                        oil_node.edge('node_oil_crude_' + str(ind) + ':here', 'node_o_heavy_' + str(ind) + ':here')
                        oil_node.edge('node_o_heavy_' + str(ind) + ':here', 'node_o_fuel_' + str(ind) + ':here')
                        oil_node.edge('node_o_water_f_' + str(ind) + ':here', 'node_o_fuel_' + str(ind) + ':here')

                        oil_node.edge('node_o_fuel_' + str(ind) + ':here', 'fuel_k12' + str(ind) + ':in',
                                      _attributes={'color': 'orange'})
                        oil_node.edge('fuel_k12' + str(ind) + ':out', 'node_o_rub_m1_' + str(ind) + ':here',
                                      _attributes={'color': 'orange'})

                        oil_node.edge('node_o_fuel_' + str(ind) + ':here', 'fuel_k6' + str(ind) + ':in',
                                      _attributes={'color': 'orange'})
                        oil_node.edge('fuel_k6' + str(ind) + ':out', 'node_o_pl_m1_' + str(ind) + ':here',
                                      _attributes={'color': 'orange'})

                        oil_node.edge('node_o_fuel_' + str(ind) + ':here', 'fuel_k24' + str(ind) + ':in',
                                      _attributes={'color': 'orange'})
                        oil_node.edge('fuel_k24' + str(ind) + ':out', 'node_o_pl_main_' + str(ind) + ':here',
                                      _attributes={'color': 'orange'})

                        oil_node.edge('node_o_fuel_' + str(ind) + ':here', 'fuel_k2' + str(ind) + ':in',
                                      _attributes={'color': 'orange'})
                        oil_node.edge('fuel_k2' + str(ind) + ':out', 'node_o_rub_2_' + str(ind) + ':here',
                                      _attributes={'color': 'orange'})

                        oil_node.edge('node_o_fuel_' + str(ind) + ':here', 'fuel_k4' + str(ind) + ':in',
                                      _attributes={'color': 'orange'})
                        oil_node.edge('fuel_k4' + str(ind) + ':out', 'node_o_pl_2_pt_' + str(ind) + ':here',
                                      _attributes={'color': 'orange'})

                    # -------------------------------- Rubber --------------------------------------
                    elif Scheme_process[ind][1] == -44 and int(oil[0]) == 0:
                        # --------------------Type_work = 1 Requirements_oil_fun = 0 --------------------
                        label = label_construct_oil(44, k_oil * 2, type_work, s_oil, k_mj * k_oil * 3, 'Rubber')
                        oil_node.node('node_' + str(key_parent), label=label)

                        label = label_construct_oil(38, k_oil * 2, type_work, 0, 'by', 'Heavy  Oil  Residue')
                        oil_node.node('node_heavy_oil_' + str(ind), label=label)

                        label = label_construct_oil(7, k_oil * 3, type_work, 0, 0, '')
                        oil_node.node('node_oil_' + str(ind), label=label)
                        #           --------------------Edge --------------------
                        oil_node.edge('node_oil_' + str(ind) + ':here',
                                      'node_' + str(key_parent) + ':here')
                        oil_node.edge('node_oil_' + str(ind) + ':here',
                                      'node_heavy_oil_' + str(ind) + ':here')

                    elif Scheme_process[ind][1] == -44 and int(oil[0]) == 1:
                        # --------------------Type_work = 1 Requirements_oil_fun = 1 --------------------
                        label = label_construct_oil(44, k_oil * 12, type_work, s_oil, k_mj * k_oil * 6, 'Recycled  Rubber')
                        oil_node.node('node_' + str(key_parent), label=label)
                        label = label_construct_oil(43, k_oil * 6, type_work, 0, k_mj * k_oil * 9, 'Plastic')
                        oil_node.node('node_oil_plastic_' + str(ind), label=label)
                        label = label_construct_oil(39, k_oil * 6, type_work, 0, k_mj * k_oil * 3, 'Diluted  Fuel')
                        oil_node.node('node_oil_fuel_' + str(ind), label=label)
                        label = label_construct_oil(38, k_oil * 3, type_work, 0, 'by', 'Heavy  Oil  Residue')
                        oil_node.node('node_heavy_oil_' + str(ind), label=label)
                        label = label_construct_oil(7, k_oil * 9, type_work, 0, 0, '')
                        oil_node.node('node_oil_' + str(ind), label=label)
                        label = label_construct_oil(1, k_oil * 6, type_work, 0, 0, '')
                        oil_node.node('node_water_' + str(ind), label=label)
                        #           --------------------Edge --------------------
                        oil_node.edge('node_oil_plastic_' + str(ind) + ':here',
                                      'node_' + str(key_parent) + ':here')
                        oil_node.edge('node_oil_fuel_' + str(ind) + ':here',
                                      'node_' + str(key_parent) + ':here')
                        oil_node.edge('node_water_' + str(ind) + ':here', 'node_oil_fuel_' + str(ind) + ':here',
                                      _attributes={'constraint': 'false'})
                        oil_node.edge('node_heavy_oil_' + str(ind) + ':here', 'node_oil_fuel_' + str(ind) + ':here')
                        oil_node.edge('node_oil_' + str(ind) + ':here', 'node_oil_plastic_' + str(ind) + ':here')
                        oil_node.edge('node_oil_' + str(ind) + ':here', 'node_heavy_oil_' + str(ind) + ':here')

                    elif Scheme_process[ind][1] == -44 and int(oil[0]) == 3:
                        # --------------------Type_work = 1 Requirements_oil_fun = 2 --------------------
                        label = label_construct_oil(44, k_oil * 54, type_work, s_oil, 0, 'Rubber')
                        oil_node.node('node_' + str(key_parent), label=label)
                        label = label_construct_oil(44, k_oil * 48, type_work, 0, k_oil * 24, 'Recycle  Rubber')
                        oil_node.node('node_o_r_pt_1_' + str(ind), label=label)

                        label = label_construct_oil(44, k_oil * 6, type_work, 0, 0, 'Recycle  Rubber')
                        oil_node.node('node_o_r_pt_2_' + str(ind), label=label)

                        label = label_construct_oil(43, k_oil * 24, type_work, 0, k_oil * 12, 'Recycle  Plastic')
                        oil_node.node('node_o_dir_1_pl_1_' + str(ind), label=label)

                        label = label_construct_oil(44, k_oil * 12, type_work, 0, k_oil * 6, 'Recycle  Rubber')
                        oil_node.node('node_o_dir_1_rub_1_' + str(ind), label=label)

                        label = label_construct_oil(43, k_oil * 6, type_work, 0, k_oil * 3, 'Recycle  Plastic')
                        oil_node.node('node_o_dir_1_pl_2_' + str(ind), label=label)

                        label = label_construct_oil(44, k_oil * 3, type_work, 0, 0, 'Residual  Rubber')
                        oil_node.node('node_o_start_dir_1_' + str(ind), label=label)

                        label = label_construct_oil(44, k_oil * 4, type_work, 0, k_oil * 2, 'Recycle  Rubber')
                        oil_node.node('node_o_dir_2_rub_1_' + str(ind), label=label)

                        label = label_construct_oil(43, k_oil * 2, type_work, 0, k_oil * 1, 'Recycle  Plastic')
                        oil_node.node('node_o_dir_2_pl_1_' + str(ind), label=label)

                        label = label_construct_oil(44, k_oil * 1, type_work, 0, 0, 'Residual  Rubber')
                        oil_node.node('node_o_st_dir_2re_' + str(ind), label=label)
                        label = label_construct_oil(44, k_oil * 2, type_work, 0, 0, 'Residual  Rubber')
                        oil_node.node('node_o_surplus_rub_' + str(ind), label=label)
                        label = label_construct_oil(44, k_oil * 3, type_work, 0, 0, 'Residual  Rubber')
                        oil_node.node('node_o_start_dir_2_' + str(ind), label=label)

                        label = label_construct_oil(44, k_oil * 6, type_work, 0, k_oil * 9, 'Residual  Rubber')
                        oil_node.node('node_o_res_rub_' + str(ind), label=label)
                        label = label_construct_oil(39, k_oil * 48, type_work, 0, k_oil * 24, 'Diluted  Fuel')
                        oil_node.node('node_o_fuel_' + str(ind), label=label)
                        label = label_construct_oil(1, k_oil * 48, type_work, 0, 0, '')
                        oil_node.node('node_water_f_' + str(ind), label=label)
                        label = label_construct_oil(1, k_oil * 12, type_work, 0, 0, '')
                        oil_node.node('node_water_r_' + str(ind), label=label)

                        label = label_construct_oil(38, k_oil * 24, type_work, 0, k_oil * 18, 'Heavy  Oil  Residue')
                        oil_node.node('node_heavy_oil_' + str(ind), label=label)
                        label = label_construct_oil(42, k_oil * 12, type_work, 0, 'by', 'Polymer  Resin')
                        oil_node.node('node_poly_' + str(ind), label=label)

                        label = label_construct_oil(7, k_oil * 18, type_work, 0, 0, '')
                        oil_node.node('node_oil_' + str(ind), label=label)

                        if type_work == 1:
                            oil_node.node('fuel_k1' + str(ind), label=str(edge_label(k_oil * 1, adv=' Fuel')))
                            oil_node.node('fuel_k2' + str(ind), label=str(edge_label(k_oil * 2, adv=' Fuel')))
                            oil_node.node('fuel_k3' + str(ind), label=str(edge_label(k_oil * 3, adv=' Fuel')))
                            oil_node.node('fuel_k6' + str(ind), label=str(edge_label(k_oil * 6, adv=' Fuel')))
                            oil_node.node('fuel_k12' + str(ind), label=str(edge_label(k_oil * 12, adv=' Fuel')))
                            oil_node.node('fuel_k24' + str(ind), label=str(edge_label(k_oil * 24, adv=' Fuel')))
                        else:
                            oil_node.node('fuel_k1' + str(ind), label=str(edge_label(round(k_oil * 1, 2), adv=' Fuel')))
                            oil_node.node('fuel_k2' + str(ind), label=str(edge_label(round(k_oil * 2, 2), adv=' Fuel')))
                            oil_node.node('fuel_k3' + str(ind), label=str(edge_label(round(k_oil * 3, 2), adv=' Fuel')))
                            oil_node.node('fuel_k6' + str(ind), label=str(edge_label(round(k_oil * 6, 2), adv=' Fuel')))
                            oil_node.node('fuel_k12' + str(ind), label=str(edge_label(round(k_oil * 12, 2), adv=' Fuel')))
                            oil_node.node('fuel_k24' + str(ind), label=str(edge_label(round(k_oil * 24, 2), adv=' Fuel')))
                        #           --------------------Edge --------------------
                        oil_node.edge('node_o_r_pt_1_' + str(ind) + ':here',
                                      'node_' + str(key_parent) + ':here')
                        oil_node.edge('node_o_r_pt_2_' + str(ind) + ':here',
                                      'node_' + str(key_parent) + ':here')

                        oil_node.edge('node_o_dir_1_pl_1_' + str(ind) + ':here',
                                      'node_o_r_pt_1_' + str(ind) + ':here')
                        oil_node.edge('node_o_dir_1_rub_1_' + str(ind) + ':here',
                                      'node_o_dir_1_pl_1_' + str(ind) + ':here')
                        oil_node.edge('node_o_dir_1_pl_2_' + str(ind) + ':here',
                                      'node_o_dir_1_rub_1_' + str(ind) + ':here')
                        oil_node.edge('node_o_start_dir_1_' + str(ind) + ':here',
                                      'node_o_dir_1_pl_2_' + str(ind) + ':here')

                        oil_node.edge('node_o_dir_2_rub_1_' + str(ind) + ':here',
                                      'node_o_r_pt_2_' + str(ind) + ':here')
                        oil_node.edge('node_o_dir_2_pl_1_' + str(ind) + ':here',
                                      'node_o_dir_2_rub_1_' + str(ind) + ':here')
                        oil_node.edge('node_o_st_dir_2re_' + str(ind) + ':here',
                                      'node_o_dir_2_pl_1_' + str(ind) + ':here')
                        oil_node.edge('node_o_surplus_rub_' + str(ind) + ':here',
                                      'node_o_r_pt_2_' + str(ind) + ':here')
                        oil_node.edge('node_o_start_dir_2_' + str(ind) + ':here',
                                      'node_o_st_dir_2re_' + str(ind) + ':here')
                        oil_node.edge('node_o_start_dir_2_' + str(ind) + ':here',
                                      'node_o_surplus_rub_' + str(ind) + ':here')

                        oil_node.edge('node_o_res_rub_' + str(ind) + ':here',
                                      'node_o_start_dir_2_' + str(ind) + ':here')
                        oil_node.edge('node_o_res_rub_' + str(ind) + ':here',
                                      'node_o_start_dir_1_' + str(ind) + ':here')
                        oil_node.edge('node_water_r_' + str(ind) + ':here', 'node_o_res_rub_' + str(ind) + ':here',
                                      _attributes={'constraint': "true"})
                        oil_node.edge('node_poly_' + str(ind) + ':here', 'node_o_res_rub_' + str(ind) + ':here')

                        oil_node.edge('node_o_fuel_' + str(ind) + ':here', 'fuel_k1' + str(ind) + ':in',
                                      _attributes={'color': 'orange'})
                        oil_node.edge('fuel_k1' + str(ind) + ':out', 'node_o_dir_2_pl_1_' + str(ind) + ':here',
                                      _attributes={'color': 'orange'})

                        oil_node.edge('node_o_fuel_' + str(ind) + ':here', 'fuel_k2' + str(ind) + ':in',
                                      _attributes={'color': 'orange'})
                        oil_node.edge('fuel_k2' + str(ind) + ':out', 'node_o_dir_2_rub_1_' + str(ind) + ':here',
                                      _attributes={'color': 'orange'})

                        oil_node.edge('node_o_fuel_' + str(ind) + ':here', 'fuel_k3' + str(ind) + ':in',
                                      _attributes={'color': 'orange'})
                        oil_node.edge('fuel_k3' + str(ind) + ':out', 'node_o_dir_1_pl_2_' + str(ind) + ':here',
                                      _attributes={'color': 'orange'})

                        oil_node.edge('node_o_fuel_' + str(ind) + ':here', 'fuel_k6' + str(ind) + ':in',
                                      _attributes={'color': 'orange'})
                        oil_node.edge('fuel_k6' + str(ind) + ':out', 'node_o_dir_1_rub_1_' + str(ind) + ':here',
                                      _attributes={'color': 'orange'})

                        oil_node.edge('node_o_fuel_' + str(ind) + ':here', 'fuel_k12' + str(ind) + ':in',
                                      _attributes={'color': 'orange'})
                        oil_node.edge('fuel_k12' + str(ind) + ':out', 'node_o_dir_1_pl_1_' + str(ind) + ':here',
                                      _attributes={'color': 'orange'})

                        oil_node.edge('node_o_fuel_' + str(ind) + ':here', 'fuel_k24' + str(ind) + ':in',
                                      _attributes={'color': 'orange'})
                        oil_node.edge('fuel_k24' + str(ind) + ':out', 'node_o_r_pt_1_' + str(ind) + ':here',
                                      _attributes={'color': 'orange'})

                        oil_node.edge('node_heavy_oil_' + str(ind) + ':here', 'node_o_fuel_' + str(ind) + ':here')
                        oil_node.edge('node_water_f_' + str(ind) + ':here', 'node_o_fuel_' + str(ind) + ':here',
                                      _attributes={'constraint': "true"})

                        oil_node.edge('node_oil_' + str(ind) + ':here', 'node_heavy_oil_' + str(ind) + ':here')
                        oil_node.edge('node_oil_' + str(ind) + ':here', 'node_poly_' + str(ind) + ':here')

                # /Oil process

            elif key_parent == 65:
                print(Scheme_process)
                dict_of_cluster[key_parent][2] = 2
                bauxite_count = []
                key_bau_start = key
                key_bau_finish = bauxite_process_cluster(key_bau_start)
                # number of occurrences in the scheme
                for key_bau_clust in Scheme_process:
                    if Scheme_process[key_bau_clust][5] == 65:
                        bauxite_count.append(key_bau_clust)

                # print('===================', key_bau_start, key_bau_finish, '===================')
                with bau_fuel_graph.subgraph(name=str(dict_of_cluster[key_parent][0]),
                                             edge_attr={'arrowhead': "diamond", 'arrowtail': "odiamond",
                                                        'arrowsize': "0.5", 'dir': "both"}) as node_cluster:
                    node_cluster.attr(fontname="Comic Sans MS", fontsize='12',
                                      label=str(dict_of_cluster[key_parent][1]), style='rounded, filled',
                                      color='gray10', concentrate='true', fillcolor="gray80:gray90",
                                      gradientangle='315')

                    node_cluster.node('cl_node_65_' + str(Scheme_process[key_bau_start][0]),
                                      label_construct_new(key_bau_start, Scheme_process_gen_amt[65]))

                    with node_cluster.subgraph(name='W_gr_64') as waste_node:
                        waste_node.attr(label='', rank='same')
                        waste_node.node('cl_node_64_' + str(Scheme_process[key_bau_start + 1][0]),
                                        label_construct_new(key_bau_start + 1, Scheme_process_gen_amt[64]))

                        label_waste = label_construct_waste(Scheme_process[key_bau_start + 1][1],
                                                            Scheme_process_gen_amt[64],
                                                            Scheme_process[key_bau_start + 1][4],
                                                            Scheme_process[key_bau_start + 1][3])

                        waste_node.node('cl_w_node_64', label_waste)
                        waste_node.edge('cl_node_64_' + str(Scheme_process[key_bau_start + 1][0]), 'cl_w_node_64',
                                        _attributes={'arrowtail': "odot", 'arrowhead': "odot",
                                                     'arrowsize': "0.5", 'dir': "both"})

                    for key_bau_clust in range(key_bau_start + 2, key_bau_finish):
                        if Scheme_process[key_bau_clust][5] == 9:
                            break
                        prod_bau = 0
                        for bau_am in bauxite_count:
                            prod_bau += Scheme_process[bau_am + key_bau_clust - key_bau_start][2]

                        if Scheme_process[key_bau_clust][5] == 56:
                            color_node = dict_of_color[Scheme_process[key_bau_clust][6]]
                            middle_node_bau = edge_label_not_oil(round(prod_bau, 2), color_node, image=True,
                                                                 id_prod_fun=Scheme_process[key_bau_clust][5])
                            node_cluster.node('cl_node_' + str(Scheme_process[key_bau_clust][5]) + '_'
                                              + str(Scheme_process[key_bau_clust][0]), str(middle_node_bau))

                        else:
                            Scheme_process_gen_amt[Scheme_process[key_bau_clust][5]] -= prod_bau

                            node_cluster.node('cl_node_' + str(Scheme_process[key_bau_clust][5]) + '_'
                                              + str(Scheme_process[key_bau_clust][0]),
                                              label_construct_new(key_bau_clust, prod_bau))

                    for key_bau_clust in range(key_bau_start, key_bau_finish):
                        if Scheme_process[key_bau_clust][5] == 9 or Scheme_process[key_bau_clust][5] == 4:
                            continue
                        elif Scheme_process[key_bau_clust][5] == 65:
                            ind_bau = 0
                            continue
                        elif Scheme_process[key_bau_clust][5] == 56:
                            pass
                        else:
                            ind_bau += 1
                            list_of_exception_key.append(key_bau_clust)
                        node_cluster.edge('cl_node_' + str(Scheme_process[key_bau_clust][5]) + '_' +
                                          str(Scheme_process[key_bau_clust][0]) + ':here',
                                          'cl_node_' + str(Scheme_process[Scheme_process[key_bau_clust][0]][5]) + '_' +
                                          str(Scheme_process[Scheme_process[key_bau_clust][0]][0]) +
                                          ':here', _attributes={'arrowhead': "diamond", 'arrowtail': "none",
                                                                'dir': "both"})
                    dict_of_check_key[key_parent] = ind_bau

        else:
            continue

    # --- Edge Cluster ---
    """Creating links between the nodes of the left side scheme. For other minor communication schemes, already created"""

    helper_node_edge = 0
    for key in dict_of_cluster:
        if key == 43 or key == 44 or key == 39 or key == 65:
            continue
        if dict_of_cluster[key][2] == 1:
            if helper_node_edge != 0:
                clust.edge('cl_node_' + str(key) + ':here', 'cl_node_' + str(helper_node_edge) + ':here',
                           directed="false", _attributes={'style': "invis"})
            helper_node_edge = key

    # --- Make Nodes ---
    """Create a central schema"""

    with s_node.subgraph(name='cluster_main_scheme') as main_node:
        main_node.attr(fontname="Comic Sans MS", fontsize='12', label="Scheme of production", style='filled, rounded',
                       concentrate='true', color='gray10', fillcolor="gray80:gray90", gradientangle='315')
        for key in Scheme_process:
            key_parent = int(Scheme_process[key][5])
            if key in list_of_exception_key:
                continue
            elif key_parent in list_of_repeat:
                pass
            elif Scheme_process[key][4] != 0 and key_parent not in dict_of_cluster:
                with main_node.subgraph(name='W_gr_' + str(key_parent)) as waste_node:
                    waste_node.attr(label='', rank='same')
                    waste_node.node('node_' + str(key_parent),
                                    label_construct_new(key, Scheme_process_gen_amt[key_parent]))
                    label_waste = label_construct_waste(Scheme_process[key][1], Scheme_process_gen_amt[key_parent],
                                                        Scheme_process[key][4], Scheme_process[key][3])
                    waste_node.node('w_node_' + str(key_parent), label_waste)
                    waste_node.edge('node_' + str(key_parent), 'w_node_' + str(key_parent),
                                    _attributes={'arrowtail': "odot", 'arrowhead': "odot",
                                                 'arrowsize': "0.5", 'dir': "both"})
                    list_of_repeat.append(key_parent)
            elif key_parent not in dict_of_cluster:
                main_node.node('node_' + str(key_parent),
                               label_construct_new(key, round(Scheme_process_gen_amt[key_parent], 2)))
                list_of_repeat.append(key_parent)

            # --- Make Edge ---

            if key == 0:
                continue

            key_child = Scheme_process[Scheme_process[key][0]][5]
            key_item = str(key_parent) + '_' + str(key_child)

            if Scheme_process[key][6] == 0 and (Scheme_process[key][5] != 44 and Scheme_process[key][5] != 43):
                color_node = str(dict_of_color_raw_mat[Scheme_process[key][5]])
                color_edge = str(dict_of_color_raw_mat[Scheme_process[key][5]]).replace('"', '')
            else:
                color_node = str(dict_of_color[Scheme_process[key][6]])
                color_edge = str(dict_of_color[Scheme_process[key][6]]).replace('"', '')

            if key_item not in dict_of_prod:
                dict_of_prod[key_item] = Scheme_process[key][2]
            else:
                dict_of_prod[key_item] += Scheme_process[key][2]

            if key_parent not in dict_of_cluster:
                middle_node_label = edge_label_not_oil(round(dict_of_prod[key_item], 2), color_node, image=False,
                                                       id_prod_fun=key_parent)
                main_node.node('node_' + str(key_parent) + '_' + str(key_child), str(middle_node_label))
                style_edge = 'solid'
                port_1 = ':in'
                port_2 = ':out'

                s_node.edge('node_' + str(key_parent) + ':here',
                            'node_' + str(key_parent) + '_' + str(key_child) + str(port_1),
                            _attributes={'arrowhead': "none", 'arrowtail': "none", 'style': str(style_edge),
                                         'dir': "both", 'color': str(color_edge)})

                s_node.edge('node_' + str(key_parent) + '_' + str(key_child) + str(port_2),
                            'node_' + str(key_child) + ':here',
                            _attributes={'arrowhead': "diamond", 'arrowtail': "none",
                                         'dir': "both", 'color': str(color_edge)})
            elif key_child not in dict_of_cluster:
                middle_node_label = edge_label_not_oil(round(dict_of_prod[key_item], 2), color_node, image=True,
                                                       id_prod_fun=key_parent)
                main_node.node('node_' + str(key_parent) + '_' + str(key_child), str(middle_node_label))
                port_1 = ':here'
                port_2 = ':here'
                style_edge = 'solid'

                main_node.edge('node_' + str(key_parent) + '_' + str(key_child) + str(port_2),
                               'node_' + str(key_child) + ':here',
                               _attributes={'arrowhead': "diamond", 'arrowtail': "odiamond",
                                            'dir': "both", 'color': str(color_edge)})

        """with main_node.subgraph(name='legend') as legend_node:
            legend_node.attr(style='rounded, filled', rank='max')

            main_node.node('legend_start', label='Legend', _attributes={'style': "filled", 'shape': "ellipse"})
            main_node.edge('legend_start', 'node_' + str(Scheme_process[0][5]), _attributes={'style': "invis"})

            helper_node_edge = 0
            for ind_equip in dict_of_equip:
                if dict_of_equip[ind_equip][0] is True:
                    if ind_equip > 9:
                        node_width = 1.2
                    else:
                        node_width = 1.2
                    legend_node.node('legend_node_' + str(ind_equip), label=str(dict_of_equip[ind_equip][1]),
                                     _attributes={'fillcolor': str(dict_of_color[ind_equip]).replace('"', ''),
                                                  'style': "filled, rounded", 'shape': "diamond",
                                                  'width': str(node_width), 'fontsize': "6pt"})
                    if helper_node_edge != 0:
                        legend_node.edge('legend_node_' + str(ind_equip), 'legend_node_' + str(helper_node_edge),
                                         _attributes={'style': "bold", 'arrowhead': "none"})
                    helper_node_edge = ind_equip
            legend_node.edge('legend_node_' + str(helper_node_edge), 'legend_start', _attributes={'style': "invis"})"""

    """Create scheme 'Raw Materials'"""
    with top_graph.subgraph(name="cluster_total") as total_node:
        total_node.attr(label="Raw Materials", style='rounded, filled', fontname="Comic Sans MS", fontsize='12',
                        color='gray10', fillcolor="gray80:gray90", gradientangle='315')
        helper_node_edge = 0
        for ind in range(1, 13):
            if Scheme_rawmat[ind] != 0:
                total_node.node('tn_' + str(ind), label=label_construct_raw_mat(ind, Scheme_rawmat[ind]))
                if helper_node_edge != 0:
                    total_node.edge('tn_' + str(ind), 'tn_' + str(helper_node_edge), _attributes={'style': "invis"})
                helper_node_edge = ind

    """Create node 'Energy'"""
    if type_work == 2:
        with top_graph.subgraph(name='cluster_energy_total') as energy_node:
            energy_node.attr(rank='same', label='Energy', style='rounded, filled', fontname="Comic Sans MS",
                             fontsize='12', color='gray10', fillcolor="gray80:gray90", gradientangle='315')
            energy_node.node('energy_node', label=str(energy_node_label()))
            top_graph.edge('energy_node', 'tn_' + str(helper_node_edge), _attributes={'style': "invis"})

    """Schematic rendering"""
    s_node.render(filename='Scheme_render.gv', format='png', view=False, renderer='cairo', cleanup=True, outfile='temp\Scheme_render.png')
    clust.render(filename='clust.gv', format='png', view=False, renderer='cairo', cleanup=True, outfile='temp\Clust.png')
    oil_graph.render(filename='oil_graph.gv', format='png', view=False, renderer='cairo', cleanup=True, outfile='temp\Oil_graph.png')
    bau_fuel_graph.render(filename='bau_fuel.gv', format='png', view=False, renderer='cairo', cleanup=True, outfile='temp\Bau_fuel.png')
    top_graph.render(filename='bau_fuel.gv', format='png', view=False, renderer='cairo', cleanup=True, outfile='temp\Top_graph.png')






