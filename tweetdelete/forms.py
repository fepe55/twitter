# -*- encoding: utf-8 -*-
from django import forms

class AuthForm(forms.Form):
    verifier = forms.CharField(required=True)

