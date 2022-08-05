import tkinter as tk
from tkinter import *
import serial
import time

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
master = tk.Tk()
master.title("map")
master.geometry("900x900")

# All measurements in mm
buttonScaler = 1
buttonHeight = str(buttonScaler * 5)
buttonWidth = str(buttonScaler * 10)
robotSizeReal = 370
playArea = 1000
canvasSize = 600
pixelToMM = playArea / canvasSize
robotIconSide = 370 / pixelToMM
robotStartPositionX = 310
robotStartPositionY = 310
lineWidth = 20
lineHeight = 20
initialRobotSpeed = 25


class Robot:
    def __init__(self, side, start_x, start_y, canvasObject, robotSpeed):
        self.side = side
        self.X = start_x
        self.Y = start_y
        self.canvasObject = canvasObject
        self.robotSpeed = robotSpeed


def writeArduino(arduinoData):
    data = arduino.readline()
    print(data)
    while (data != b'0'):
        time.sleep(0.05)
        data = arduino.readline()
    arduino.write(bytes(arduinoData, 'utf-8'))


def motion(event):
    mouseClickX, mouseClickY = event.x, event.y
    print('{}, {}'.format(mouseClickX, mouseClickY))
    movementCordX = mouseClickX - robot.X
    movementCordY = mouseClickY - robot.Y
    if (movementCordX < 0):
        left(round(abs(movementCordX) * pixelToMM / 10))
    elif (movementCordX > 0):
        right(round(abs(movementCordX) * pixelToMM / 10))
    if (movementCordY < 0):
        up(round(abs(movementCordY) * pixelToMM / 10))
    elif (movementCordY > 0):
        down(round(abs(movementCordY) * pixelToMM / 10))

    robot.X = mouseClickX
    robot.Y = mouseClickY




def left(distance=10):
    # print("left 10")
    directionData = "90," + str(robot.robotSpeed) + "," + str(distance) + ",$"
    print(directionData)
    if(distance == 10):
        robot.X = robot.X - (100/pixelToMM)
    writeArduino(directionData)
    robotIconUpdate()
    print(robot.X)



def right(distance=10):
    # print("right 10")
    robot.X = robot.X + (100/pixelToMM)
    directionData = "270," + str(robot.robotSpeed) + "," + str(distance) + ",$"
    print(directionData)
    robotIconUpdate()
    writeArduino(directionData)


def up(distance=10):
    # print("up 10")
    robot.Y = robot.Y - (100/pixelToMM)
    directionData = "0," + str(robot.robotSpeed) + "," + str(distance) + ",$"
    print(directionData)
    robotIconUpdate()
    writeArduino(directionData)


def down(distance=10):
    # print("down 10")
    robot.Y = robot.Y + (100/pixelToMM)
    directionData = "180," + str(robot.robotSpeed) + "," + str(distance) + ",$"
    print(directionData)
    robotIconUpdate()
    writeArduino(directionData)


def speedCounter(upOrDown=2):
    if (upOrDown == 1):
        if (robot.robotSpeed < 100):
            robot.robotSpeed = robot.robotSpeed + 5
    elif (upOrDown == 0):
        if (robot.robotSpeed > 0):
            robot.robotSpeed = robot.robotSpeed - 5
    speedTextValue = "Current Speed is: " + str(robot.robotSpeed)
    speedText.delete("1.0", "end")
    speedText.insert(END, speedTextValue)
    print(speedTextValue)

def robotIconUpdate():
    myCanvas.coords(robot.canvasObject, (robot.X - robotIconSide / 2), (robot.Y + robotIconSide / 2),
                    (robot.X + robotIconSide / 2), (robot.Y - robotIconSide / 2))
    robotPosTextValue = "X = " + str((robotStartPositionX - robot.X) * pixelToMM / 10) + "cm Y = " + str((robotStartPositionY - robot.Y) * pixelToMM / 10) + "cm"
    robotPosText.delete("1.0", "end")
    robotPosText.insert(INSERT, robotPosTextValue)


myCanvas = tk.Canvas(
    master,
    bg="black",
    height=600,
    width=600,
)

robotRect = myCanvas.create_rectangle(
    (robotStartPositionX - robotIconSide / 2), (robotStartPositionY + robotIconSide / 2),
    (robotStartPositionX + robotIconSide / 2), (robotStartPositionY - robotIconSide / 2),
    fill='red',
    outline='blue'
)

robot = Robot(robotIconSide, robotStartPositionX, robotStartPositionY, robotRect, initialRobotSpeed)

leftButton = tk.Button(
    master,
    text="<-",
    bg="blue",
    fg="white",
    width=buttonWidth,
    height=buttonHeight,
    relief="raised",
    activebackground="white",
    command=left
)

rightButton = tk.Button(
    master,
    text="->",
    bg="blue",
    fg="white",
    width=buttonWidth,
    height=buttonHeight,
    pady="3",
    relief="raised",
    padx="3",
    activebackground="white",
    command=right
)

upButton = tk.Button(
    master,
    text="^\n|",
    bg="blue",
    fg="white",
    width=buttonWidth,
    height=buttonHeight,
    pady="3",
    relief="raised",
    padx="3",
    activebackground="white",
    command=up
)

downButton = tk.Button(
    master,
    text="|\nv",
    bg="blue",
    fg="white",
    width=buttonWidth,
    height=buttonHeight,
    pady="3",
    relief="raised",
    padx="3",
    activebackground="white",
    command=down
)

speedUpButton = tk.Button(
    master,
    text="^\n|",
    bg="black",
    fg="white",
    width=buttonWidth,
    height=buttonHeight,
    pady="3",
    relief="raised",
    padx="3",
    activebackground="white",
    command=(lambda: speedCounter(1))
)

speedDownButton = tk.Button(
    master,
    text="|\nv",
    bg="black",
    fg="white",
    width=buttonWidth,
    height=buttonHeight,
    pady="3",
    relief="raised",
    padx="3",
    activebackground="white",
    command=(lambda: speedCounter(0))
)

speedText = tk.Text(
    master,
    height=1,
    font=("Helvetica", "16"),
    bg="white",
    width=17,
)

robotPosText = tk.Text(
    master,
    height=1,
    font=("Helvetica", "16"),
    bg="white",
    width=20,
)

leftButton.place(x=600, y=800)
rightButton.place(x=800, y=800)
upButton.place(x=700, y=700)
downButton.place(x=700, y=800)
speedUpButton.place(x=800, y=100)
speedDownButton.place(x=800, y=200)
speedText.place(x=650, y=10)
robotPosText.place (x=200, y= 620)

speedTextValue = "Current Speed is: " + str(robot.robotSpeed)
robotPosTextValue = "X = " + str((robotStartPositionX - robot.X) * pixelToMM / 10) + "cm Y = " + str((robotStartPositionY - robot.Y) * pixelToMM / 10) + "cm"

speedText.insert(INSERT, speedTextValue)
robotPosText.insert(INSERT, robotPosTextValue)

myCanvas.place(x=10, y=10)

myCanvas.bind('<Button 1>', motion)
master.mainloop()