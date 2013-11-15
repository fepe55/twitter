# -*- encoding: utf-8 -*-
from django import forms

class AuthForm(forms.Form):
    token = forms.CharField(required=True)
    verifier = forms.CharField(required=True)

