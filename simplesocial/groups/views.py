from django.contrib.auth.mixins import (LoginRequiredMixin,PermissionRequiredMixin)
from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib import messages
from . import models


from groups.models import Group,GruopMember
# Create your views here.

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ('name','description') #user can edit this
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroup(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug = self.kwargs.get('slug'))

        try:
            GruopMember.objects.create(user=self.request.user, group = group)

        except:
            messages.warning(self.request,('Warning Already a member'))
        else:
            messages.success(self.request,('You are now a member!'))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})


    def get(self,request,*args,**kwargs):

        try:
            membership = models.GroupMember.objects.filter(
                user = self.request.user,
                group__slug = self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry You are not in this Grouop!')
        else:
            membership.delete()
            messages.success(self.request,'You Have Left the Group!')
        
        return super().get(request, *args, **kwargs)
