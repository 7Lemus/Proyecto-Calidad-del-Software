from django import forms


class Pago(forms.Form):
    nombre = forms.CharField(label='Nombre *', max_length=100)
    apellido = forms.CharField(label='Apellido *', max_length=100)
    direccion = forms.CharField(label='Dirección *', max_length=255)
    nit = forms.CharField(label='NIT', max_length=12, required=False)
    # metodo = forms.ListField(label='Método de pago', )
