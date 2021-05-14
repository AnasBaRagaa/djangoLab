from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.views import generic
from .forms import EntryForm, ContactForm
from phonebook.models import Contact, Entry
from django.urls import reverse, reverse_lazy
from .forms import UserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
"""
owner : Anas Ba Ragaa


"""

def index(request):
    contact_list = Contact.objects.all()
    context = {'contacts_list': contact_list}
    return render(request, 'phonebook/index.html', context)


def detail(request, contact_id):
    c = get_object_or_404(Contact, pk=contact_id)
    return render(request, 'phonebook/detail.html', {'contact': c})


class IndexView(generic.ListView):
    template_name = 'phonebook/index.html'
    context_object_name = 'contacts_list'

    def get_queryset(self):
        return Contact.objects.all()


class DetailView(generic.DetailView):
    model = Contact
    template_name = 'phonebook/detail.html'


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request=request, user=user)
            messages.success(request, 'Successful registration')
            return redirect('phonebook:index')
        messages.error(request, 'Unsuccessful registration')
    form = UserForm
    return render(request, template_name="registration/register.html", context={'form': form})


def logout_user(request):
    logout(request)
    messages.info(request, "User logged out")
    return redirect('phonebook:index')


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            u = authenticate(request, username=username, password=password)
            if u is not None:
                login(request, u)
                messages.info(request, 'Logged in as {}'.format(username))
                return redirect('phonebook:index')
            else:
                messages.error(request, "Wrong username or password.")
        else:
            messages.error(request, "Wrong username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name='registration/login.html', context={'form': form})


# Subclassing the generic classes to include ownership check and assignment of the records and enforce login
# Enforce login by subclassing LoginRequiredMixin
class BaseListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'objects'

    # filter based on the current user
    def get_queryset(self, *args, **kwargs):
        qs = super(BaseListView, self).get_queryset(*args, **kwargs)
        qs = qs.filter(owner=self.request.user)  # show only the objects belonging to the current user
        return qs


class BaseDeleteView(LoginRequiredMixin, generic.DeleteView):
    success_message = "Record was deleted successfully."
    template_name = 'phonebook/delete.html'  # Generic template

    # overide get_object to prevent users from accessing records they do not own
    def get_object(self, queryset=None):
        obj = super(BaseDeleteView, self).get_object()
        if obj.owner != self.request.user:
            raise Http404('You do not own this record')  # prevent users from deleting records they do not own
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)  # send feedback to the user when record is deleted
        return super(BaseDeleteView, self).delete(request, *args, **kwargs)


class BaseUpdateView(LoginRequiredMixin, generic.UpdateView):
    success_message = "Record was updated successfully."
    template_name = 'phonebook/update.html.html'  # Generic template

    def get_object(self, queryset=None):
        obj = super(BaseUpdateView, self).get_object()
        if obj.owner != self.request.user:
            raise Http404  # prevent users from accessing records they do not own
        return obj

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(BaseUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(BaseUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class BaseCreateView(LoginRequiredMixin, generic.CreateView):
    success_message = "Record was added successfully."

    # send  current user to the form
    def get_form_kwargs(self):
        kwargs = super(BaseCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    # save the current user as the owner of the created record
    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user  # add owner to the record
        messages.success(self.request, self.success_message)

        return super(BaseCreateView, self).form_valid(form)


###############################################
# Now we can create our views for each model with few lines of code

class CreateEntry(BaseCreateView):
    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy('phonebook:index')
    template_name = 'phonebook/test.html'


######################################
class IndexView(BaseListView):
    template_name = 'phonebook/index.html'
    context_object_name = 'contacts_list'
    model = Contact
##################################
class CreateContact(BaseCreateView):
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('phonebook:index')
    template_name = 'phonebook/test.html'


class UpdateContact(BaseUpdateView):
    template_name = 'phonebook/update.html'
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('phonebook:index')
    # Note that we are using the generic template at phonebook/update.html which is declared in BaseUpdateView
    # You can override template_name if you have a customized template


class UpdateEntry(BaseUpdateView):
    template_name = 'phonebook/update.html'
    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy('phonebook:index')


class DeleteContact(BaseDeleteView):
    model = Contact
    success_url = reverse_lazy('phonebook:index')


class DeleteEntry(BaseDeleteView):
    model = Entry
    success_url = reverse_lazy('phonebook:index')
