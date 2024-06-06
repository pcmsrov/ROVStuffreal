import PySimpleGUI as sg
import sys, socket, time, select, threading

layout = [[sg.Text(text="Unable to obtain depth", key="-DEPTH-"),
           sg.Text(text="Unable to obtain pressure", key="-PRESSURE-")],
          [sg.Text(text="Unable to obtain time", key="-TIME-")],
          [sg.Button("Push"), sg.Button("Pull"), sg.Button("Dive")],
          [sg.StatusBar(text="Disconnected", key="-STAT-", text_color="#F55D30")],
          [sg.StatusBar(text="Currently no message", key="-MSG-", text_color="#d3d3d3")],
          [sg.StatusBar(text="Not connected to WiFi", key="-WIFI-", text_color="#F55D30")],
          [sg.StatusBar(text="The float is not conducting any actions", key="-ACT-", text_color="#d3d3d3")],
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

    if event == "Push":
        try:
            bt_socket.send(bytes("push", 'UTF-8'))
            window["-ACT-"].update("Float is pushing", text_color="#00ff00")
        except:
            window["-MSG-"].update("Unable to send command", text_color="#b3b300")
    if event == "Pull":
        try:
            bt_socket.send(bytes("pull", 'UTF-8'))
            window["-ACT-"].update("Float is pulling", text_color="#00ff00")
        except:
            window["-MSG-"].update("Unable to send command", text_color="#b3b300")
    if event == "Dive":
        try:
            bt_socket.send(bytes("dive", 'UTF-8'))
            window["-ACT-"].update("Float is diving", text_color="#00ff00")
        except:
            window["-MSG-"].update("Unable to send command", text_color="#b3b300")
    if event == "Connect":
        try:
            command = "wifi^{}^{}".format(values["-SSID-"][0], values["-PWD-"][0])
            bt_socket.send(bytes(command, 'UTF-8'))
            window["-WIFI-"].update("Connected to Wifi", text_color="#00ff00")
        except:
            window["-WIFI-"].update("Unable to connect to Wifi", text_color="#F55D30")

    while is_resetting:
        try:
            bt_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            bt_socket.connect((BT_addr, 1))
            bt_socket.setblocking(0)
            window["-STAT-"].update("Connected", text_color="#00ff00")
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
                # split response into shit do later
                repo = response.split("\n")
                window["-TIME-"].update(repo[0])
                window["-DEPTH-"].update(repo[1])
                psi = float(repo[1]) * 1000 * 9.81
                window["-PRESSURE-"].update(psi)

    except:
        window["-TIME-"].update("Unable to receive time", text_color="F55D30")
        window["-STAT-"].update("Disconnected", text_color="#F55D30")
        is_resetting = True
        bt_socket.close()


window.close()
