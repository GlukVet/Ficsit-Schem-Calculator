import sqlite3
import PySimpleGUI as sg
import graphviz
import os
import shutil
from PIL import Image
from PySimpleGUI import RELIEF_SUNKEN, RELIEF_FLAT, RELIEF_GROOVE
try:
    from bite64_icons_GUI import *
except ImportError:
    pass


# --- GUI Module ---
def type_work_conversion(mode):

    """Сhoice between 'Automated' and 'Handicraft'"""

    if mode is True:
        type_work_fun = 2
    else:
        type_work_fun = 1
    return type_work_fun


def amount_conversion(amount_fun, mode):

    """Conversion into integer format for handicraft mode"""

    if mode is False:
        amount_fun = int(amount_fun)
    return amount_fun


def find_id_from_name(name):

    """Search id by name in the database"""

    name = str(name).replace(' ', '_')
    cursor = satisfactory_db.cursor()

    id_prod_fun = cursor.execute("SELECT id_rmp FROM Raw_mat_and_products WHERE name = :name",
                                 {'name': name}).fetchone()
    cursor.close()
    return id_prod_fun


def popup_window(message_popup, DARK_HEADER_COLOR, BORDER_COLOR):

    """Pop-up window when there is a problem"""

    sg.set_options(auto_size_buttons=True, border_width=1, button_color=sg.COLOR_SYSTEM_DEFAULT)

    if str(message_popup).count('amount') > 0:
        k_popup = 20
    else:
        k_popup = 5

    block_baner_popup = [
        [sg.T('', background_color=DARK_HEADER_COLOR, font='Any 20', size=(20, 60), justification='c')]]
    block_top_popup = [
        [sg.T('Attention!', font='Any 20', size=(20, 0), justification='c')],
        [sg.VPush()],
        [sg.HorizontalSeparator(color=BORDER_COLOR, pad=((5, 20), 0))],
        [sg.VPush()],
        [sg.T(str(message_popup), font='Any 12', justification='c', size=(34, 0))]
    ]
    block_button_popup = [[sg.Button('OK', button_color=(BORDER_COLOR, 'DarkOrange1'), size=(10, 0), font='Any 15', pad=((100, 100), (5, 5)))]]

    layout_popup = [
        [sg.Column(block_baner_popup, size=(320, 30), background_color=DARK_HEADER_COLOR)],
        [sg.Column(block_top_popup, size=(320, 85 + k_popup))],
        [sg.Column(block_button_popup, size=(320, 50), background_color='#444444')]
    ]

    window_popup = sg.Window('Attention', layout_popup, margins=(0, 0), background_color=BORDER_COLOR, keep_on_top=True,
                             no_titlebar=True, grab_anywhere=True, finalize=True, modal=True, alpha_channel=0.98)

    while True:  # Event Loop
        event, values = window_popup.read()
        if event == sg.WINDOW_CLOSED or event == 'OK':
            break
    window_popup.close()


def layout_progress_bar(DARK_HEADER_COLOR, BORDER_COLOR):

    """Progress bar layout"""

    block_baner_popup = [
        [sg.T('', background_color=DARK_HEADER_COLOR, font='Any 20', size=(20, 60), justification='c')]]
    block_top_popup = [
        [sg.T('Please Stand By!', font='Any 20', size=(20, 0), justification='c')],
        [sg.VPush()],
        [sg.HorizontalSeparator(color=BORDER_COLOR, pad=((5, 20), 0))],
        [sg.VPush()],
        [sg.T('Operation in Progress', font='Any 12', justification='c', size=(34, 0), pad=(0, (0, 5)))],
    ]
    block_progress_bar_popup = [[sg.ProgressBar(100, orientation='h', size_px=(306, 30), pad=(5, (4, 2)),
                                                relief=RELIEF_GROOVE, border_width=1,
                                                bar_color=(DARK_HEADER_COLOR, BORDER_COLOR), k='-PROGRESS_BAR-')]]

    layout_progress_bar_popup = [
        [sg.Column(block_baner_popup, size=(320, 30), background_color=DARK_HEADER_COLOR)],
        [sg.Column(block_top_popup, size=(320, 85))],
        [sg.Column(block_progress_bar_popup, size=(320, 45), background_color='#444444')]
    ]
    return layout_progress_bar_popup


def window_save_as(DARK_HEADER_COLOR, BORDER_COLOR, TEXT_INPUT):
    working_directory = os.getcwd()

    sg.set_options(auto_size_buttons=True, border_width=1, button_color=sg.COLOR_SYSTEM_DEFAULT)

    block_baner_popup = [
        [sg.T('', background_color=DARK_HEADER_COLOR, font='Any 20', size=(20, 60), justification='c')]
    ]

    block_top_popup = [
        [sg.T('Do you want to save the scheme?', font='Any 16', justification='c', pad=((80, 80), 5))],
        [sg.VPush()],
        [sg.HorizontalSeparator(color=BORDER_COLOR, pad=((5, 10), 0))],
        [sg.VPush()]
    ]
    block_button_popup = [
        [sg.InputText(enable_events=True, key='-PATH-', size=(52, 15), disabled_readonly_text_color=TEXT_INPUT,
                      disabled_readonly_background_color=BORDER_COLOR, readonly=True),
         sg.SaveAs(button_text='Browser', initial_folder=working_directory, k='-SAVE_AS-', button_color=("#e8bb4e", BORDER_COLOR),
                   file_types=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("TIFF", "*.tiff")], default_extension="*.png")],
        [sg.VPush()],
        [sg.Submit(disabled=True, size=(15, 0), button_color=(BORDER_COLOR, 'DarkOrange1')),
         sg.Cancel(k='-CANCEL_SAVE_AS-', size=(8, 0), button_color=(BORDER_COLOR, 'OrangeRed2'))]
    ]

    layout_popup_save_as = [
        [sg.Column(block_baner_popup, size=(480, 30), background_color=DARK_HEADER_COLOR)],
        [sg.Column(block_top_popup, size=(480, 40))],
        [sg.Column(block_button_popup, size=(480, 80))]
    ]

    window = sg.Window('Scheme Ready', layout=layout_popup_save_as, background_color=BORDER_COLOR, no_titlebar=True,
                       grab_anywhere=True, finalize=True, alpha_channel=0.9, use_custom_titlebar=False, modal=True,
                       keep_on_top=True, location=(0, 0))
    while True:
        event, values = window.read()
        if values['-PATH-'] != '':
            window['Submit'].update(disabled=False)
        if event == '-CANCEL_SAVE_AS-' or event == sg.WINDOW_CLOSED:
            img_folder = None
            break
        elif event == 'Submit':
            img_folder = values['-PATH-']
            break

    window.close()
    return img_folder


def window_help(DARK_HEADER_COLOR, BORDER_COLOR):
    sg.set_options(auto_size_buttons=True, border_width=1, button_color=sg.COLOR_SYSTEM_DEFAULT)

    block_baner_popup = [[sg.T('', background_color=DARK_HEADER_COLOR, font='Any 20', size=(20, 60), justification='c')]]
    block_top_popup = [[sg.Image(Help, background_color=BORDER_COLOR, pad=((0, 2), 0))]]
    block_button_popup = [[sg.Button('OK', button_color=(BORDER_COLOR, 'DarkOrange1'), size=(10, 0), font='Any 15',
                                     pad=((420, 0), (5, 5)))]]

    layout_popup = [
        [sg.Column(block_baner_popup, size=(960, 30), background_color=DARK_HEADER_COLOR)],
        [sg.Column(block_top_popup, size=(960, 540), background_color=BORDER_COLOR)],
        [sg.Column(block_button_popup, size=(960, 50))]
    ]

    window_popup = sg.Window('Help', layout_popup, margins=(0, 0), background_color=BORDER_COLOR, keep_on_top=True,
                             no_titlebar=True, grab_anywhere=True, finalize=True, modal=True, alpha_channel=0.98)

    while True:  # Event Loop
        event, values = window_popup.read()
        if event == sg.WINDOW_CLOSED or event == 'OK':
            break
    window_popup.close()


def minimize_main_window(main_window):
    """
    Creates an icon on the taskbar that represents your custom titlebar window.
    The FocusIn event is set so that if the user restores the window from the taskbar.
    If this window is closed by right clicking on the icon and choosing close, then the
    program will exit just as if the "X" was clicked on the main window.
    """

    """Taken from GitHub PySimpleGUI"""

    main_window.hide()
    layout = [[sg.T('This is your window with a customized titlebar... you just cannot see it')]]
    window = sg.Window(main_window.Title, layout, finalize=True, alpha_channel=0)
    window.minimize()
    window.bind('<FocusIn>', '-RESTORE-')
    # store the dummy window as a function property
    minimize_main_window.dummy_window = window


def restore_main_window(main_window):
    """
    Call this function when you want to restore your main window
    :param main_window:
    :return:
    """

    """Taken from GitHub PySimpleGUI"""

    if hasattr(minimize_main_window, 'dummy_window'):
        minimize_main_window.dummy_window.close()
        minimize_main_window.dummy_window = None
    main_window.un_hide()


# --- Search Recipe Module ---
def search_recipe(id_prod_fun, requirements_fun, sql_quarry_fun, amount_fun, type_work_fun, mother_key):

    """The purpose of this function is to fill in the "Scheme_process" dictionary
    in order to build a scheme based on it."""

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

    # dict_of_equip[Scheme_process[int(Seq_key[-1])][6]][0] = True

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

    if id_prod_fun not in Scheme_process_gen_amt:
        Scheme_process_gen_amt[int(id_prod_fun)] = round(amount_input_fun, 2)
    else:
        Scheme_process_gen_amt[int(id_prod_fun)] = round(amount_input_fun + Scheme_process_gen_amt[int(id_prod_fun)], 2)


def append_to_dict_of_surplus(id_prod_fun):

    """Calculation of the remaining products for the mode 'Handicraft'"""

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

    if id_prod_fun in (13, 19, 23, 53, 55, 56):
        #  {id_prod: (index_requirements, id_recipe)}
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


# --- Graph Module ---
def graph_system_path():

    """For the Graphviz module to work, you need to make an entry in the path"""
    os.environ['PATH'] += os.getcwd() + "/bin_graphviz"

    return


def energy_node_label():

    """single node label 'Energy' """

    label_fun = '<<TABLE border="0" cellpadding="5"><TR><TD><IMG SCALE="true" SRC="icons/Energy.png"/></TD></TR>' \
                '<TR><TD border="1" STYLE="rounded" BGCOLOR="darkorange1">' \
                'Total Energy:<BR/>' + str(round(MJ_Total[0])) + '  MJ</TD></TR></TABLE>>'
    return label_fun


def bauxite_process_cluster(key_start_fun):

    """Defines the processing of bauxite"""

    list_of_bau = [key_start_fun]
    key_fun = key_start_fun + 1
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

    """Label for small intermediate nodes (not for fuel)"""

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

    """Label for nodes in the cluster 'Oil Refining' """

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

    cursor = satisfactory_db.cursor()
    k_mj = cursor.execute('SELECT MJ FROM Equipment WHERE id_equip = :id_eq_fun', {'id_eq_fun': id_eq_fun}).fetchone()
    cursor.close()
    mj = round((float(amount_prod_fun) * int(circle_dur_fun) / (60 * float(out_prod_fun)) * float(k_mj[0])), 2)
    if is_cluster is False:
        MJ_Total[0] += mj
    return mj


def label_construct_new(ind_fun, amount_prod_fun, is_cluster=False):

    """Label for large node"""

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

    w_dir = os.getcwd() + "/temp_sacalkscheme"

    """Schematic rendering"""
    s_node.render(filename='Scheme_render.gv', format='png', view=False, renderer='cairo', cleanup=True, outfile=w_dir + '\Scheme_render.png')
    clust.render(filename='clust.gv', format='png', view=False, renderer='cairo', cleanup=True, outfile=w_dir + '\Clust.png')
    oil_graph.render(filename='oil_graph.gv', format='png', view=False, renderer='cairo', cleanup=True, outfile=w_dir + '\Oil_graph.png')
    bau_fuel_graph.render(filename='bau_fuel.gv', format='png', view=False, renderer='cairo', cleanup=True, outfile=w_dir + '\Bau_fuel.png')
    top_graph.render(filename='bau_fuel.gv', format='png', view=False, renderer='cairo', cleanup=True, outfile=w_dir + '\Top_graph.png')


# --- Image Constructor Module ---
def image_constructor():

    """The task of the function is to combine five rendered schemes into one"""

    size_total_img = [0, 0]
    w_dir = os.getcwd() + "/temp_sacalkscheme"

    with Image.open(w_dir + "\Clust.png") as left_img:
        left_img.load()
        left_img_size = left_img.size
    with Image.open(w_dir + "\Scheme_render.png") as centre_img:
        centre_img.load()
        centre_img_size = centre_img.size
    with Image.open(w_dir + "\Bau_fuel.png") as right_img:
        right_img.load()
        right_img_size = right_img.size
    with Image.open(w_dir + "\Oil_graph.png") as under_img:
        under_img.load()
        under_img_size = under_img.size
    with Image.open(w_dir + "\Top_graph.png") as top_img:
        top_img.load()
        top_img_size = top_img.size

    """Determining the Width and Height of Merged Schemas Based on Their Dimensions"""
    if Scheme_process[0][5] in (13, 19, 53, 55, 56, 23, 24):
        size_total_img[0] = max(left_img_size[0], top_img_size[0])
        size_total_img[1] = left_img_size[1] + top_img_size[1]
        var = None
    elif centre_img_size[1] < 0.75 * under_img_size[1]:
        var = True
        size_total_img[0] += left_img_size[0]
        if centre_img_size[0] < under_img_size[0]:
            size_total_img[0] += max(under_img_size[0], top_img_size[0]) + right_img_size[0]
        else:
            size_total_img[0] += max(centre_img_size[0], top_img_size[0], centre_img_size[0] + right_img_size[0])
        size_total_img[1] = under_img_size[1] + top_img_size[1] + centre_img_size[1]
        var_bau = None
    else:
        var = False
        if under_img_size[1] >= right_img_size[1]:
            if under_img_size[1] == right_img_size[1]:
                var_bau = None
            else:
                var_bau = True
            size_total_img[0] += left_img_size[0] + max(centre_img_size[0], top_img_size[0], right_img_size[0],
                                                        right_img_size[0] + centre_img_size[0]) + under_img_size[0]
            size_total_img[1] = max(left_img_size[1], centre_img_size[1], right_img_size[1], under_img_size[1]) + top_img_size[1]
        else:
            var_bau = False
            size_total_img[0] += left_img_size[0] + max(top_img_size[0], centre_img_size[0] + under_img_size[0], centre_img_size[0] + right_img_size[0])
            size_total_img[1] = max(left_img_size[1], centre_img_size[1], right_img_size[1] + under_img_size[1]) + top_img_size[1]

    """Create a blank canvas"""
    total_img = Image.new('RGB', (size_total_img[0], size_total_img[1]), '#7f7f7f')

    """Layout"""
    if var is None:
        total_img.paste(top_img, (0, 0))
        if top_img_size < left_img_size:
            total_img.paste(left_img, (0, top_img_size[1]))
        else:
            total_img.paste(left_img, (top_img_size[0] - left_img_size[0], top_img_size[1]))
    else:
        total_img.paste(left_img, (0, top_img_size[1]))
        total_img.paste(top_img, (left_img_size[0], 0))
        total_img.paste(centre_img, (left_img.size[0], top_img_size[1]))
        if var is False:
            if var_bau is True:
                total_img.paste(under_img, (left_img_size[0] + centre_img_size[0], top_img_size[1]))
                total_img.paste(right_img, (left_img_size[0] + centre_img_size[0] + under_img_size[0], top_img_size[1]))
            elif var_bau is False:
                total_img.paste(right_img, (left_img_size[0] + centre_img_size[0], top_img_size[1]))
                total_img.paste(under_img, (left_img_size[0] + centre_img_size[0], top_img_size[1] + right_img_size[1]))
            else:
                pass
        else:
            total_img.paste(under_img, (left_img_size[0], top_img_size[1] + centre_img_size[1]))
            total_img.paste(right_img, (left_img_size[0] + max(centre_img_size[0], under_img_size[0]), top_img_size[1]))

    total_img.show()
    return total_img


def image_save(img_folder, total_img):

    """Saving the schema if needed"""

    if img_folder is None:
        return
    total_img.save(img_folder)
    return


# =====================================================================================================================
"""Database connection"""
try:
    satisfactory_db = sqlite3.connect('database/Satisfactory_DB.db')
    print("SQLite connection open")
    database_find = True
except sqlite3.Error as error:
    print("Error connecting to sqlite", error)
    satisfactory_db.close()
    database_find = False

"""Create folder for temporary files"""
try:
    os.mkdir("temp_sacalkscheme")
except FileExistsError:
    pass
# =====================================================================================================================
"""Working materials"""

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
dict_of_cheap_mat = {13: (1, 1), 19: (2, 19), 23: (3, 29), 53: (7, 95), 55: (8, 99), 56: (8, 101)}
Scheme_rawmat = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
dict_of_color = {0: '"gray"', 1: '"deepskyblue"', 2: '"deeppink"', 3: '"green2"', 4: '"firebrick1"',
                 6: '"darkorchid1"', 7: '"darkslategray2"', 8: '"lightcoral"', 9: '"darkgoldenrod2"',
                 10: '"aquamarine"', 11: '"aquamarine"', 12: '"khaki1"'}
dict_of_color_raw_mat = {1: '"blue"', 2: '"brown4"', 3: '"crimson"', 4: '"tan"', 5: '"azure4"', 6: '"yellow"',
                         7: '"x11purple"', 8: '"gold"', 9: '"violet"', 10: '"tomato1"', 11: '"gray"',
                         12: '"springgreen2"'}
list_of_repeat = []
MJ_Total = [0]

total_img = None

list_of_exception_key = []
dict_of_check_key = {}
dict_of_prod = {}

dict_of_equip = {1: [False, 'Constructor'], 2: [False, 'Smelter'], 3: [False, 'Assembler'],
                 4: [False, 'Foundry'],
                 6: [False, 'Refinery'], 7: [False, 'Packager'], 8: [False, 'Manufacturer'],
                 9: [False, 'Blender'],
                 10: [False, 'Particle Accelerator'], 11: [False, 'Particle Accelerator'],
                 12: [False, 'Nuclear Power Plant']}
# =====================================================================================================================
"""Formation of a list of products and checking for the presence of image files"""
if database_find is True:
    cursor = satisfactory_db.cursor()
    Choose_list = cursor.execute("SELECT name FROM Raw_mat_and_products WHERE is_product = 1 ORDER BY name").fetchall()
    Folder_list = cursor.execute("SELECT image FROM Raw_mat_and_products").fetchall()
    cursor.close()
    for ind_list in range(len(Choose_list)):
        Choose_list[ind_list] = str(Choose_list[ind_list]).replace('_', ' ')
        Choose_list[ind_list] = str(Choose_list[ind_list]).translate({ord(iterat): None for iterat in "[](),'"})
        img_find = True
    img_find = True
    for list_elem in Folder_list:
        if os.path.exists(list_elem[0]) is False:
            print(list_elem)
            img_find = False
    if os.path.exists("icons\Energy.png") is False:
        img_find = False
else:
    img_find = False

"""Permission to activate the button 'Calculate Scheme'"""
if database_find is True and img_find is True:
    scheme_but_enable = False
else:
    scheme_but_enable = True
# =====================================================================================================================
"""Formation of the main window"""
requirements = ()

theme_dict = {'BACKGROUND': '#444444',
              'TEXT': '#fdcb52',
              'INPUT': '#2e2e2e',
              'TEXT_INPUT': '#fdcb52',
              'SCROLL': '#705e52',
              'BUTTON': ('#000000', '#fdcb52'),
              'PROGRESS': ('#FFFFFF', '#C7D5E0'),
              'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}

sg.LOOK_AND_FEEL_TABLE['Satisfactory'] = theme_dict
sg.theme('Satisfactory')
sg.set_options(auto_size_buttons=True, border_width=1, button_color=sg.COLOR_SYSTEM_DEFAULT)

BORDER_COLOR = '#2e2e2e'
DARK_HEADER_COLOR = '#b05701'
BPAD_TOP = ((22, 20), (20, 10))
BPAD_LEFT = ((22, 10), (0, 0))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT = ((10, 20), (0, 0))
BPAD_BUTTON = ((22, 20), (10, 10))
SLIDER_PAD = (10, 0)

block_Iron = [[sg.Image(data=iron_icon)], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-IRON-', pad=SLIDER_PAD)]]
block_Copper = [[sg.Image(data=copper_icon)], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-COPPER-', pad=SLIDER_PAD)]]
block_Lime = [[sg.Image(data=lime_icon)], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-LIME-', pad=SLIDER_PAD)]]
block_Coal = [[sg.Image(data=coal_icon)], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-COAL-', pad=SLIDER_PAD)]]
block_Sulf = [[sg.Image(data=sulf_icon)], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-SULF-', pad=SLIDER_PAD)]]
block_Oil = [[sg.Image(data=oil_icon)], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-OIL-', pad=SLIDER_PAD)]]
block_Catr = [[sg.Image(data=caterium_icon)], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-CATR-', pad=SLIDER_PAD)]]
block_Quartz = [[sg.Image(data=quartz_icon)], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-QUARTZ-', pad=SLIDER_PAD)]]
block_Baux = [[sg.Image(data=bauxite_icon)], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-BAUX-', pad=SLIDER_PAD)]]
block_Nitro = [[sg.Image(data=nitro_icon)], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-NITRO-', pad=SLIDER_PAD)]]
block_Uran = [[sg.Image(data=uran_icon)], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-URAN-', pad=SLIDER_PAD)]]

tc = "#fdcb52"
bc = BORDER_COLOR
title = "Ficsit Scheme Calculator"

title_bar = [sg.Col([[sg.T(text="", text_color=tc, background_color=bc)]], pad=(0, 0), background_color=bc),
         sg.Col([[sg.T('_', text_color=tc, background_color=bc, enable_events=True, key='-MINIMIZE-'),
         sg.Text('❎', text_color=tc, background_color=bc, enable_events=True, key='-EXIT_X-')]], element_justification='r', key='-TITLEBAR-',
                pad=(0, 0), background_color=bc)]

top_banner = [[sg.Image(Ficsit_icon_1, background_color=BORDER_COLOR)]]

top = [[sg.Text('Welcome to the Ficsit Scheme Calculator', size=(55, 0), justification='c', pad=BPAD_TOP, font='Any 20')]]

block_3 = [[sg.Text('Resource Сonsumption\n', font='Any 16')],
           [sg.Push(), sg.Column(block_Iron), sg.VerticalSeparator(color=BORDER_COLOR),
            sg.Column(block_Copper), sg.VerticalSeparator(color=BORDER_COLOR),
            sg.Column(block_Lime), sg.VerticalSeparator(color=BORDER_COLOR),
            sg.Column(block_Coal), sg.VerticalSeparator(color=BORDER_COLOR),
            sg.Column(block_Sulf), sg.VerticalSeparator(color=BORDER_COLOR),
            sg.Column(block_Oil), sg.VerticalSeparator(color=BORDER_COLOR),
            sg.Column(block_Catr), sg.VerticalSeparator(color=BORDER_COLOR),
            sg.Column(block_Quartz), sg.VerticalSeparator(color=BORDER_COLOR),
            sg.Column(block_Baux), sg.VerticalSeparator(color=BORDER_COLOR),
            sg.Column(block_Nitro), sg.VerticalSeparator(color=BORDER_COLOR),
            sg.Column(block_Uran)]
           ]

block_2 = [
    [sg.Text('Product', font='Any 16')],
    [sg.Text('Select product', font='Any 10', size=(11, 1)),
     sg.Input(size=(35, 1), enable_events=True, key='-IN-')],
    [sg.pin(sg.Col([[sg.Listbox(values=[], size=(35, 10), enable_events=True, key='-BOX-',
                                select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, no_scrollbar=True)]],
                   key='-BOX-CONTAINER-', pad=(103, 0), visible=False))],
    [sg.VPush()],
    # [sg.HorizontalSeparator(color=BORDER_COLOR)],
    [sg.VPush()],
    [sg.Text('Amount', font='Any 10', size=(11, 1)), sg.Input(size=(35, 1), key="-AMOUNT-", enable_events=True),
     sg.StatusBar(text="per/min", k='-MODE_STATUS-', relief=RELIEF_FLAT)]
]

block_4 = [
    [sg.Text('Additional Settings', font='Any 16')],
    [
        sg.Frame('Working Mode',
                 [[sg.R("Automated", group_id='-WK-', default=True, size=10, k='-MODE-', enable_events=True)],
                  [sg.R('Handicraft', group_id='-WK-', size=10, k='-MODE-', enable_events=True)]
                  ], relief=RELIEF_SUNKEN, size=(180, 80), font='Any 10'),
        sg.Frame('Oil Level', [[sg.Slider(range=(0, 3), orientation='h', default_value=3, relief=RELIEF_GROOVE,
                                          trough_color=BORDER_COLOR, k='-OIL_LEVEL-', enable_events=True)]],
                 vertical_alignment='t', relief=RELIEF_SUNKEN, size=(210, 80), font='Any 10')]
]

block_5 = [
    [sg.Button('Calculate Scheme', button_color=(BORDER_COLOR, 'DarkOrange1'), font='Any 15', size=(20, 0), pad=(10, (5, 5)), key='-START-',
               disabled=scheme_but_enable),
     sg.Button('Help', button_color=(BORDER_COLOR, 'DarkOrange1'), font='Any 15', size=(10, 0), pad=((410, 0), (5, 5)), key='-HELP-'),
     sg.Button('Exit', button_color=(BORDER_COLOR, 'OrangeRed2'), font='Any 15', size=(10, 0), pad=((10, 0), (5, 5)), key='-EXIT-')]

]

layout = [
          [title_bar],
          [sg.Column(top_banner, size=(960, 60), pad=((0, 8), 0), background_color=BORDER_COLOR)],
          [sg.Column(top, size=(920, 90), pad=BPAD_TOP)],
          [sg.Column([[sg.Column(block_2, size=(450, 150), pad=BPAD_LEFT_INSIDE)],
                      ], pad=BPAD_LEFT, background_color=BORDER_COLOR),
           sg.Column(block_4, size=(450, 150), pad=BPAD_RIGHT)],
          [sg.Column(block_3, size=(920, 300), pad=BPAD_BUTTON)],
          [sg.Column(block_5, size=(920, 50), pad=BPAD_BUTTON)]
          ]

window = sg.Window(title, layout, margins=(0, 0), background_color=BORDER_COLOR,
                   no_titlebar=True, grab_anywhere=True, finalize=True, alpha_channel=1, keep_on_top=True,
                   use_custom_titlebar=False, resizable=True, return_keyboard_events=True)

window['-TITLEBAR-'].expand(True, False, False)  # expand the titlebar's rightmost column so that it resizes correctly

list_element: sg.Listbox = window.Element('-BOX-')  # store listbox element for easier access and to get to docstrings
prediction_list, input_text, sel_item = [], "", 0
mode_status = ""
counter = 0

"""System Path"""
graph_system_path()

"""EVENT LOOP"""
while True:
    window_O, event, values = sg.read_all_windows(timeout=1000)
    if database_find is False:
        popup_window('Unable to connect to database', DARK_HEADER_COLOR, BORDER_COLOR)
        database_find = None
        continue
    if img_find is False:
        popup_window('Some files in the icon directory are missing', DARK_HEADER_COLOR, BORDER_COLOR)
        img_find = None
        continue
    if event == '-MINIMIZE-':
        minimize_main_window(window)
        continue
    elif event == '-RESTORE-' or (event == sg.WINDOW_CLOSED and window_O != window):
        restore_main_window(window)
        continue
        # ------ remainder of your "normal" events and window code ------
    counter += 1

    if event == sg.WINDOW_CLOSED or event == '-EXIT-' or event == '-EXIT_X-':
        break
    elif event == '-HELP-':
        window_help(DARK_HEADER_COLOR, BORDER_COLOR)
        continue
    elif event.startswith('Escape'):
        window['-IN-'].update('')
        window['-BOX-CONTAINER-'].update(visible=False)
    elif event.startswith('Down') and len(prediction_list):
        sel_item = (sel_item + 1) % len(prediction_list)
        list_element.update(set_to_index=sel_item, scroll_to_index=sel_item)
    elif event.startswith('Up') and len(prediction_list):
        sel_item = (sel_item + (len(prediction_list) - 1)) % len(prediction_list)
        list_element.update(set_to_index=sel_item, scroll_to_index=sel_item)
    elif event == '\r':
        if len(values['-BOX-']) > 0:
            window['-IN-'].update(value=str(values['-BOX-']).translate({ord(iterat): None for iterat in "[]',"}))
            window['-BOX-CONTAINER-'].update(visible=False)
    elif event == '-IN-':
        text = values['-IN-'].lower()
        if text == input_text:
            continue
        else:
            input_text = text
        prediction_list_count = []
        prediction_list_start = []
        prediction_list = []
        prediction_list_count = [item for item in Choose_list if item.lower().count(text) > 0]
        prediction_list_start = [item for item in Choose_list if item.lower().startswith(text)]

        if len(text) >= 3:
            prediction_list = prediction_list_count
        else:
            prediction_list = prediction_list_start

        list_element.update(values=prediction_list)
        sel_item = 0
        list_element.update(set_to_index=sel_item)

        if len(prediction_list) > 0:
            window['-BOX-CONTAINER-'].update(visible=True)
        else:
            window['-BOX-CONTAINER-'].update(visible=False)
    elif event == '-BOX-':
        window['-IN-'].update(value=str(values['-BOX-']).translate({ord(iterat): None for iterat in "[]',"}))
        window['-BOX-CONTAINER-'].update(visible=False)
    elif event == '-MODE-':
        window['-MODE_STATUS-'].update(value='per/min')
    elif event == '-MODE-0':
        window['-MODE_STATUS-'].update(value='units')
    elif event == '-START-':
        """Validation of input parameters"""
        if values['-IN-'] not in Choose_list:
            popup_window('You have not selected a product', DARK_HEADER_COLOR, BORDER_COLOR)
            continue
        try:
            if str(values['-AMOUNT-']).count(',') > 0:
                values['-AMOUNT-'] = str(values['-AMOUNT-']).replace(',', '.')
            values['-AMOUNT-'] = float(values['-AMOUNT-'])
            if values['-AMOUNT-'] <= 0:
                popup_window('The specified amount of the product\ncannot be reached', DARK_HEADER_COLOR, BORDER_COLOR)
                continue
        except ValueError:
            popup_window('The specified amount of the product\ncannot be reached', DARK_HEADER_COLOR, BORDER_COLOR)
            continue

        window_progress = sg.Window('Operation in Progress', layout=layout_progress_bar(DARK_HEADER_COLOR, BORDER_COLOR),
                                    background_color=BORDER_COLOR, no_titlebar=True, grab_anywhere=True, finalize=True,
                                    alpha_channel=0.9, use_custom_titlebar=False, modal=True, keep_on_top=True, location=(0, 0))

        """Search id by name in the database"""
        id_prod = int(find_id_from_name(values['-IN-'])[0])

        """Formation of a tuple of requirements"""
        requirements = (int(values['-OIL_LEVEL-']), int(values['-IRON-']), int(values['-COPPER-']), int(values['-LIME-']),
                        int(values['-COAL-']), int(values['-SULF-']), int(values['-OIL-']), int(values['-CATR-']),
                        int(values['-QUARTZ-']), int(values['-BAUX-']), int(values['-NITRO-']), int(values['-URAN-']))

        """Formatting the quantity (if necessary) and determining the operating mode"""
        amount = amount_conversion(values['-AMOUNT-'], values['-MODE-'])
        type_work = type_work_conversion(values['-MODE-'])

        window_progress['-PROGRESS_BAR-'].update(1)

        """Fill the "Scheme_process" dictionary"""
        search_recipe(id_prod_fun=id_prod, requirements_fun=requirements, sql_quarry_fun=sql_quarry,
                      amount_fun=amount, type_work_fun=type_work, mother_key=0)

        window_progress['-PROGRESS_BAR-'].update(33)

        """Formation of schemes"""
        scheme_node_new(type_work=type_work, oil_level=requirements[0])

        window_progress['-PROGRESS_BAR-'].update(66)

        """Combining schemas"""
        minimize_main_window(window)
        total_img = image_constructor()

        window_progress['-PROGRESS_BAR-'].update(100)
        window_progress.close()

        """Saving a schema"""
        img_folder = window_save_as(DARK_HEADER_COLOR, BORDER_COLOR, TEXT_INPUT='#fdcb52')
        image_save(img_folder, total_img)
        restore_main_window(window)

        """Reset working materials"""
        Scheme_process = {}
        Scheme_rawmat = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
        MJ_Total = [0]
        Seq_key = [-1]
        Scheme_process_gen_amt = {}
        dict_of_sur = {}
        dict_of_check_key = {}
        list_of_repeat = []
        list_of_exception_key = []
        dict_of_prod = {}
        total_img = None

"""Closing the database and deleting the temporary folder"""
satisfactory_db.close()
window.close()
shutil.rmtree("temp_sacalkscheme")

