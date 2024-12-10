from django.http import HttpResponse
from django.shortcuts import render, redirect
from backendapp.models import *
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.apps import apps
from django.forms import modelform_factory
from django.db.models import CASCADE
from django.db import transaction
from .forms import AddBookForm

#def index(request):
#    return render(request,"backendApp/index.html",context)



def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Save the Book entry
                    Book_List = form.save(commit=False)
                    Book_List.save()

                    # Save the Genres in the Contains table
                    genres = form.cleaned_data['GenreIDs']
                    for genre in genres:
                        Book_and_Genres.objects.create(BookID=Book_List, GenreName=genre)

                    messages.success(request, "Book and associated genres added successfully!")
                    return redirect('view_table', table_name='Book_List')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AddBookForm()

    return render(request, 'add_book.html', {'form': form})

def add_edit_row(request, table_name, row_id=None):
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
    model = apps.get_model('backendapp', table_name)
    instance = get_object_or_404(model, pk=row_id)

    # Pre-fetch related objects that will be deleted due to cascade
    related_objects = []
    for related in model._meta.related_objects:
        related_model = related.related_model
        related_field_name = related.field.name
        if related.on_delete == CASCADE:  # Only consider cascading deletes
            related_queryset = related_model.objects.filter(**{related_field_name: instance})
            if related_queryset.exists():
                related_objects.append({
                    'model': related_model._meta.verbose_name_plural,
                    'objects': list(related_queryset)  # Convert queryset to list for rendering
                })

    if request.method == 'POST':
        # Collect details of the objects to be deleted
        deleted_details = []
        for related in related_objects:
            deleted_details.append(f"{len(related['objects'])} {related['model']}")

        # Perform the deletion
        try:
            instance.delete()
            success_message = f"Deleted successfully. Additionally deleted: {', '.join(deleted_details)}." if deleted_details else "Deleted successfully."
            messages.success(request, success_message)
        except IntegrityError as e:
            messages.error(request, f"Cannot delete: {e}")
        return redirect('view_table', table_name=table_name)

    # Render confirmation page with the list of related objects
    return render(request, 'delete_confirm.html', {
        'table_name': table_name,
        'object': instance,
        'related_objects': related_objects
    })


def list_tables(request):
    tableslist = [
        {'name': 'list_of_registered_users'},
        {'name': 'Book_Genres'},
        {'name': 'Book_Publishers'},
        {'name': 'Book_Authors'},
        {'name': 'Book_List'},
        {'name': 'Book_and_Genres'},
        {'name': 'Book_and_Authors'},
        {'name': 'Book_and_Publishers'},
    ]

    # Fetch the 7 most recent changes
    recent_changes = ChangeLog.objects.order_by('-timestamp')[:7]

    # Count the number of records for each table
    book_count = Book_List.objects.count()
    author_count = Book_Authors.objects.count()
    publisher_count = Book_Publishers.objects.count()
    genre_count = Book_Genres.objects.count()

    # Handle delete request for recent changes
    if request.method == "POST" and 'delete_changes' in request.POST:
        ChangeLog.objects.all().delete()
        return redirect('list_tables')  # Redirect to refresh the page


    return render(request, 'list_tables.html', 
                  {'tables': tableslist,
                   'recent_changes': recent_changes,
                    'book_count': book_count,
                    'author_count': author_count,
                    'publisher_count': publisher_count,
                    'genre_count': genre_count,

})


def view_table(request, table_name):
    model = apps.get_model('backendapp', table_name)
    objects = model.objects.all()
    fields = [field.name for field in model._meta.fields]


    rows = [
        {field: getattr(obj, field) for field in fields} for obj in objects
    ]

    idfield = model._meta.fields[0].name
    print("id is "+ idfield)
    return render(request, 'view_table.html', {
        'table_name': table_name,
        'fields': fields,
        'rows': rows,
        'idfield': idfield,
    })


