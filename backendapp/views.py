from django.http import HttpResponse
from django.shortcuts import render, redirect
from backendapp.models import *
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.apps import apps
from django.forms import modelform_factory


#def index(request):
#    return render(request,"backendApp/index.html",context)


def add_edit_row(request, table_name, row_id=1):
    model = apps.get_model('backendapp', table_name)
    instance = model.objects.filter(pk=row_id).first() if row_id else None
    form_class = modelform_factory(model, exclude=[])  # Create a form dynamically
    form = form_class(request.POST or None, instance=instance)

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"{'Updated' if instance else 'Added'} successfully.")
                return redirect('view_table', table_name=table_name)
            except IntegrityError as e:
                messages.error(request, f"Integrity error: {e}")
        else:
            messages.error(request, "Form submission failed. Check the entered data.")

    return render(request, 'add_edit_row.html', {
        'form': form,
        'editing': instance is not None,
        'table_name': table_name
    })

def delete_row(request, table_name, row_id):
    model = apps.get_model('your_app_name', table_name)
    instance = get_object_or_404(model, pk=row_id)

    if request.method == 'POST':
        try:
            instance.delete()
            messages.success(request, "Deleted successfully.")
        except IntegrityError as e:
            messages.error(request, f"Cannot delete: {e}")
        return redirect('view_table', table_name=table_name)

    return render(request, 'delete_confirm.html', {
        'table_name': table_name,
        'object': instance
    })

def list_tables(request):
    tables = [
        {'name': 'User'},
        {'name': 'Genre'},
        {'name': 'Publisher'},
        {'name': 'Author'},
        {'name': 'Book'},
        {'name': 'Contains'},
        {'name': 'Written'},
        {'name': 'Published'},
    ]
    return render(request, 'list_tables.html', {'tables': tables})


def view_table(request, table_name):
    model = apps.get_model('backendapp', table_name)
    objects = model.objects.all()
    fields = [field.name for field in model._meta.fields]

    rows = [
        {field: getattr(obj, field) for field in fields} for obj in objects
    ]

    idfield = list(rows[0].keys())[0]
    print(idfield)
    return render(request, 'view_table.html', {
        'table_name': table_name,
        'fields': fields,
        'rows': rows,
        'idfield': idfield,
    })


