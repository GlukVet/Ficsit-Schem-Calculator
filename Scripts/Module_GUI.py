import PySimpleGUI as sg
import os
from PySimpleGUI import RELIEF_GROOVE

from Module_Input_Parametrs import satisfactory_db


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

    window_popup = sg.Window('Attention', layout_popup, margins=(0, 0), background_color=BORDER_COLOR, keep_on_top=False,
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
        [sg.T('Do you want to keep the scheme?', font='Any 16', justification='c', pad=((80, 80), 5))],
        [sg.VPush()],
        [sg.HorizontalSeparator(color=BORDER_COLOR, pad=((5, 10), 0))],
        [sg.VPush()]
    ]
    block_button_popup = [
        [sg.InputText(enable_events=True, key='-PATH-', size=(52, 15), disabled_readonly_text_color=TEXT_INPUT,
                      disabled_readonly_background_color=BORDER_COLOR, readonly=True),
         sg.SaveAs(button_text='Save Scheme', initial_folder=working_directory, k='-SAVE_AS-', button_color=("#e8bb4e", BORDER_COLOR),
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
                       keep_on_top=False)
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

    block_baner_popup = [
        [sg.T('', background_color=DARK_HEADER_COLOR, font='Any 20', size=(20, 60), justification='c')]]
    block_top_popup = [
        [sg.T('User manual', font='Any 20', size=(29, 0), justification='c')],
        [sg.VPush()],
        [sg.HorizontalSeparator(color=BORDER_COLOR, pad=((5, 20), 0))],
        [sg.VPush()],
        [sg.T("1. Select the type of product to be produced in your factory", font='Any 12', justification='l', size=(53, 0))],
        [sg.T("2. Choose the amount of this product you need", font='Any 12', justification='l', size=(53, 0))],
        [sg.T("3. Select resource consumption level", font='Any 12', justification='l', size=(34, 0))],
        [sg.VPush()],
        [sg.T("Note:\nlevel 0 - saving of this resource will not be made;\nlevel 3 - austerity of this resource, if possible, will not participate in the production chain",
              font='Any 10', justification='l', size=(53, 0))],
        [sg.VPush()],
        [sg.T("Note:\nOil Level determines the level of oil refining", font='Any 10', justification='l', size=(53, 0))],
    ]
    block_button_popup = [[sg.Button('OK', button_color=(BORDER_COLOR, 'DarkOrange1'), size=(10, 0), font='Any 15',
                                     pad=((180, 180), (5, 5)))]]

    layout_popup = [
        [sg.Column(block_baner_popup, size=(480, 30), background_color=DARK_HEADER_COLOR)],
        [sg.Column(block_top_popup, size=(480, 300))],
        [sg.Column(block_button_popup, size=(480, 50), background_color='#444444')]
    ]

    window_popup = sg.Window('Help', layout_popup, margins=(0, 0), background_color=BORDER_COLOR, keep_on_top=False,
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


