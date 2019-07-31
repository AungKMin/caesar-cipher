import string

def load_words(file_name):
    '''
    file_name (string): the name of the file containing the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    '''
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    in_file.close()
    return word_list

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of valid words. 
    word (string): word to be tested. 
    
    Returns: True if word is in word_list, False otherwise
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    '''
    The base class for CiphertextMessage and PlaintextMessage. Contains important attributes to be
    inherited. 
    '''
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        attributes: 
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to access a copy of self.valid_words outside of the class
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]
        
    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        assert isinstance(shift, int)
        strs = string.ascii_lowercase
        strb = string.ascii_uppercase
        builtDictLower = {}
        builtDictUpper = {}
        for letter in string.ascii_lowercase:
            builtDictLower[letter] = None
        for letter in string.ascii_uppercase:
            builtDictUpper[letter] = None
        for letter in builtDictLower:
            builtDictLower[letter] = strs[(strs.index(letter) + shift) % 26]
        for letter in builtDictUpper:
            builtDictUpper[letter] = strb[(strb.index(letter) + shift) % 26]
        builtDictLower.update(builtDictUpper)
        return builtDictLower

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        builtDict = self.build_shift_dict(shift)
        textList = list(self.message_text)
        for i in range(len(textList)):
            try:
                textList[i] = builtDict[textList[i]]
            except KeyError:
                pass
        return ''.join(textList)
            
        
class PlaintextMessage(Message):
    '''
    Represents a plain text message which has a shift associated with it.
    get_message_text_encrypted can be used to get the cipher text.
    '''
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        attributes: 
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)
        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encrypting_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)

    def get_shift(self):
        '''
        Used to access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encrypting_dict(self):
        '''
        Used to access a copy self.encrypting_dict outside of the class
        
        Returns: a COPY of self.encrypting_dict
        '''
        return self.encrypting_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted 

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift (ie. self.encrypting_dict and 
        message_text_encrypted).
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encrypting_dict = Message.build_shift_dict(self, self.shift)
        self.message_text_encrypted = Message.apply_shift(self, self.shift)


class CiphertextMessage(Message):
    '''
    Represents a cipher text to be decoded to plain text. decrypt_message can be called
    to decrypt the message and get the plain text. 
    '''
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. The "best" shift is defined as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        best = 0
        best_shift = 0
        for i in range(1, 27):
            dummy = self.apply_shift(i)
            count = 0
            for j in dummy.split(" "):
                if j in self.get_valid_words():
                    count += 1
            if count > best:
                best = count
                best_shift = 26 - i
        return (26 - best_shift, Message.apply_shift(self, 26 - best_shift))
                
