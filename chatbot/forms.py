# chatbot/forms.py
from django import forms

class ChatForm(forms.Form):
    message = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Nhập triệu chứng bạn gặp phải...", "class": "form-control"}),
        label=''
    )
