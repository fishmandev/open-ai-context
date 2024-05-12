from .models import Dialog
from django.views import generic
from .forms import DialogCreateForm, QueryCreateForm
from .services import send_request


class ListView(generic.ListView):
    template_name = "list.html"
    context_object_name = "dialogs"
    queryset = Dialog.objects.all()
    paginate_by = 5


class CreateView(generic.CreateView):
    model = Dialog
    template_name = "create.html"
    form_class = DialogCreateForm


class DetailView(generic.CreateView, generic.DetailView):
    model = Dialog
    template_name = "detail.html"
    form_class = QueryCreateForm

    def get_initial(self):
        initial = super().initial.copy()
        initial["dialog"] = self.get_object().id
        return initial

    def form_valid(self, form):
        print(form.instance.dialog)
        res = send_request(form.instance.dialog, form.instance.req)
        form.instance.res = res
        return super().form_valid(form)
