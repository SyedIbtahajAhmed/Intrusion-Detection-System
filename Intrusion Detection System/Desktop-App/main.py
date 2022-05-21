# IMPORTING LIBRARIES
from re import L
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PySide2 import *
from videostream1 import *
from videostream2 import *
from videostream3 import *
from videostream4 import *


# IMPORTING GUI FILE
from interface import *


with open('theme.txt') as f:
    lines = f.readlines()
f.close()
globalthemecolor=lines[0]

# Main Window Class
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ##############################
        ##############################
        ######### Variables ##########
        ##############################
        ##############################
        gridWidth = 100
        gridHeight = 100
        gridFrames = 4
        gridFrameHeight = 100
        gridFrameWidth = 100
        self.gridSelected = 2
        self.label_Selected = [False, False, False, False]
        self.themecolor=globalthemecolor
        ##############################
        ##############################

        ##############################
        # Reading The Selected Grid File
        ##############################
        file = open("gridSelected.txt", "r+")
        file.seek(0)
        myFile = file.read()
        file.close()

        ##############################
        # Changing The Grid Layout From The File
        ##############################
        if (myFile=='2x2'):
            self.gridSelected=2
        elif (myFile=='3x3'):
            self.gridSelected=3
        elif (myFile=='4x4'):
            self.gridSelected=4
        else:
            self.gridSelected=2



        ##############################
        #Removing Window Title Bar
        ##############################
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        ##############################
        # Setting Main Background To Transparent
        ##############################
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        ##############################
        # Shadow Effect Style
        ##############################
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 550))

        ##############################
        # Applying Shadow To Central Widget
        ##############################
        self.ui.centralwidget.setGraphicsEffect(self.shadow)


        ##############################
        # Setting Window Icon
        # This icon and title will not appear on our app main window
        # becasue we removed the title bar
        ##############################
        self.setWindowIcon(QIcon(":/icons/icons/camera.svg"))
        # Setting Window Title
        self.setWindowTitle("Modern UI")


        ##############################
        # Window Size grip to resize window
        ##############################
        #QSizeGrip(self.ui.size_grip)

        ##############################
        # Maximizing The Window
        ##############################
        self.MaximizeWindow()


        ##############################
        # Setting The Constraints
        ##############################
        self.SetConstraintsSpecs()


        ##############################
        # Minimizing The Window
        ##############################
        self.ui.minimize_window_button.clicked.connect(lambda: self.showMinimized())


        ##############################
        # Closing The Window
        ##############################
        self.ui.close_window_button.clicked.connect(lambda: self.close())

        ##############################
        # Restore / Maximize Window
        ##############################
        # self.ui.restore_window_button.clicked.connect(lambda: self.restore_or_maximize_window())

        ##############################
        # Function to Move Window on Mouse Drag Event on the title Bar
        ##############################
        def moveWindow(e):
            # Detect if the window is normal size
            if self.isMaximized() == False:
                ## Moving Window only when the window is normal size
                ## Only Accepting the left Mouse Button
                if e.buttons() == Qt.LeftButton:
                    # Move Window
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
            ###################################################
        #######################################################


        ##############################
        # Add CLick Event/Mouse Move Event/Drag event to the top header to move the window
        ##############################
        self.ui.body_header.mouseMoveEvent = moveWindow


        ##############################
        # Left Menu Toggle Button
        ##############################
        # self.ui.open_close_side_bar_btn.clicked.connect(lambda: self.slideLeftMenu())


        ##############################
        # Right Status Menu Toggle Button
        ##############################
        self.ui.right_side_toggle_button_1.clicked.connect(lambda: self.slideRightMenu())


        ##############################
        # Right Side Menu Toggle Button 2
        ##############################
        self.ui.right_side_toggle_button_2.clicked.connect(lambda: self.enableAllCamerasGridView())


        ##############################
        # Color Button
        ##############################
        # self.ui.colorButton.clicked.connect(lambda: self.changeColor())

        ##############################
        # For Loop To Create A Grid Of GridFrames
        ##############################
        # Rows Loop
        for i in range(0, self.gridSelected):
            # Columns Loop
            for j in range(0, self.gridSelected):
                camera_frame_iter = self.createNewGridFrames(i, j)
                # Pushing to the camera List To Access Globally All Cameras
                camera_list.append(camera_frame_iter)
                # self.animateGridFrame(camera_frame_iter)

        ##############################
        # For Loop To Create A Grid Of GridFrames
        ##############################
        # Rows Loop
        count = 0
        while count < len(camera_list):
            self.createNewSideStatusPanelCameraFrames(count)
            count += 1

        ##############################
        # Getting Click on the GridFrame
        ##############################
        self.ui.frame_00.mousePressEvent = self.GridFrame_00_Clicked
        self.ui.frame_01.mousePressEvent = self.GridFrame_01_Clicked
        self.ui.frame_10.mousePressEvent = self.GridFrame_10_Clicked
        self.ui.frame_11.mousePressEvent = self.GridFrame_11_Clicked

        self.ui.side_frame_0.mousePressEvent = self.GridFrame_00_Clicked
        self.ui.side_frame_1.mousePressEvent = self.GridFrame_01_Clicked
        self.ui.side_frame_2.mousePressEvent = self.GridFrame_10_Clicked
        self.ui.side_frame_3.mousePressEvent = self.GridFrame_11_Clicked

        ##############################
        # Theme Changing Buttons
        ##############################
        self.ui.aqua_theme_button.clicked.connect(lambda: self.ChangeTheme('aqua'))
        self.ui.red_theme_button.clicked.connect(lambda: self.ChangeTheme('red'))
        self.ui.yellow_theme_button.clicked.connect(lambda: self.ChangeTheme('yellow'))
        self.ui.green_theme_button.clicked.connect(lambda: self.ChangeTheme('green'))
        self.ui.brown_theme_button.clicked.connect(lambda: self.ChangeTheme('bronze'))
        self.ui.white_theme_button.clicked.connect(lambda: self.ChangeTheme('white'))
        #################################################################################
        #################################################################################

        ##############################
        # Theme Changing Buttons
        ##############################
        self.ui.grid_22_Button.clicked.connect(lambda: self.ChangeSelectedGrid('2x2'))
        self.ui.grid_33_Button.clicked.connect(lambda: self.ChangeSelectedGrid('3x3'))
        self.ui.grid_44_Button.clicked.connect(lambda: self.ChangeSelectedGrid('4x4'))
        #################################################################################
        #################################################################################



        ##############################
        # Hiding and showing the side panelcameras
        ##############################
        self.enableDisableSidePanelCameras(self.label_Selected)

        self.show()
        #threads that read video stream from available devices
        self.WorkingThread1 = WorkingThread1()
        self.WorkingThread1.start()
        self.WorkingThread1.ImageUpdate.connect(self.ImageUpdateSlot1)

        # self.WorkingThread2 = WorkingThread2()
        # self.WorkingThread2.start()
        # self.WorkingThread2.ImageUpdate.connect(self.ImageUpdateSlot2)

        # self.WorkingThread3 = WorkingThread3()
        # self.WorkingThread3.start()
        # self.WorkingThread3.ImageUpdate.connect(self.ImageUpdateSlot3)

        # self.WorkingThread4 = WorkingThread4()
        # self.WorkingThread4.start()
        # self.WorkingThread4.ImageUpdate.connect(self.ImageUpdateSlot4)

# <============================================================================ Functions ======================================================> #

    ##############################
    # Getting The User Input and Changing the color (THEME CHANGING)
    ##############################
    def ChangeTheme(self, theme):
        if (theme == 'aqua'):
            Color1 = '#00FFFF'
            import fileinput
            file = open("theme.txt", "r+")
            file.seek(0)
            file.write(Color1)
            file.close()
            QtCore.QCoreApplication.quit()
            status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        elif (theme == 'red'):
            Color1 = '#FF0000'
            import fileinput
            file = open("theme.txt", "r+")
            file.seek(0)
            file.write(Color1)
            file.close()
            QtCore.QCoreApplication.quit()
            status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        elif (theme == 'yellow'):
            Color1 = '#FFC300'
            import fileinput
            file = open("theme.txt", "r+")
            file.seek(0)
            file.write(Color1)
            file.close()
            QtCore.QCoreApplication.quit()
            status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        elif (theme == 'green'):
            Color1 = '#097969'
            import fileinput
            file = open("theme.txt", "r+")
            file.seek(0)
            file.write(Color1)
            file.close()
            QtCore.QCoreApplication.quit()
            status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        elif (theme == 'bronze'):
            Color1 = '#CD7F32'
            import fileinput
            file = open("theme.txt", "r+")
            file.seek(0)
            file.write(Color1)
            file.close()
            QtCore.QCoreApplication.quit()
            status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        elif (theme == 'white'):
            Color1 = '#FFFFFF'
            import fileinput
            file = open("theme.txt", "r+")
            file.seek(0)
            file.write(Color1)
            file.close()
            QtCore.QCoreApplication.quit()
            status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        else:
            Color1 = '#00FFFF'
            import fileinput
            file = open("theme.txt", "r+")
            file.seek(0)
            file.write(Color1)
            file.close()
            QtCore.QCoreApplication.quit()
            status = QtCore.QProcess.startDetached(sys.executable, sys.argv)

    
    ##############################
    # Getting The User Input To Change The Grid Size
    ##############################
    def ChangeSelectedGrid(self, size):
        if (size=='2x2'):
            self.gridSelected=2
            import fileinput
            file = open("gridSelected.txt", "r+")
            file.seek(0)
            file.write(str(self.gridSelected) + 'x' + str(self.gridSelected))
            file.close()
            QtCore.QCoreApplication.quit()
            status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        elif (size=='3x3'):
            self.gridSelected=3
            import fileinput
            file = open("gridSelected.txt", "r+")
            file.seek(0)
            file.write(str(self.gridSelected) + 'x' + str(self.gridSelected))
            file.close()
            QtCore.QCoreApplication.quit()
            status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        elif (size=='4x4'):
            self.gridSelected=4
            import fileinput
            file = open("gridSelected.txt", "r+")
            file.seek(0)
            file.write(str(self.gridSelected) + 'x' + str(self.gridSelected))
            file.close()
            QtCore.QCoreApplication.quit()
            status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        else:
            self.gridSelected=2
            import fileinput
            file = open("gridSelected.txt", "r+")
            file.seek(0)
            file.write(str(self.gridSelected) + 'x' + str(self.gridSelected))
            file.close()
            QtCore.QCoreApplication.quit()
            status = QtCore.QProcess.startDetached(sys.executable, sys.argv)


    ##############################
    # Centering The Window
    ##############################
    def CenterTheWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



    ##############################
    # Setting The Grid Height and Width
    ##############################
    def SetConstraintsSpecs(self):
        self.gridWidth = self.ui.main_body_content_area.width()
        self.gridHeight = self.ui.main_body_content_area.height()
        # print('Width : ' + str(self.gridWidth))
        # print('Height : ' + str(self.gridHeight))


        # temp vars
        newGridWidth = self.gridWidth - 60      # Padding 30 on each side
        newGridHeight = self.gridHeight - 60      # Padding 30 on each side

        tempWidth = int(newGridWidth / 3)
        tempHeight = tempWidth
        while (True):
            if (round(tempWidth/tempHeight, 2) == 1.77):    # 16:9
                break
            tempHeight -= 1
        self.gridFrameWidth = tempWidth
        self.gridFrameHeight = tempHeight

    ##############################
    # Grid Frames Click Event
    ##############################
    def GridFrame_00_Clicked(self, event):
        # print("Frame_00 Clicked")
        self.ui.main_body_content_area.setMinimumSize(QtCore.QSize(self.gridWidth - 100, self.gridHeight - 100))
        self.ui.main_body_content_area.setMaximumSize(QtCore.QSize(self.gridWidth, self.gridHeight))
        self.ui.frame_00.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_00.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_00.show()
        self.ui.frame_01.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_01.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_01.show()
        self.ui.frame_10.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_10.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_10.show()
        self.ui.frame_11.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_11.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_11.show()
        if event.buttons() == QtCore.Qt.LeftButton:
            event.accept()
            gridLayout_width = self.ui.main_body_content_area.width()
            selected_camera_width = gridLayout_width - 20   # For Padding 10
            selected_camera_height = gridLayout_width - 50
            while (True):

                if (round(selected_camera_width/selected_camera_height, 2) == 1.77):
                    break
                selected_camera_height -= 1
            # print(selected_camera_width)
            # print(selected_camera_height)
            self.ui.frame_00.setMinimumSize(QtCore.QSize(selected_camera_width, selected_camera_height))
            self.ui.frame_00.setMaximumSize(QtCore.QSize(selected_camera_width, selected_camera_height))
            ## Making the Selected True
            self.label_Selected[0] = True
            self.enableDisableSidePanelCameras(self.label_Selected)

            self.ui.frame_00.show()
            self.ui.frame_01.hide()
            self.ui.frame_10.hide()
            self.ui.frame_11.hide()
    

    def GridFrame_01_Clicked(self, event):
        # print("Frame_01 Clicked")
        self.ui.main_body_content_area.setMinimumSize(QtCore.QSize(self.gridWidth - 100, self.gridHeight - 100))
        self.ui.main_body_content_area.setMaximumSize(QtCore.QSize(self.gridWidth, self.gridHeight))
        self.ui.frame_00.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_00.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_00.show()
        self.ui.frame_01.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_01.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_01.show()
        self.ui.frame_10.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_10.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_10.show()
        self.ui.frame_11.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_11.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_11.show()
        if event.buttons() == QtCore.Qt.LeftButton:
            event.accept()
            gridLayout_width = self.ui.main_body_content_area.width()
            selected_camera_width = gridLayout_width - 20   # For Padding 100
            selected_camera_height = gridLayout_width - 50
            while (True):

                if (round(selected_camera_width/selected_camera_height, 2) == 1.77):
                    break
                selected_camera_height -= 1
            # print(selected_camera_width)
            # print(selected_camera_height)
            self.ui.frame_01.setMinimumSize(QtCore.QSize(selected_camera_width, selected_camera_height))
            self.ui.frame_01.setMaximumSize(QtCore.QSize(selected_camera_width, selected_camera_height))
            ## Making the Selected True
            self.label_Selected[1] = True
            self.enableDisableSidePanelCameras(self.label_Selected)


            self.ui.frame_00.hide()
            self.ui.frame_01.show()
            self.ui.frame_10.hide()
            self.ui.frame_11.hide()
            


    def GridFrame_10_Clicked(self, event):
        # print("Frame_10 Clicked")
        self.ui.main_body_content_area.setMinimumSize(QtCore.QSize(self.gridWidth - 100, self.gridHeight - 100))
        self.ui.main_body_content_area.setMaximumSize(QtCore.QSize(self.gridWidth, self.gridHeight))
        self.ui.frame_00.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_00.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_00.show()
        self.ui.frame_01.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_01.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_01.show()
        self.ui.frame_10.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_10.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_10.show()
        self.ui.frame_11.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_11.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_11.show()
        if event.buttons() == QtCore.Qt.LeftButton:
            event.accept()
            gridLayout_width = self.ui.main_body_content_area.width()
            selected_camera_width = gridLayout_width - 20   # For Padding 100
            selected_camera_height = gridLayout_width - 50
            while (True):

                if (round(selected_camera_width/selected_camera_height, 2) == 1.77):
                    break
                selected_camera_height -= 1
            # print(selected_camera_width)
            # print(selected_camera_height)
            self.ui.frame_10.setMinimumSize(QtCore.QSize(selected_camera_width, selected_camera_height))
            self.ui.frame_10.setMaximumSize(QtCore.QSize(selected_camera_width, selected_camera_height))
            ## Making the Selected True
            self.label_Selected[2] = True
            self.enableDisableSidePanelCameras(self.label_Selected)

            self.ui.frame_00.hide()
            self.ui.frame_01.hide()
            self.ui.frame_10.show()
            self.ui.frame_11.hide()


    def GridFrame_11_Clicked(self, event):
        # print("Frame_11 Clicked")
        self.ui.main_body_content_area.setMinimumSize(QtCore.QSize(self.gridWidth - 100, self.gridHeight - 100))
        self.ui.main_body_content_area.setMaximumSize(QtCore.QSize(self.gridWidth, self.gridHeight))
        self.ui.frame_00.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_00.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_00.show()
        self.ui.frame_01.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_01.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_01.show()
        self.ui.frame_10.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_10.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_10.show()
        self.ui.frame_11.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_11.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_11.show()
        if event.buttons() == QtCore.Qt.LeftButton:
            event.accept()
            gridLayout_width = self.ui.main_body_content_area.width()
            selected_camera_width = gridLayout_width - 20   # For Padding 100
            selected_camera_height = gridLayout_width - 50
            while (True):

                if (round(selected_camera_width/selected_camera_height, 2) == 1.77):
                    break
                selected_camera_height -= 1
            # print(selected_camera_width)
            # print(selected_camera_height)
            self.ui.frame_11.setMinimumSize(QtCore.QSize(selected_camera_width, selected_camera_height))
            self.ui.frame_11.setMaximumSize(QtCore.QSize(selected_camera_width, selected_camera_height))
            self.label_Selected[3] = True
            self.enableDisableSidePanelCameras(self.label_Selected)

            self.ui.frame_00.hide()
            self.ui.frame_01.hide()
            self.ui.frame_10.hide()
            self.ui.frame_11.show()
    ##############################
    ##############################
    ##############################
    ##############################


    ##############################
    # Creating Grid Camera Frames
    ##############################
    def createNewGridFrames(self, rowNumber, colNumber):
        # Creating New Names For Frames Of The Grid
        newName = "frame_" + str(rowNumber) + str(colNumber)
        newLabelName = "label_" + str(rowNumber) + str(colNumber)
        newVerticalLayout_cameraFrameName = "verticalLayout_cameraFrame_" + str(rowNumber) + str(colNumber)

        #####################################################################################################
        # Grid Frame
        # self.camera_frame = QtWidgets.QFrame(self.ui.main_body_content_area)
        # # self.grid_frame = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents)
        # # Using setObjectName() to set the names of the new frames
        # self.camera_frame.setObjectName(newName)
        # self.camera_frame.setMinimumSize(QtCore.QSize(640, 480))
        # self.camera_frame.setMaximumSize(QtCore.QSize(640, 480))
        # self.camera_frame.setStyleSheet("background-color: #000000;\n" "border: 2px solid #008080;\n" "border-radius: 10px;")
        # self.camera_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.camera_frame.setFrameShadow(QtWidgets.QFrame.Raised)


        self.camera_frame = QtWidgets.QFrame(self.ui.main_body_content_area)
        self.camera_frame.setMinimumSize(QtCore.QSize(self.gridFrameWidth , self.gridFrameHeight ))
        self.camera_frame.setMaximumSize(QtCore.QSize(self.gridFrameWidth , self.gridFrameHeight ))
        self.camera_frame.setStyleSheet("background-color: "+self.themecolor+"; border-radius: 10px;")
        self.camera_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.camera_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camera_frame.setObjectName(newName)
        # Creating new attribute to UI_MainWindow
        # Syntax : setattr(obj, var, val)
        # obj : Object whose which attribute is to be assigned
        # var : Object attribute which has to be assigned
        # val : value with which variable is to be assigned
        setattr(self.ui, newName, self.camera_frame)


        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.camera_frame)
        self.verticalLayout_16.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(newVerticalLayout_cameraFrameName)
        # Creating new attribute to UI_MainWindow
        # Syntax : setattr(obj, var, val)
        # obj : Object whose which attribute is to be assigned
        # var : Object attribute which has to be assigned
        # val : value with which variable is to be assigned
        setattr(self.ui, newVerticalLayout_cameraFrameName, self.verticalLayout_16)


        globals()[newLabelName] = QtWidgets.QLabel(self.camera_frame)
        globals()[newLabelName].setAutoFillBackground(False)
        globals()[newLabelName].setText("")
        globals()[newLabelName].setTextFormat(QtCore.Qt.AutoText)
        globals()[newLabelName].setPixmap(QtGui.QPixmap("../../Pictures/jetson nano.png"))
        globals()[newLabelName].setAlignment(QtCore.Qt.AlignCenter)
        globals()[newLabelName].setScaledContents(True)

        globals()[newLabelName].setObjectName(newLabelName)
        self.verticalLayout_16.addWidget(globals()[newLabelName])
        # Creating new attribute to UI_MainWindow
        # Syntax : setattr(obj, var, val)
        # obj : Object whose which attribute is to be assigned
        # var : Object attribute which has to be assigned
        # val : value with which variable is to be assigned
        setattr(self.ui, newLabelName, globals()[newLabelName])
        
        self.ui.gridLayout.addWidget(self.camera_frame, rowNumber, colNumber, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHCenter)
        return newName
        #####################################################################################################
        #####################################################################################################


    ##############################
    # Creating Side Status Panel Camera Frames
    ##############################
    def createNewSideStatusPanelCameraFrames(self, index):
        # Creating New Names For Frames Of The Grid
        newNameSidePanel = "side_frame_" + str(index)
        newLabelNameSidePanel = "side_label_" + str(index)
        newVerticalLayout_cameraFrameNameSidePanel = "side_verticalLayout_cameraFrame_" + str(index)

        self.side_camera_frame = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents)
        self.side_camera_frame.setMinimumSize(QtCore.QSize(0, 140))
        self.side_camera_frame.setMaximumSize(QtCore.QSize(260, 150))
        self.side_camera_frame.setStyleSheet("background-color:"+self.themecolor+"; border-radius: 10px;")
        self.side_camera_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.side_camera_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.side_camera_frame.setObjectName(newNameSidePanel)
        # Creating new attribute to UI_MainWindow
        # Syntax : setattr(obj, var, val)
        # obj : Object whose which attribute is to be assigned
        # var : Object attribute which has to be assigned
        # val : value with which variable is to be assigned
        setattr(self.ui, newNameSidePanel, self.side_camera_frame)


        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.side_camera_frame)
        self.verticalLayout_14.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_14.setSpacing(5)
        self.verticalLayout_14.setObjectName(newVerticalLayout_cameraFrameNameSidePanel)
        # Creating new attribute to UI_MainWindow
        # Syntax : setattr(obj, var, val)
        # obj : Object whose which attribute is to be assigned
        # var : Object attribute which has to be assigned
        # val : value with which variable is to be assigned
        setattr(self.ui, newVerticalLayout_cameraFrameNameSidePanel, self.verticalLayout_14)


        globals()[newLabelNameSidePanel] = QtWidgets.QLabel(self.side_camera_frame)
        globals()[newLabelNameSidePanel].setStyleSheet("border-radius: 10px;")
        globals()[newLabelNameSidePanel].setText("")
        globals()[newLabelNameSidePanel].setPixmap(QtGui.QPixmap("../../Pictures/laptop.jpg"))
        globals()[newLabelNameSidePanel].setObjectName(newLabelNameSidePanel)
        self.verticalLayout_14.addWidget(globals()[newLabelNameSidePanel])
        globals()[newLabelNameSidePanel].setScaledContents(True)
        # Creating new attribute to UI_MainWindow
        # Syntax : setattr(obj, var, val)
        # obj : Object whose which attribute is to be assigned
        # var : Object attribute which has to be assigned
        # val : value with which variable is to be assigned
        setattr(self.ui, newLabelNameSidePanel, globals()[newLabelNameSidePanel])
        self.ui.verticalLayout_13.addWidget(self.side_camera_frame, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)



    #####################################################################################################
    #####################################################################################################


    ##############################
    # Animating The Grid Frame
    ##############################    
    def animateGridFrame(self, camera_frame):
        # Animating The Transition
        self.animation = QPropertyAnimation(camera_frame, b"minimumSize")
        # Animating Minimum Size
        self.animation.setDuration(2000)
        self.animation.setStartValue(QtCore.QSize(0, 0))    # Start Value is the current width
        self.animation.setEndValue(QtCore.QSize(640, 480))      # End value is the new width
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.start()


    ##############################
    # Slide Left Menu Function
    ##############################
    # def slideLeftMenu(self):
    #     # Get cueent left menu width
    #     width = self.ui.slide_menu_container.width()

    #     # IF Minimized
    #     if width == 0:
    #         # Expand Menu
    #         newWidth = 250
    #         self.ui.open_close_side_bar_btn.setIcon(QIcon(u":/icons/icons/chevrons-left.svg"))
    #         self.SetConstraintsSpecs()

    #     # If Maximized
    #     else:
    #         # Restore Menu
    #         newWidth = 0
    #         self.ui.open_close_side_bar_btn.setIcon(QIcon(u":/icons/icons/menu.svg"))
    #         self.SetConstraintsSpecs()
        
    #     # Animating The Transition
    #     self.animation = QPropertyAnimation(self.ui.slide_menu_container, b"minimumWidth")
    #     # Animating Minimum Width
    #     self.animation.setDuration(250)
    #     self.animation.setStartValue(width)     # Start Value is the current width
    #     self.animation.setEndValue(newWidth)    # End value is the new width
    #     self.animation.setEasingCurve(QEasingCurve.InOutQuart)
    #     self.animation.start()
    ##############################


    ##############################
    # Slide Right Menu Function
    ##############################
    def slideRightMenu(self):
        # Get cueent left menu width
        width = self.ui.status_side_menu.width()

        # IF Minimized
        if width == 0:
            # Expand Menu
            newWidth = 350
            self.ui.right_side_toggle_button_1.setIcon(QIcon(u":/icons/icons/toggle-right.svg"))

        # If Maximized
        else:
            # Restore Menu
            newWidth = 0
            self.ui.right_side_toggle_button_1.setIcon(QIcon(u":/icons/icons/toggle-left.svg"))
        
        # Animating The Transition
        self.animation = QPropertyAnimation(self.ui.status_side_menu, b"minimumWidth")
        # Animating Minimum Width
        self.animation.setDuration(300)
        self.animation.setStartValue(width)     # Start Value is the current width
        self.animation.setEndValue(newWidth)    # End value is the new width
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()
        # enableAllCamerasGridView(self)
    ##############################



    ##############################
    # Slide Right Menu Function
    ##############################
    def enableAllCamerasGridView(self):
        # Get cueent left menu width
        width = self.ui.status_side_menu.width()

        # # IF Minimized
        # if width == 0:
        #     # Expand Menu
        #     newWidth = 350
        #     self.ui.right_side_toggle_button_1.setIcon(QIcon(u":/icons/icons/toggle-right.svg"))

        # # If Maximized
        # else:
        #     # Restore Menu
        #     newWidth = 0
        #     self.ui.right_side_toggle_button_1.setIcon(QIcon(u":/icons/icons/toggle-left.svg"))
        
        # Animating The Transition
        # self.animation = QPropertyAnimation(self.ui.status_side_menu, b"minimumWidth")
        # # Animating Minimum Width
        # self.animation.setDuration(300)
        # self.animation.setStartValue(width)     # Start Value is the current width
        # self.animation.setEndValue(newWidth)    # End value is the new width
        # self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        # self.animation.start()
        self.ui.main_body_content_area.setMinimumSize(QtCore.QSize(self.gridWidth - 100, self.gridHeight - 100))
        self.ui.main_body_content_area.setMaximumSize(QtCore.QSize(self.gridWidth, self.gridHeight))
        self.ui.frame_00.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_00.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_00.show()
        self.ui.frame_01.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_01.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_01.show()
        self.ui.frame_10.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_10.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_10.show()
        self.ui.frame_11.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.ui.frame_11.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.ui.frame_11.show()
    ##############################


    ##############################
    # Slide Right Menu Function
    ##############################
    def enableDisableSidePanelCameras(self, camerasList):
        for i in range(len(camerasList)):
            if (i == 0 and camerasList[i] == True):
                # print("0 Clicked")
                self.ui.side_frame_0.show()
                self.ui.side_frame_1.show()
                self.ui.side_frame_2.show()
                self.ui.side_frame_3.show()
            elif (i == 1 and camerasList[i] == True):
                # print("1 Clicked")
                self.ui.side_frame_0.show()
                self.ui.side_frame_1.show()
                self.ui.side_frame_2.show()
                self.ui.side_frame_3.show()
            elif (i == 2 and camerasList[i] == True):
                # print("2 Clicked")
                self.ui.side_frame_0.show()
                self.ui.side_frame_1.show()
                self.ui.side_frame_2.show()
                self.ui.side_frame_3.show()
            elif (i == 3 and camerasList[i] == True):
                # print("4 Clicked")
                self.ui.side_frame_0.show()
                self.ui.side_frame_1.show()
                self.ui.side_frame_2.show()
                self.ui.side_frame_3.show()
            else:
                # print("Nothing Clicked")
                self.ui.side_frame_0.show()
                self.ui.side_frame_1.show()
                self.ui.side_frame_2.show()
                self.ui.side_frame_3.show()
    ##############################

    
    ##############################
    # Update Restore Button icon or Maximizing or Minimizing Window
    ##############################
    # def restore_or_maximize_window(self):
    #     # If Window Is Maximized
    #     if self.isMaximized():
    #         self.showNormal()
    #         # Change Icon
    #         self.ui.restore_window_button.setIcon(QIcon(":/icons/icons/maximize.svg"))

    #     else:
    #         self.showMaximized()
    #         # Changing Icon
    #         self.ui.restore_window_button.setIcon(QIcon(":/icons/icons/minimize-2.svg"))
    ##############################


    ##############################
    # Maximizing The Window
    ##############################
    def MaximizeWindow(self):
        self.showFullScreen()
    ##############################


    ##############################
    # Add Mouse Evenrs To The Window
    ##############################
    def mousePressEvent(self, event):
        # Get the current position of the mouse
        self.clickPosition = event.globalPos()
        # We will use this value to mobe the window
    ##############################
    def ImageUpdateSlot1(self, Image):
        # globals()[newLabelName].setPixmap(QtGui.QPixmap(Image))
        label_00.setPixmap(QtGui.QPixmap(Image))
        side_label_0.setPixmap(QtGui.QPixmap(Image))
        # label_01.setPixmap(QtGui.QPixmap(Image))
        # label_10.setPixmap(QtGui.QPixmap(Image))
        # label_11.setPixmap(QtGui.QPixmap(Image))
    def ImageUpdateSlot2(self, Image):
        # globals()[newLabelName].setPixmap(QtGui.QPixmap(Image))
        label_01.setPixmap(QtGui.QPixmap(Image))
        side_label_1.setPixmap(QtGui.QPixmap(Image))

    def ImageUpdateSlot3(self, Image):
        # globals()[newLabelName].setPixmap(QtGui.QPixmap(Image))
        label_10.setPixmap(QtGui.QPixmap(Image))
        side_label_2.setPixmap(QtGui.QPixmap(Image))

    def ImageUpdateSlot4(self, Image):
        # globals()[newLabelName].setPixmap(QtGui.QPixmap(Image))
        label_11.setPixmap(QtGui.QPixmap(Image))
        side_label_3.setPixmap(QtGui.QPixmap(Image))

# Execute App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    ## Screen Size Getting
    screen = app.primaryScreen()
    size = screen.size()
    global rect
    rect = screen.availableGeometry()
    # print('Available: %d x %d' % (rect.width(), rect.height()))

    ## Camera List
    global camera_list
    camera_list = []

    window = MainWindow()


    sys.exit(app.exec_())