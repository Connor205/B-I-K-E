from Arduino import Arduino
import logging
import time


### Now the shuffler should in theory be very very simple. The shuffler shouldn't even be software activated probably.
# Simply put the shuffler should trigger when it senses a new deck in the input slot.
# It should then shuffle the deck and then send it to the output slot.
# The shuffler should probably have the ability to be turned off and on.
class Shuffler:
    logger: logging.Logger = None
    arduino: Arduino = None
    paused: bool = True

    def __init__(self, port: str, baud=9600):
        self.logging = logging.getLogger(__name__)
        self.arduino = Arduino(port, baud)
        self.arduino.monitorState()

    # We want to be able to pause and play the shuffling process
    def pauseShuffling(self, blocking=True):
        # Now we have this issue that if the arduino is actually in the middle of shuffling a deck, it should probably finish shuffling that given deck
        # Before it pauses, so how to we reflect this and do we want to enforce this?
        self.arduino.sendCommand('PAUSE')
        self.logger.info("Pausing shuffling")
        # If we do decide that we want to be able to block we can wait until the state is IDLE
        if blocking:
            self.logger.info("Waiting for shuffler to finish shuffling")
            self.arduino.waitForReady()

    def resumeShuffling(self):
        # Resuming shuffling is not particularly complicated tbh, we just send the resume command over.
        self.arduino.sendCommand('RESUME')
        self.logger.info("Resuming shuffling")

    # Lets go ahead and add a toggle function now
    def toggleShuffling(self):
        curState = self.arduino.getStateSafe()
        if curState == 'PAUSED':
            self.resumeShuffling()
        if curState in ['READY', 'SHUFFLING']:
            self.pauseShuffling()
