import serial
import PySimpleGUI as sg
import struct

sg.theme("GreenTan")
layout_th = [
    [sg.Frame(
        layout=[
            [sg.Text("Choose To show either Temperature or Humidity")],
        ],
        title="", relief=sg.RELIEF_GROOVE)
     ],
    [sg.Button("Temperature", auto_size_button=True),
     sg.Button("Humidity", auto_size_button=True),
     sg.Graph((125, 50), (0, 0), (125, 50), k='-GRAPH3-')],
    [sg.Text("", size=(30, 1), key="-OUTPUT1-")]
]

layout_led = [
    [sg.Frame(
        layout=[
            [sg.Text("Press to choose the LED")],
        ],
        title="", relief=sg.RELIEF_GROOVE,)
     ],
    [sg.Button("LED1", tooltip="There is no OFF though"),
     sg.Button("LED2", tooltip="You can ON or OFF"),
     sg.Graph((125, 50), (0, 0), (125, 50), k='-GRAPH1-')],
    [sg.Text("", size=(30, 1), key="-OUTPUT2-")]
]

layout_b = [
    [sg.Frame(
        layout=[
            [sg.Text("Press to Blink the LED")],
        ],
        title="", relief=sg.RELIEF_GROOVE, )
     ],
    [sg.Button("Blink", auto_size_button=True, tooltip="Flashes the LED"),
     sg.Graph((125, 50), (0, 0), (125, 50), k='-GRAPH2-')],
]

layout_slider = [
    [sg.Frame(
        layout=[
            [sg.Text("Move the Slider to ON the LED")],
        ],
        title="", relief=sg.RELIEF_GROOVE, )
     ],
    [sg.Slider(range=(0, 10), default_value=0, expand_x=True, enable_events=True, orientation='horizontal', key='-SL-'),
     sg.Graph((125, 50), (0, 0), (125, 50), k='-GRAPH4-')],
    [sg.Text("", size=(30, 1), key="-OUTPUT4-")]
]

layout = [
    [sg.T('The PySimpleGUI', font='_ 18', justification='c', expand_x=True, tooltip="Title")],
    [[layout_th], [layout_led], [layout_b], [layout_slider]]
]

ser = None
window = sg.Window("The PySimpleGUI", layout, finalize=True, keep_on_top=True)
window['-GRAPH1-'].draw_image(data=sg.EMOJI_BASE64_HAPPY_JOY, location=(0, 50))
window['-GRAPH2-'].draw_image(data=sg.EMOJI_BASE64_HAPPY_WINK, location=(0, 50))
window['-GRAPH3-'].draw_image(data=sg.EMOJI_BASE64_FINGERS_CROSSED, location=(0, 50))
window['-GRAPH4-'].draw_image(data=sg.EMOJI_BASE64_PONDER, location=(0, 50))


def send_brightness(brightness):
    slider_value = int((brightness / 10) * 65535)

    # Pack the brightness value into a little-endian 16-bit integer
    data_to_send = struct.pack('<H', slider_value)
    ser.write(data_to_send)


while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        ch = sg.popup_yes_no("Are you sure you want to exit?",  title="YesNo")
        if (ch == "Yes"):
            break
        else:
            if ser is None or not ser.is_open:
                ser = serial.Serial("COM8", 115200, timeout=1)
            data_to_send = "E"
            ser.write(data_to_send.encode())
            break

    elif event == "Temperature":
        try:
            if ser is None or not ser.is_open:
                ser = serial.Serial("COM8", 115200, timeout=1)
            data_to_send = "T"
            ser.write(data_to_send.encode())
            data = ser.readline().decode('utf-8').strip()
            window["-OUTPUT1-"].update(data)
        except Exception as e:
            print(e)
        continue

    elif event == "Humidity":
        try:
            if ser is None or not ser.is_open:
                ser = serial.Serial("COM8", 115200, timeout=1)
            data_to_send = "H"
            ser.write(data_to_send.encode())
            data = ser.readline().decode('utf-8').strip()
            window["-OUTPUT1-"].update(data)
        except Exception as e:
            print(e)
        continue

    elif event == "LED1":
        try:
            if ser is None or not ser.is_open:
                ser = serial.Serial("COM8", 115200, timeout=1)
            data_to_send = "4"
            ser.write(data_to_send.encode())
        except Exception as e:
            print(e)
        continue

    elif event == "LED2":
        try:
            if ser is None or not ser.is_open:
                ser = serial.Serial("COM8", 115200, timeout=1)
            data_to_send = "5"
            ser.write(data_to_send.encode())
        except Exception as e:
            print(e)
        continue

    elif event == "Blink":
        try:
            if ser is None or not ser.is_open:
                ser = serial.Serial("COM8", 115200, timeout=1)
            data_to_send = "B"
            ser.write(data_to_send.encode())
        except Exception as e:
            print(e)
        continue

    elif event == '-SL-':
        try:
            if ser is None or not ser.is_open:
                ser = serial.Serial("COM8", 115200, timeout=1)
            data_to_send = "S"
            ser.write(data_to_send.encode())
            brightness = int(values["-SL-"])
            window["-OUTPUT4-"].update(brightness)
            send_brightness(brightness)
        except Exception as e:
            print(e)
        continue

window.close()
