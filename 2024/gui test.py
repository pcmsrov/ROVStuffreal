import PySimpleGUI as sg

layout1 = [[sg.Text('Window 1')],
          [sg.Input(key='-INPUT-')],
          [sg.Text(key='-TEXT-')],
          [sg.Button('Show on Win 2')]]

layout2 = [[sg.Text('Window 2')],
          [sg.Input(key='-INPUT-')],
          [sg.Text(key='-TEXT-')],
          [sg.Button('Show on Win 1')]]

window1 = sg.Window('Window 1', layout1, relative_location=(0,-180), finalize=True)
window2 = sg.Window('Window 2', layout2, finalize=True)

while True:  # The Event Looop
    window, event, values = sg.read_all_windows()

    if event == sg.WIN_CLOSED:
        break
    if window == window1:       # if button click on window 1, show text on window 2
        window2['-TEXT-'].update(values['-INPUT-'])
    else:                       # button was on window 2, so show text on window 1
        window1['-TEXT-'].update(values['-INPUT-'])

window1.close()
window2.close()
