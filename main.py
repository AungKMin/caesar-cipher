import classes

class UserInterface(object):
    '''
    Serves as the primary user-program interface
    '''

    def __init__(self):
        '''
        Initializes a UserInterface object.

        attributes:
            self.lastInput (string, determined by user-inputted message for encoding or decoding)
        '''
        self.lastInput = None

    def start(self):
        '''
        Starts the program

        Returns: a string 'e', 'd', or 'exit' used to control the flow of the program
        '''
        while True:
            userInput = input(('Would you like to decode (type d), or encode (type e)? Or you can type exit to exit. '))
            if userInput == 'e':
                return 'encode'
            elif userInput == 'd':
                return 'decode'
            elif userInput == 'exit':
                return 'exit'
            else:
                print('Invalid input!')


    def decodeMode(self):
        '''
        Asks user for text and decodes the user-inputted cipher text

        Returns: the decoded message, along with the shift used (tuple of the form ( shift(int), plain text(string) ) )
        '''
        userInput = input('Enter the text that you want to decode: ')
        self.lastInput = userInput
        message = classes.CiphertextMessage(userInput)
        return message.decrypt_message()

    def encodeMode(self):
        '''
        Asks user for plain text and shift, and encodes the text using the shift

        Returns: the encoded message (string)
        '''
        userInputString = input('Enter the text you would like to encode: ')
        while True:
            try:
                userInputShift = int(input('Enter the shift you would like to use to encode this text: '))
                break
            except:
                print('Enter an integer please!')
        message = classes.PlaintextMessage(userInputString, userInputShift)
        return message.get_message_text_encrypted()


if __name__ == '__main__':
    print('Welcome to the super secret caesar cipher machine!')
    programInstance = UserInterface()
    while True:
        userInput = None
        userInput = programInstance.start()
        if userInput == 'encode':
            print('I encoded it: %s' % (programInstance.encodeMode()))
        elif userInput == 'decode':
            print('I decoded it by shifiting by %d: %s' % programInstance.decodeMode())
        else:
            print('Thanks for using super secret caesar cipher!')
            break