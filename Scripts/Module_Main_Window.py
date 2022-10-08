from PySimpleGUI import RELIEF_SUNKEN, RELIEF_FLAT

import Module_Input_Parametrs
from Module_GUI import *
from Module_Search_Recipe import search_recipe
from Module_Graph import scheme_node_new
from Module_Image_Constructor import image_constructor, image_save
from Module_Input_Parametrs import sql_quarry, satisfactory_db


cursor = satisfactory_db.cursor()
Choose_list = cursor.execute("SELECT name FROM Raw_mat_and_products WHERE is_product = 1 ORDER BY name").fetchall()
cursor.close()
for ind_list in range(len(Choose_list)):
    Choose_list[ind_list] = str(Choose_list[ind_list]).replace('_', ' ')
    Choose_list[ind_list] = str(Choose_list[ind_list]).translate({ord(iterat): None for iterat in "[](),'"})

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
# sg.change_look_and_feel('DarkAmber')

BORDER_COLOR = '#2e2e2e'
DARK_HEADER_COLOR = '#b05701'
BPAD_TOP = ((20, 20), (20, 10))
BPAD_LEFT = ((20, 10), (0, 0))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT = ((10, 20), (0, 0))
BPAD_BUTTON = ((20, 20), (10, 10))
SLIDER_PAD = (10, 0)

block_Iron = [[sg.Image(r'icons\mini\iron_icon.png')], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-IRON-', pad=SLIDER_PAD)]]
block_Copper = [[sg.Image(r'icons\mini\copper_icon.png')], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-COPPER-',
              pad=SLIDER_PAD)]]
block_Lime = [[sg.Image(r'icons\mini\lime_icon.png')], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-LIME-', pad=SLIDER_PAD)]]
block_Coal = [[sg.Image(r'icons\mini\coal_icon.png')], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-COAL-', pad=SLIDER_PAD)]]
block_Sulf = [[sg.Image(r'icons\mini\sulf_icon.png')], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-SULF-', pad=SLIDER_PAD)]]
block_Oil = [[sg.Image(r'icons\mini\oil_icon.png')], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-OIL-', pad=SLIDER_PAD)]]
block_Catr = [[sg.Image(r'icons\mini\caterium_icon.png')], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-CATR-', pad=SLIDER_PAD)]]
block_Quartz = [[sg.Image(r'icons\mini\quartz_icon.png')], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-QUARTZ-',
              pad=SLIDER_PAD)]]
block_Baux = [[sg.Image(r'icons\mini\bauxite_icon.png')], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-BAUX-', pad=SLIDER_PAD)]]
block_Nitro = [[sg.Image(r'icons\mini\nitro_icon.png')], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-NITRO-', pad=SLIDER_PAD)]]
block_Uran = [[sg.Image(r'icons\mini\uran_icon.png')], [sg.VPush()], [
    sg.Slider(range=(0, 3), orientation='v', default_value=1, trough_color='#2e2e2e', k='-URAN-', pad=SLIDER_PAD)]]

tc = "#fdcb52"
bc = BORDER_COLOR
title = "Ficsit Scheme Calculator"

title_bar = [sg.Col([[sg.T(text="", text_color=tc, background_color=bc)]], pad=(0, 0), background_color=bc),
         sg.Col([[sg.T('_', text_color=tc, background_color=bc, enable_events=True, key='-MINIMIZE-'),
         sg.Text('❎', text_color=tc, background_color=bc, enable_events=True, key='-EXIT_X-')]], element_justification='r', key='-TITLEBAR-',
                pad=(0, 0), background_color=bc)]

top_banner = [[sg.Image(r'icons\mini\Ficsit_icon_1.png', background_color=BORDER_COLOR)]]

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
    [sg.Button('Calculate Scheme', button_color=(BORDER_COLOR, 'DarkOrange1'), font='Any 15', size=(20, 0), pad=(10, (5, 5)), key='-START-'),
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
                   no_titlebar=True, grab_anywhere=True, finalize=True, alpha_channel=0.9, keep_on_top=False,
                   use_custom_titlebar=False, resizable=True)

window['-TITLEBAR-'].expand(True, False, False)  # expand the titlebar's rightmost column so that it resizes correctly

list_element: sg.Listbox = window.Element('-BOX-')  # store listbox element for easier access and to get to docstrings
prediction_list, input_text, sel_item = [], "", 0
mode_status = ""
counter = 0

while True:  # Event Loop
    window_O, event, values = sg.read_all_windows(timeout=1000)
    print(event, values)
    if event == '-MINIMIZE-':
        minimize_main_window(window)
        continue
    elif event == '-RESTORE-' or (event == sg.WINDOW_CLOSED and window_O != window):
        restore_main_window(window)
        continue
        # ------ remainder of your "normal" events and window code ------
    # window['-IN-'].update(counter)
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
        prediction_list = []
        prediction_list = [item for item in Choose_list if item.lower().count(text) > 0]
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
        if values['-IN-'] not in Choose_list:
            popup_window('You have not selected a product', DARK_HEADER_COLOR, BORDER_COLOR)
            continue
        try:
            if str(values['-AMOUNT-']).count(',') > 0:
                values['-AMOUNT-'] = str(values['-AMOUNT-']).replace(',', '.')
            values['-AMOUNT-'] = float(values['-AMOUNT-'])
        except ValueError:
            popup_window('The specified amount of the product\ncannot be reached', DARK_HEADER_COLOR, BORDER_COLOR)
            continue

        window_progress = sg.Window('Operation in Progress', layout=layout_progress_bar(DARK_HEADER_COLOR, BORDER_COLOR),
                                    background_color=BORDER_COLOR, no_titlebar=True, grab_anywhere=True, finalize=True,
                                    alpha_channel=0.9, use_custom_titlebar=False, modal=True, keep_on_top=False)

        id_prod = int(find_id_from_name(values['-IN-'])[0])

        requirements = (int(values['-OIL_LEVEL-']), int(values['-IRON-']), int(values['-COPPER-']), int(values['-LIME-']),
                        int(values['-COAL-']), int(values['-SULF-']), int(values['-OIL-']), int(values['-CATR-']),
                        int(values['-QUARTZ-']), int(values['-BAUX-']), int(values['-NITRO-']), int(values['-URAN-']))

        amount = amount_conversion(values['-AMOUNT-'], values['-MODE-'])

        type_work = type_work_conversion(values['-MODE-'])

        window_progress['-PROGRESS_BAR-'].update(1)

        search_recipe(id_prod_fun=id_prod, requirements_fun=requirements, sql_quarry_fun=sql_quarry,
                      amount_fun=amount, type_work_fun=type_work, mother_key=0)

        window_progress['-PROGRESS_BAR-'].update(33)

        scheme_node_new(type_work=type_work, oil_level=requirements[0])

        window_progress['-PROGRESS_BAR-'].update(66)

        image_constructor()

        window_progress['-PROGRESS_BAR-'].update(100)

        window_progress.close()

        img_folder = window_save_as(DARK_HEADER_COLOR, BORDER_COLOR, TEXT_INPUT='#fdcb52')

        image_save(img_folder)

        Module_Input_Parametrs.Scheme_process = {}
        Module_Input_Parametrs.Scheme_rawmat = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
        Module_Input_Parametrs.MJ_Total = [0]
        Module_Input_Parametrs.Seq_key = [-1]
        Module_Input_Parametrs.Scheme_process_gen_amt = {}
        Module_Input_Parametrs.dict_of_sur = {}
        Module_Input_Parametrs.dict_of_check_key = {}
        Module_Input_Parametrs.list_of_repeat = []
        Module_Input_Parametrs.list_of_exception_key = []
        Module_Input_Parametrs.total_img = None

satisfactory_db.close()

window.close()





