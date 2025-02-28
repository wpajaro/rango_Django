from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=128,
        help_text="Please enter the category name."
    )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
       # Asociar el ModelForm con el modelo Category
       model = Category
       fields = ('name',) 

class PageForm(forms.ModelForm):
    title = forms.CharField(
        max_length=128,
        help_text="Please enter the title of the page."
    )
    url = forms.URLField(
        max_length=200,
        help_text="Please enter the URL of the page."
    )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Asociar el ModelForm con el modelo Page
        model = Page
        # Excluir el campo 'category' para que no aparezca en el formulario
        exclude = ('category',)
        

