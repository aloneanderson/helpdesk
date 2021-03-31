from django import forms
from .models import Requisitions, Comment


class RequisitionsCreateForm(forms.ModelForm):
    class Meta:
        model = Requisitions
        fields = ('status', 'title', 'text', 'active_status')


class RequisitionsUpdateForm(forms.ModelForm):
    class Meta:
        model = Requisitions
        fields = ('status', 'title', 'text', 'active_status')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class AcceptRequisitionsForm(forms.ModelForm):
    review = forms.HiddenInput()
    active_status = forms.HiddenInput()

    class Meta:
        model = Requisitions
        fields = ('review', 'active_status',)


class CancelRequisitionsForm(forms.ModelForm):
    class Meta:
        model = Requisitions
        fields = '__all__'


class RecoveryRequisitionsForm(forms.ModelForm):
    class Meta:
        model = Requisitions
        fields = ('recovery',)
