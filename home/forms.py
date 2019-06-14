from django import forms


class ConnectionForm(forms.Form):
    username = forms.CharField(label = "Nom d'utilisateur",
        widget=forms.TextInput(attrs={"placeholder": "Nom d\'utilisateur",
        "class":"input100"}),
        error_messages={'required': 'Entrez un nom d\'utilisateur valide'}
    )
    password = forms.CharField(label = "Mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe",
        "class":"input100"}),
        error_messages={'required': 'Entrez un mot de passe valide'}
    )
