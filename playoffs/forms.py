from django import forms
from nospoil.constants import MAX_PLAYOFF_ROUNDS
from .models import Playoff


ROUND_CHOICES = tuple((i, '{} rounds'.format(i))
                      for i in xrange(2, MAX_PLAYOFF_ROUNDS+1))

class PlayoffForm(forms.ModelForm):
    class Meta:
        model = Playoff
        fields = ['sport', 'title', 'rounds', 'double', 'private']
        widgets = {'rounds': forms.Select(choices=ROUND_CHOICES)}

    def clean_rounds(self):
        rounds = self.cleaned_data['rounds']
        if 2 <= rounds <= MAX_PLAYOFF_ROUNDS:
            return rounds
        raise forms.ValidationError('Wrong rounds number')

    def save(self, user):
        playoff = super(PlayoffForm, self).save(commit=False)
        if user.is_authenticated:
            playoff.owner = user
        else:
            playoff.private = False
        playoff.save()
        return playoff
