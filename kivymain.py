import kivy
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import classes


class MainScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        # Message to the user. 
        self.messageToUser = Label(text='[size=20][b]Welcome to the [u]Super Secret Caesar Cipher Machine![/u][/b][/size]', markup=True)
        self.add_widget(self.messageToUser)

        self.add_widget(Label(text='[size=16][b]Encode[/b][/size]', markup=True))

        # The textbox labels
        self.encodeGrid = GridLayout()
        self.encodeGrid.cols = 2
        self.encodeGrid.add_widget(Label(text='Text to encode: '))
        self.encodeGrid.add_widget(Label(text='Shift to use: '))

        # The text boxes
        self.textEncode = TextInput(multiline=False)
        self.shiftEncode = TextInput(multiline=False)
        self.encodeGrid.add_widget(self.textEncode)
        self.encodeGrid.add_widget(self.shiftEncode)
        self.add_widget(self.encodeGrid)

        # The submit button
        self.submitEncode = Button(text='Encode!')
        self.submitEncode.bind(on_press=self.encode_button)
        self.add_widget(self.submitEncode)

        # The result of encoding
        self.encodeResult = Label(text='')
        self.add_widget(self.encodeResult)

        self.add_widget(Label(text='[size=16][b]Decode[/b][/size]', markup=True))

        # The textbox label
        self.add_widget(Label(text='Text to decode: '))

        # The text box
        self.textDecode = TextInput(multiline=False)
        self.add_widget(self.textDecode)

        # The submit button
        self.submitDecode = Button(text='Decode!')
        self.submitDecode.bind(on_press=self.decode_button)
        self.add_widget(self.submitDecode)

        # The result of decoding
        self.decodeGrid = GridLayout()
        self.decodeGrid.cols = 2
        # The plain text
        self.decodeResult = Label(text='')
        # The shift used to decode
        self.decodeShift = Label(text='')
        self.decodeGrid.add_widget(self.decodeResult)
        self.decodeGrid.add_widget(self.decodeShift)
        self.add_widget(self.decodeGrid)

    def reset_greeting(self, *args):
        self.messageToUser.text = '[size=20][b]Welcome to the [u]Super Secret Caesar Cipher Machine![/u][/b][/size]'

    def encode_button(self, instance):
        text = self.textEncode.text
        try:
            shift = int(self.shiftEncode.text)
            plain_object = classes.PlaintextMessage(text, shift)
            to_print = plain_object.get_message_text_encrypted()
            self.encodeResult.text = 'Cipher text:' + to_print
        except ValueError:
            self.messageToUser.text = '[color=ff0000]Shift must be an integer![/color]'
            Clock.schedule_once(self.reset_greeting, 2)

    def decode_button(self, instance):
        text = self.textDecode.text
        cipher_object = classes.CiphertextMessage(text)
        to_print = cipher_object.decrypt_message()
        self.decodeResult.text = 'Plain text: ' + to_print[1]
        self.decodeShift.text = 'Shift used: ' + str(to_print[0])


class MainApp(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    caesar_app = MainApp()
    caesar_app.run()
