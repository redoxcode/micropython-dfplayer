import machine
import time

class DFPlayer:
    def __init__(self,uart_id,tx_pin_id=None,rx_pin_id=None):
        self.uart_id=uart_id
        #init with given baudrate
        self.uart = machine.UART(uart_id, 9600)  
                
        #not all boards can set the pins for the uart channel
        if tx_pin_id or rx_pin_id:
            self.uart.init(9600, bits=8, parity=None, stop=1, tx=tx_pin_id, rx=rx_pin_id)
        else:
            self.uart.init(9600, bits=8, parity=None, stop=1)
        
    def flush(self):
        self.uart.flush()
        if self.uart.any():
            self.uart.read()
        
    def send_query(self,cmd,param1=0,param2=0):
        retry=True
        while (retry):
            self.flush()
            self.send_cmd(cmd,param1,param2)
            time.sleep(0.05)
            in_bytes = self.uart.read()
            if not in_bytes: #timeout
                return -1
            if len(in_bytes)==10 and in_bytes[1]==255 and in_bytes[9]==239:
                retry=False
        return in_bytes
    
    def send_cmd(self,cmd,param1=0,param2=0):
        out_bytes = bytearray(10)
        out_bytes[0]=126
        out_bytes[1]=255
        out_bytes[2]=6
        out_bytes[3]=cmd
        out_bytes[4]=0
        out_bytes[5]=param1
        out_bytes[6]=param2
        out_bytes[9]=239
        checksum = 0
        for i in range(1,7):
            checksum=checksum+out_bytes[i]
        out_bytes[7]=(checksum>>7)-1
        out_bytes[7]=~out_bytes[7]
        out_bytes[8]=checksum-1
        out_bytes[8]=~out_bytes[8]
        self.uart.write(out_bytes)

    def stop(self):
        self.send_cmd(22,0,0)
        
    def play(self,folder,file):
        self.stop()
        time.sleep(0.05)
        self.send_cmd(15,folder,file)
        
    def volume(self,vol):
        self.send_cmd(6,0,vol)
        
    def volume_up(self):
        self.send_cmd(4,0,0)

    def volume_down(self):
        self.send_cmd(5,0,0)
    
    def reset(self):
        self.send_cmd(12,0,1)
        
    def is_playing(self):
        in_bytes = self.send_query(66)
        if in_bytes==-1 or in_bytes[5]!=2:
            return -1
        return in_bytes[6]
    
    def get_volume(self):
        in_bytes = self.send_query(67)
        if in_bytes==-1 or in_bytes[3]!=67:
            return -1
        return in_bytes[6]

    def get_files_in_folder(self,folder):
        in_bytes = self.send_query(78,0,folder)
        if in_bytes==-1:
            return -1
        if in_bytes[3]!=78:
            return 0
        return in_bytes[6]

