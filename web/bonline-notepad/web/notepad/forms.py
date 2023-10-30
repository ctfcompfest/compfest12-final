from django import forms

class NotepadForm(forms.Form):
    notepad_text = forms.CharField(label='Input your note ')