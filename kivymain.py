import kivy
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.behaviors import FocusBehavior
import classes

"""
To do: 

- Customize app using .kv file 
- Figure out a way to get the cursor to start at main_app.textEncode
"""

class FocusTextInput(TextInput, FocusBehavior):
    """
    Text Input objects you can tab between 
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.write_tab = False

    # Override _key_down in TextInput to get rid of the on_text_validate event call whenever enter is pressed
    # This event set focus to False, meaning we couldn't check where the focus was when the user presses Enter.
    def _key_down(self, key, repeat=False):
        displayed_str, internal_str, internal_action, scale = key

        # handle deletion
        if (self._selection and
                internal_action in (None, 'del', 'backspace', 'enter')):
            if internal_action != 'enter' or self.multiline:
                self.delete_selection()
        elif internal_action == 'del':
            # Move cursor one char to the right. If that was successful,
            # do a backspace (effectively deleting char right of cursor)
            cursor = self.cursor
            self.do_cursor_movement('cursor_right')
            if cursor != self.cursor:
                self.do_backspace(mode='del')
        elif internal_action == 'backspace':
            self.do_backspace()

        # handle action keys and text insertion
        if internal_action is None:
            self.insert_text(displayed_str)
        elif internal_action in ('shift', 'shift_L', 'shift_R'):
            if not self._selection:
                self._selection_from = self._selection_to = self.cursor_index()
                self._selection = True
            self._selection_finished = False
        elif internal_action == 'ctrl_L':
            self._ctrl_l = True
        elif internal_action == 'ctrl_R':
            self._ctrl_r = True
        elif internal_action == 'alt_L':
            self._alt_l = True
        elif internal_action == 'alt_R':
            self._alt_r = True
        elif internal_action.startswith('cursor_'):
            cc, cr = self.cursor
            self.do_cursor_movement(internal_action,
                                    self._ctrl_l or self._ctrl_r,
                                    self._alt_l or self._alt_r)
            if self._selection and not self._selection_finished:
                self._selection_to = self.cursor_index()
                self._update_selection()
            else:
                self.cancel_selection()
        elif internal_action == 'enter':
            if self.multiline:
                self.insert_text(u'\n')
        elif internal_action == 'escape':
            self.focus = False


class MainScreen(GridLayout):
    """
    The main widget we will be running the entire program on
    """
    def __init__(self, **kwargs):
        """
        :param kwargs: some initialization assignments as required by kivy
        """
        super().__init__(**kwargs)
        self.cols = 1

        # Message to the user.
        self.messageToUser = Label(
            text='[size=20][b]Welcome to the [u]Super Secret Caesar Cipher Machine![/u][/b][/size]', markup=True)
        self.add_widget(self.messageToUser)

        self.add_widget(Label(text='[size=16][b]Encode[/b][/size]', markup=True))

        # The textbox labels
        self.encodeGrid = GridLayout()
        self.encodeGrid.cols = 2
        self.encodeGrid.add_widget(Label(text='Text to encode: '))
        self.encodeGrid.add_widget(Label(text='Shift to use: '))

        # The text boxes
        self.textEncode = FocusTextInput(multiline=False)
        self.shiftEncode = FocusTextInput(multiline=False)
        self.encodeGrid.add_widget(self.textEncode)
        self.encodeGrid.add_widget(self.shiftEncode)
        self.add_widget(self.encodeGrid)

        # The submit button
        self.submitEncode = Button(text='Encode!')
        self.submitEncode.bind(on_press=self.encode_button)
        self.add_widget(self.submitEncode)

        # The result of encoding
        self.encodeResult = FocusTextInput(text='')
        self.add_widget(self.encodeResult)

        self.add_widget(Label(text='[size=16][b]Decode[/b][/size]', markup=True))

        # The textbox label
        self.add_widget(Label(text='Text to decode: '))

        # The text box
        self.textDecode = FocusTextInput(multiline=False)
        self.add_widget(self.textDecode)

        # The submit button
        self.submitDecode = Button(text='Decode!')
        self.submitDecode.bind(on_press=self.decode_button)
        self.add_widget(self.submitDecode)

        # The result of decoding
        self.decodeGrid = GridLayout()
        self.decodeGrid.cols = 2
        # The plain text
        self.decodeResult = FocusTextInput(text='')
        # The shift used to decode
        self.decodeShift = FocusTextInput(text='')
        self.decodeGrid.add_widget(self.decodeResult)
        self.decodeGrid.add_widget(self.decodeShift)
        self.add_widget(self.decodeGrid)

        # Set up focus behavior
        self.textEncode.focus_next = self.shiftEncode
        self.encodeResult.focus_next = self.textEncode
        self.textDecode.focus_next = self.decodeResult
        self.decodeShift.focus_next = self.textDecode

        self.keyboard = Window.request_keyboard (self.keyboard_closed, self, 'text')

        self.keyboard.bind(on_key_down=self.on_key_down)

    def on_key_down(self, keyboard, keycode, text, modifiers):
        """
        What to do when a user presses a key
        :param keyboard: not used; required by kivy
        :param keycode: a tuple representing the key the user entered (code representing key(int), key(str))
        :param text: not used; required by kivy
        :param modifiers: not used; required by kivy
        :return: None
        """
        if keycode == (13, 'enter'):
            # if the user focus is in the encode section, pressing enter encodes (encode_button).
            if self.textEncode.focus or self.shiftEncode.focus or self.encodeResult.focus:
                self.encode_button(None)
            # if the user focus is in the decode section, pressing enter decodes (decode_button).
            elif self.textDecode.focus or self.decodeResult.focus or self.decodeShift.focus:
                self.decode_button(None)

    def keyboard_closed(self):
        """
        :return: None
        """
        pass

    def reset_greeting(self, *args):
        """
        Resets the greeting message to the title of the program
        :return: None
        """
        self.messageToUser.text = '[size=20][b]Welcome to the [u]Super Secret Caesar Cipher Machine![/u][/b][/size]'

    def encode_button(self, instance):
        """
        Sets encodeResult to the appropriate cipher text by reading self.shiftEncode and self.textEncode
        :return: None
        """
        text = self.textEncode.text
        # try using the PlaintextMessage class to get the appropriate cipher text
        try:
            shift = int(self.shiftEncode.text)
            plain_object = classes.PlaintextMessage(text, shift)
            to_print = plain_object.get_message_text_encrypted()
            self.encodeResult.text = 'Cipher text:' + to_print
        # if the shift is not an integer, inform the user
        except ValueError:
            self.messageToUser.text = '[color=ff0000][size=20]Shift must be an integer![/size][/color]'
            Clock.schedule_once(self.reset_greeting, 2)

    def decode_button(self, instance):
        """
        Sets decodeResult to plain text and decodeShift to the shift used to get plain text, from reading self.textDecode
        :return: None
        """
        # use the CiphertextMessage class to decode the plain text
        if self.textDecode.text:
            text = self.textDecode.text
            cipher_object = classes.CiphertextMessage(text)
            to_print = cipher_object.decrypt_message()
            self.decodeResult.text = 'Plain text: ' + to_print[1]
            self.decodeShift.text = 'Shift used: ' + str(to_print[0])


class CaesarCipherApp(App):
    """
    The app that calls MainScreen widget and starts the program
    """
    def build(self):
        main_app = MainScreen()
        return main_app


if __name__ == '__main__':
    caesar_app = CaesarCipherApp()
    caesar_app.run()
