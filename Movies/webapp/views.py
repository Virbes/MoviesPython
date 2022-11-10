from django.db import connection
from personas.models import Persona
from django.forms import modelform_factory
from django.shortcuts import render, get_object_or_404, redirect

# Variables declaration
PersonaForm = modelform_factory(Persona, exclude=[])
# End of variables declaration


def bienvenido(request):
    context = {
        'no_personas': Persona.objects.count(),
        'personas': Persona.objects.all()
    }
    return render(request, 'bienvenido.html', context)


def detallePersona(request, id):
    # persona = Persona.objects.get(pk=id)
    persona = get_object_or_404(Persona, pk=id)

    context = {'persona': persona}
    return render(request, 'personas/detalle.html', context)


def nuevaPersona(request):
    context = {'formaPersona': PersonaForm()}

    if request.method == 'POST':
        forma_persona = PersonaForm(request.POST)

        if forma_persona.is_valid():
            forma_persona.save()

            return redirect('inicio')

    return render(request, 'personas/nuevo.html', context)


def testQuery(request):
    with connection.cursor() as cursor:
        query = "SELECT * FROM Movies"
        cursor.execute(query)
        row = cursor.fetchone()
        # all_count, yes_count = row

        context = {'movie': row}
        return render(request, 'personas/nuevo.html', context)
