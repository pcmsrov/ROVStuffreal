import PySimpleGUI as sg
import sys, socket, time, select, threading

layout = [ [sg.Text(text="Unable to obtain depth", key="-DEPTH-"), sg.Text(text="Unable to obtain pressure", key="-PRESSURE-")],
           [sg.Text(text="Unable to obtain time", key="-TIME-")],
           [sg.Button("Push"), sg.Button("Pull"), sg.Button("Dive")],
           [sg.StatusBar(text="Disconnected", key="-STAT-", text_color="#c2ffa7")],
           [sg.StatusBar(text="Currently no message", key="-MSG-", text_color="#c2ffa7")],
           [sg.StatusBar(text="Not connected to WiFi", key="-WIFI-", text_color="#c2ffa7")],
           [sg.StatusBar(text="The float is not conducting any actions", key="-ACT-", text_color="#c2ffa7")],
           [sg.Input(default_text="SSID", key="-SSID-"), sg.Input(default_text="Password", key="-PWD-")],
           [sg.Button("Connect")]
           ]

window = sg.Window("Float Control", layout)


is_resetting = True
BT_addr = "9C:9C:1F:EB:00:82"
BT_port = 1
bt_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    while is_resetting:
        try:
            bt_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            bt_socket.connect((BT_addr, 1))
            bt_socket.setblocking(0)
            window["-STAT-"].update("Connected")
            is_resetting = False
        except:
            bt_socket.close()

    try:
        if is_resetting:
            pass
        ready = select.select([bt_socket], [], [], 3)
        if ready[0]:
            response = bt_socket.recv(100).decode("UTF-8").strip()
            if response != '':
                #split response into shit do later
                pass
    except:
        window["-TIME-"].update("Unable to receive time")
        window["-STAT-"].update("Disconnected")
        is_resetting = True
        bt_socket.close()

    if event == "Push":
        try:
            bt_socket.send(bytes("push", 'UTF-8'))
            window["-ACT-"].update("Float is pushing")
        except:
            window["-MSG-"].update("Unable to send command")
    if event == "Pull":
        try:
            bt_socket.send(bytes("pull", 'UTF-8'))
            window["-ACT-"].update("Float is pulling")
        except:
            window["-MSG-"].update("Unable to send command")
    if event == "Dive":
        try:
            bt_socket.send(bytes("dive", 'UTF-8'))
            window["-ACT-"].update("Float is diving")
        except:
            window["-MSG-"].update("Unable to send command")
    if event == "Connect":
        try:
            command = "wifi^{}^{}".format(values["-SSID-"][0], values["-PWD-"][0])
            bt_socket.send(bytes(command, 'UTF-8'))
            window["-WIFI-"].update("Connected to Wifi")
        except:
            window["-WIFI-"].update("Unable to connect to Wifi")

window.close()