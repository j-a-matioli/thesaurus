from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

class EditProfileForm(UserChangeForm):
    email = forms.EmailField(label='',help_text='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Seu melhor email'}))
    first_name = forms.CharField(label='',help_text='',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Seu primeiro nome'}))
    last_name = forms.CharField(label='',help_text='',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Seu sobrenome'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden'}))
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].widget.attrs['help_text'] = '<span class="form-text text-muted"><small>Obrigatório. 50 caracteres ou menos. Letras, números e @/./+/-/_ apenas.</small></span>'
        self.fields['username'].label=""


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='',help_text='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Seu melhor email'}))
    first_name = forms.CharField(label='',help_text='',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Seu primeiro nome'}))
    last_name = forms.CharField(label='',help_text='',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Seu sobrenome'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].widget.attrs['help_text'] = '<span class="form-text text-muted"><small>Obrigatório. 50 caracteres ou menos. Letras, números e @/./+/-/_ apenas.</small></span>'
        self.fields['username'].label=""

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Escolha uma senha'
        self.fields['password1'].label=""
        self.fields['password1'].widget.attrs['help_text'] = '<ul class="form-text text-muted"><small><li>Sua senha não pode ser muito parecida com o resto das suas informações pessoais.</li><li>Sua senha precisa conter pelo menos 8 caracteres.</li><li>Sua senha não pode ser uma senha comumente utilizada.</li><li>Sua senha não pode ser uma senha comumente utilizada.</li></ul></small>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme a senha escolhida'
        self.fields['password2'].label=""
        self.fields['password2'].widget.attrs['help_text'] = '<span class="form-text text-muted"><small>Informe a mesma senha informada anteriormente, para verificação.</small></div>'
