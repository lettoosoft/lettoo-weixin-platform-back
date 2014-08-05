from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.utils.http import base36_to_int
from django.views.generic import FormView, View
from django.views.generic.base import TemplateResponseMixin

from .models import EmailConfirmation

from .forms import ResetPasswordKeyForm
import signals


class ConfirmEmailView(TemplateResponseMixin, View):
    def get_template_names(self):
        if self.request.method == 'POST':
            return ["account/email_confirmed.html"]
        else:
            return ["account/email_confirm.html"]

    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.confirm(self.request)
        except Http404:
            self.object = None
        return redirect("https://www.calvinapp.com")

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(key=self.kwargs["key"].lower())
        except EmailConfirmation.DoesNotExist:
            raise Http404()

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs


confirm_email = ConfirmEmailView.as_view()


class PasswordResetFromKeyView(FormView):
    template_name = 'account/password_reset_from_key.html'
    form_class = ResetPasswordKeyForm
    token_generator = default_token_generator
    success_url = reverse_lazy('reset_password_done')

    def _get_user(self, uidb36):
        # pull out user
        try:
            uid_int = base36_to_int(uidb36)
        except ValueError:
            raise Http404
        return get_object_or_404(User, id=uid_int)

    def dispatch(self, request, uidb36, key, **kwargs):
        self.request = request
        self.uidb36 = uidb36
        self.key = key
        self.reset_user = self._get_user(uidb36)
        if not self.token_generator.check_token(self.reset_user, key):
            return self._response_bad_token(request, uidb36, key, **kwargs)
        else:
            return super(PasswordResetFromKeyView, self).dispatch(request,
                                                                  uidb36,
                                                                  key,
                                                                  **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PasswordResetFromKeyView, self).get_form_kwargs()
        kwargs['user'] = self.reset_user
        kwargs['temp_key'] = self.key
        return kwargs

    def form_valid(self, form):
        form.save()
        signals.password_reset.send(sender=self.reset_user.__class__,
                                    request=self.request,
                                    user=self.reset_user)
        return super(PasswordResetFromKeyView, self).form_valid(form)

    def _response_bad_token(self, request, uidb36, key, **kwargs):
        return self.render_to_response(self.get_context_data(token_fail=True))


password_reset_from_key = PasswordResetFromKeyView.as_view()


def reset_password_done(request, template='account/password_reset_done.html', extra_context=None):
    context = {}
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))
