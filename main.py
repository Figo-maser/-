import sys
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
from ui_demo_1 import Ui_Form
from PyQt5.QtGui import QFont
from binascii import *
from crcmod import *
class Pyqt5_Serial(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(Pyqt5_Serial, self).__init__()
        self.setupUi(self)
        self.init()
        self.setWindowTitle("串口小助手")
        self.ser = serial.Serial()
        self.port_check()
        self.outdata = ''
        self.ptz = ''
        self.mode = ''
        self.frame_lenth = 0
        self.zoom = 0
        self.video = 0
        self.camera = 0
    def init(self):
        # 串口检测按钮
        self.s1__box_1.clicked.connect(self.port_check)

        # 串口信息显示
        self.s1__box_2.currentTextChanged.connect(self.port_imf)

        # 打开串口按钮
        self.open_button.clicked.connect(self.port_open)

        # 关闭串口按钮
        self.close_button.clicked.connect(self.port_close)

        # 定时发送数据
        self.timer_send = QTimer()
        self.timer_send.timeout.connect(self.data_send)

        #放大
        self.zoom_add.clicked.connect(self.zoom_up)
        #缩小
        self.zoom_sub.clicked.connect(self.zoom_down)
        #停止
        self.zoom_stop.clicked.connect(self.zoom_st)
        #视频选择1
        self.select1.clicked.connect(self.select_hdmi)
        # 视频选择1
        self.select2.clicked.connect(self.select_inf)
        # 视频选择1
        self.select3.clicked.connect(self.select_hdmi_inf)
        # 视频选择1
        self.select4.clicked.connect(self.select_inf_hdmi)
        # 可见光拍照
        self.k_photo.clicked.connect(self.camera_photo)
        # 可见光录像开
        self.k_rec1.clicked.connect(self.camera_recon)
        # 可见光录像关
        self.k_rec2.clicked.connect(self.camera_recoff)
        # 红外拍照
        self.h_photo.clicked.connect(self.inf_photo)
        # 红外录像开
        self.h_rec1.clicked.connect(self.inf_recon)
        # 红外录像关
        self.h_rec2.clicked.connect(self.inf_recoff)

    def camera_photo(self):
        self.camera = 17

    def camera_recon(self):
        self.camera = 18

    def camera_recoff(self):
        self.camera = 19

    def inf_photo(self):
        self.camera = 33

    def inf_recon(self):
        self.camera = 34

    def inf_recoff(self):
        self.camera = 35

    def select_hdmi(self):
        self.video = 1

    def select_inf(self):
        self.video = 2

    def select_hdmi_inf(self):
        self.video = 3

    def select_inf_hdmi(self):
        self.video = 4
            # 放大

    def zoom_up(self):
        self.zoom = -10000
    def zoom_down(self):
        self.zoom = 10000
    def zoom_st(self):
        self.zoom = 0
    # 串口检测
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.s1__box_2.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.s1__box_2.addItem(port[0])
        if len(self.Com_Dict) == 0:
            self.state_label.setText(" 无串口")

    # 串口信息
    def port_imf(self):
        # 显示选定的串口的详细信息
        imf_s = self.s1__box_2.currentText()
        if imf_s != "":
            self.state_label.setText(self.Com_Dict[self.s1__box_2.currentText()])

    # 打开串口
    def port_open(self):
        self.ser.port = self.s1__box_2.currentText()
        self.ser.baudrate = int(self.s1__box_3.currentText())
        self.ser.bytesize = 8
        self.ser.stopbits = 1

        try:
            self.ser.open()
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None

        # 打开串口接收定时器，周期为2ms
    #    self.timer.start(20)
        self.timer_send.start(1000)
        if self.ser.isOpen():
            self.open_button.setEnabled(False)
            self.close_button.setEnabled(True)


    # 关闭串口
    def port_close(self):

        self.timer_send.stop()
        try:
            self.ser.close()
        except:
            pass
        self.open_button.setEnabled(True)
        self.close_button.setEnabled(False)

    # 发送数据
    def data_send(self):
        if self.ser.isOpen():
            pitch_value=self.silder1.value()
            if pitch_value < 0 :
                pitch_value = 65536 + pitch_value
            pitch_value_H = pitch_value //256
            pitch_value_L = pitch_value %256
            hex_pitch_H = '{:02X}'.format(pitch_value_H)
            hex_pitch_L = '{:02X}'.format(pitch_value_L)
            roll_value = self.silder2.value()
            if roll_value < 0 :
                roll_value = roll_value + 65536
            roll_value_H = roll_value // 256
            roll_value_L = roll_value % 256
            hex_roll_H = '{:02X}'.format(roll_value_H)
            hex_roll_L = '{:02X}'.format(roll_value_L)

            yaw_value = self.silder3.value()
            if yaw_value < 0:
                yaw_value = yaw_value  + 65536
            yaw_value_H = yaw_value // 256
            yaw_value_L = yaw_value % 256
            hex_yaw_H = '{:02X}'.format(yaw_value_H)
            hex_yaw_L = '{:02X}'.format(yaw_value_L)
            zoom_value = self.zoom
            if zoom_value < 0 :
                zoom_value = zoom_value + 65536
            zoom_value_H = zoom_value // 256
            zoom_value_L = zoom_value % 256
            hex_zoom_H = '{:02X}'.format(zoom_value_H)
            hex_zoom_L = '{:02X}'.format(zoom_value_L)
            self.frame_lenth = 64
            hex_frame = '{:02X}'.format(self.frame_lenth)
            output_s = 'AB0E' + hex_frame + '013200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000B54008'+hex_pitch_L +hex_pitch_H +hex_roll_L +hex_roll_H +hex_yaw_L +hex_yaw_H + hex_zoom_L +hex_zoom_H
        #    print(output_s)
            if self.video != 0 :
                self.frame_lenth = 67
                hex_frame = '{:02X}'.format(self.frame_lenth)
                hex_video = '{:02X}'.format(self.video)
                output_s = 'AB0E' + hex_frame + '013200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000B54008' + hex_pitch_L + hex_pitch_H + hex_roll_L + hex_roll_H + hex_yaw_L + hex_yaw_H + hex_zoom_L + hex_zoom_H + '7001' + hex_video
                self.video = 0

            if self.camera != 0 :
                self.frame_lenth = 67
                hex_frame = '{:02X}'.format(self.frame_lenth)
                hex_camera = '{:02X}'.format(self.camera)
                output_s = 'AB0E' + hex_frame + '013200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000B54008' + hex_pitch_L + hex_pitch_H + hex_roll_L + hex_roll_H + hex_yaw_L + hex_yaw_H + hex_zoom_L + hex_zoom_H + '7101' + hex_camera
                self.camera = 0
            input_s = output_s

            crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
            data = input_s.replace(" ", "")
            readcrcout = hex(crc16(unhexlify(data))).upper()
            str_list = list(readcrcout)
            if len(str_list) == 5:
                str_list.insert(2, '0')  # 位数不足补0
            crc_data = "".join(str_list)
            input_s= input_s.strip() + crc_data[4:] + crc_data[2:4]
            if input_s != "":
                send_list = []
                while input_s != '':
                    try:
                        num = int(input_s[0:2], 16)
                    except ValueError:
                        QMessageBox.critical(self, 'wrong data', '请输入十六进制数据，以空格分开!')
                        return None
                    input_s = input_s[2:].strip()
                    send_list.append(num)
                input_s = bytes(send_list)
                self.ser.write(input_s)

        else:
            pass



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = Pyqt5_Serial()
    myshow.show()
    sys.exit(app.exec_())
