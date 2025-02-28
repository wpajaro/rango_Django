from django.shortcuts import render, redirect
from django.http import HttpResponse 
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.urls import reverse

def index(request):
    # Construye un diccionario para pasar al motor de plantillas
    # como su contexto. ¡Observa que la clave 'boldmessage' coincide
    # con {{ abolmessage }} en la plantilla!
    context_dict = {
        'aboldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'
    }

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict['categories'] = category_list

    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list

    # Agregar la lista al diccionario de contexto (junto con nuestro mensaje destacado)
    # que será pasado al motor de plantillas.


    # Retorna una respuesta renderizada para enviar al cliente.
    # Utilizamos la función abreviada para facilitar nuestra vida.
    # Observa que el primer parámetro es la plantilla que deseamos usar.
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    # crear un diccionario de contexto que podamos usar
    # al motor de renderizado de plantillas
    context_dict = {}

    try: 
        # ¿Podemos encontrar un slug de categoría con el nombre dado?  
        # Si no podemos, el método .get() lanza una excepción DoesNotExist.  
        # El método .get() devuelve una instancia del modelo o lanza una excepción.  
        category = Category.objects.get(slug=category_name_slug)

        # Recuperar todas las páginas asociadas.  
        # El método filter() devolverá una lista de objetos de página o una lista vacía.
        pages = Page.objects.filter(category=category)

        # Agregar la lista de resultados al contexto con el nombre "pages".  
        context_dict['pages'] = pages

        # También agregamos el objeto categoría de la base de datos  
        # al diccionario de contexto. Lo usaremos en la plantilla  
        # para verificar que la categoría existe.  
        context_dict['category'] = category

    except Category.DoesNotExist:
        # Llegamos aquí si no encontramos la categoría especificada.  
        # No hacemos nada:  
        # la plantilla mostrará el mensaje "no hay categoría" por nosotros. 
        context_dict['category'] = None
        context_dict['pages'] = None

    # Renderizamos la respuesta y la devolvemos al cliente.  
    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    form = CategoryForm()

    # ¿Se ha recibido una solicitd HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # ¿El formulario es válido?
        if form.is_valid():
            #Guardar la nueva categoría en la base de datos
            form.save(commit=True)

            # Ahora que la categoría está guardada, podríamos confirmarlo.
            # Por ahora, solo redirigimos al usuario a la vista de inicio.
            return redirect('/rango/')
        else:
            # El formulario contiene errores, los imprimos en la terminal.
            print(form.errors)
    
    # Maneja casos en los que el formulario es válido, nuevo o no se ha proporcionado.
    # Renderiza el formulario con los mensajes de error (si los hay).
    return render(request, 'rango/add_category.html', {'form': form})



def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    if category is None:
        return redirect(reverse('rango:index'))
    
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
            
            return redirect(reverse('rango:show_category',
                                     kwargs={'category_name_slug':
                                             category_name_slug}))
        
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
