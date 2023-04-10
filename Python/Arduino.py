import threading
import time
import serial
import logging
import sys


class Arduino:
    state: str = None
    port: str = None
    baud: int = None
    ser: serial.Serial = None
    stateLock: threading.Lock = threading.Lock()
    logger: logging.Logger = None

    def __init__(
        self,
        port: str,
        baud=9600,
    ):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

        self.port = port
        self.baud = baud
        self.connect()
        self.monitorState()

    def connect(self):
        # Start up the serial connection
        self.ser = serial.Serial(self.port, self.baud, timeout=None)
        self.ser.flushInput()
        self.ser.flushOutput()

    def monitorState(self):
        # Start a thread to monitor the state of the Arduino
        self.t = threading.Thread(target=self.monitorArduinoOutputThread,
                                  daemon=True)
        self.t.start()

    def monitorArduinoOutputThread(self):
        # This is the thread that monitors the state of the Arduino
        while True:
            # Read the state of the Arduino
            self.readInput()
            # Sleep for a bit
            time.sleep(0.1)

    def read_handler(self, command, value):
        raise NotImplementedError("Read Handler Is Not Implemented")

    def readInput(self) -> None:
        # Read the state of the Arduino
        # Pipes the output into self.state
        # This is a blocking call
        try:
            input = self.ser.read_until(b'\n').decode('utf-8').strip()
            if ':' not in input:
                self.logger.warning("Invalid Input: {}".format(input))
                return
            command, value = input.split(':')
            self.logger.debug("Command: {} | Value: {}".format(command, value))
            self.read_handler(command, value)

        except UnicodeDecodeError:
            self.logger.warning("UnicodeDecodeError")

    def getStateSafe(self):
        # getter for state with locking
        with self.stateLock:
            return self.state

    def sendCommand(self, type: str, values: list = []) -> None:
        # If the character : is in any of the strings in values raise an exception
        values = [str(value) for value in values]
        for value in values:
            if ':' in value:
                raise (ValueError(
                    'Values cannot contain the character : when sending data to the Arduino: {}'
                    .format(value)))

        # Here we write the type of command and then the value of said command so that the arduino is able to parse it
        self.ser.write(f'{type}\n'.encode())
        time.sleep(.2)
        for value in values:
            self.ser.write(f'{value}\n'.encode())
            time.sleep(.2)

    def waitForReady(self):
        if self.state == 'ready':
            self.logger.info("State Was Ready When Wait For Ready Was Called")
        time.sleep(.3)
        while self.state != 'ready':
            time.sleep(0.1)