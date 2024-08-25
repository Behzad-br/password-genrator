import random
import string
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.core.clipboard import Clipboard
from kivy.uix.popup import Popup
from kivy.core.window import Window


class PasswordGeneratorApp(App):

    def build(self):
        self.title = "Password Generator"

        # Set the background color of the window to a light color
        Window.clearcolor = (0.9, 0.9, 0.9, 1)  # Light gray background

        # Root Layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Password Length
        length_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        length_label = Label(text="Password Length:", size_hint=(0.4, 1), color=(0, 0, 0, 1))  # Black text
        self.length_input = TextInput(multiline=False, input_filter='int', hint_text="Enter length",
                                      background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        length_layout.add_widget(length_label)
        length_layout.add_widget(self.length_input)
        layout.add_widget(length_layout)

        # Include Uppercase Letters Checkbox
        self.uppercase_checkbox = CheckBox(active=False, color=(0, 0, 0, 1))
        uppercase_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        uppercase_label = Label(text="Include Uppercase Letters:", size_hint=(0.6, 1), color=(0, 0, 0, 1))
        uppercase_layout.add_widget(uppercase_label)
        uppercase_layout.add_widget(self.uppercase_checkbox)
        layout.add_widget(uppercase_layout)

        # Include Digits Checkbox
        self.digits_checkbox = CheckBox(active=False, color=(0, 0, 0, 1))
        digits_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        digits_label = Label(text="Include Digits:", size_hint=(0.6, 1), color=(0, 0, 0, 1))
        digits_layout.add_widget(digits_label)
        digits_layout.add_widget(self.digits_checkbox)
        layout.add_widget(digits_layout)

        # Include Special Characters Checkbox
        self.special_checkbox = CheckBox(active=False, color=(0, 0, 0, 1))
        special_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        special_label = Label(text="Include Special Characters:", size_hint=(0.6, 1), color=(0, 0, 0, 1))
        special_layout.add_widget(special_label)
        special_layout.add_widget(self.special_checkbox)
        layout.add_widget(special_layout)

        # Generate Button
        generate_button = Button(text="Generate Password", size_hint=(1, 0.2),
                                 background_color=(0.6, 0.9, 0.6, 1), color=(0, 0, 0, 1))  # Light green
        generate_button.bind(on_press=self.generate_password)
        layout.add_widget(generate_button)

        # Generated Password Output
        self.result_label = Label(text="", size_hint=(1, 0.2), color=(0, 0, 0, 1))  # Black text
        layout.add_widget(self.result_label)

        # Copy to Clipboard Button
        copy_button = Button(text="Copy to Clipboard", size_hint=(1, 0.2),
                             background_color=(0.6, 0.6, 0.9, 1), color=(0, 0, 0, 1))  # Light blue
        copy_button.bind(on_press=self.copy_to_clipboard)
        layout.add_widget(copy_button)

        return layout

    def generate_password(self, instance):
        try:
            length = int(self.length_input.text)
            if length <= 0:
                raise ValueError("Length must be positive.")
        except ValueError:
            self.show_error("Invalid Input", "Please enter a valid positive number for the password length.")
            return

        # Characters pool based on user selection
        characters = string.ascii_lowercase
        if self.uppercase_checkbox.active:
            characters += string.ascii_uppercase
        if self.digits_checkbox.active:
            characters += string.digits
        if self.special_checkbox.active:
            characters += string.punctuation

        if not characters:
            self.show_error("No Characters Selected", "Please select at least one character type.")
            return

        password = ''.join(random.choice(characters) for _ in range(length))
        self.result_label.text = "Generated Password: " + password

    def copy_to_clipboard(self, instance):
        if self.result_label.text.startswith("Generated Password: "):
            Clipboard.copy(self.result_label.text.split(": ")[1])
            self.show_popup("Copied", "Password copied to clipboard")
        else:
            self.show_error("No Password", "Please generate a password first.")

    def show_error(self, title, message):
        popup = Popup(title=title, content=Label(text=message, color=(1, 0, 0, 1)),
                      size_hint=(0.8, 0.4))
        popup.open()

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message, color=(0, 1, 0, 1)),
                      size_hint=(0.8, 0.4))
        popup.open()


if __name__ == "__main__":
    PasswordGeneratorApp().run()
