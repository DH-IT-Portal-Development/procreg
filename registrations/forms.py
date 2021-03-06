from django.utils.translation import ugettext_lazy as _
from django import forms
from django.urls import reverse

from uil.questions import questions
from .models import Registration, ParticipantCategory



class RegistrationQuestionMixin:

    show_progress = False

    def __init__(self, *args, **kwargs):

        self.reg_pk = kwargs.pop('reg_pk', None)
        return super().__init__(*args, **kwargs)


    def get_edit_url(self):

        if not hasattr(self.instance, 'registration'):
            self.instance.registration = self.instance

        return reverse(
            'registrations:edit_question',
            kwargs={
                'question': self.slug,
                'question_pk': self.instance.pk,
                'reg_pk': self.instance.registration.pk,
            }
        )

    def instantiate_from_blueprint(blueprint):

        return super()(instance=blueprint.registration)


class NewRegistrationQuestion(RegistrationQuestionMixin,
        questions.Question,):

    title = _("registrations:forms:registration_title")
    model = Registration
    slug = 'new_reg'
    is_editable = True

    class Meta:
        model = Registration
        fields = [
            'title',
        ]

    def get_segments(self):

        segments = []
        segments.append(self._field_to_segment('title'))

        return segments

class FacultyQuestion(RegistrationQuestionMixin, questions.Question):

    show_progress = True
    
    class Meta:
        model = Registration
        fields = [
            'faculty',
        ]

    title = _("registrations:forms:faculty_question_title")
    model = Registration
    slug = "faculty"
    is_editable = True


    def get_segments(self):

        segments = []
        segments.append(self._field_to_segment('faculty'))

        return segments


class TraversalQuestion(RegistrationQuestionMixin, questions.Question):

    show_progress = True

    class Meta:
        model = Registration
        fields = [
            'date_start',
            'date_end',
        ]

    title = _("registrations:forms:traversal_question_title")
    description = _("registrations:forms:traversal_question_description")
    model = Registration
    slug = "traversal"
    is_editable = True


    def get_segments(self):

        segments = []
        segments.append(self._field_to_segment('date_start'))
        segments.append(self._field_to_segment('date_end'))

        return segments



class CategoryQuestion(RegistrationQuestionMixin, questions.Question):

    show_progress = True
    
    class Meta:
        model = ParticipantCategory
        fields = [
            'name',
            'number',
            'has_consented',
        ]

    title = "registrations:forms:category_question_title"
    description = "registrations:forms:category_question_description"
    is_editable = True
    slug = "category"
    model = ParticipantCategory

    def get_segments(self):

        segments = []
        segments.append(self._field_to_segment('name'))
        segments.append(self._field_to_segment('number'))
        segments.append(self._field_to_segment('has_consented'))


        return segments

    def save(self, *args, **kwargs):

        reg = Registration.objects.get(pk=self.reg_pk)
        self.instance.registration = reg
        return super().save(*args, **kwargs)



Q_LIST = [NewRegistrationQuestion,
          FacultyQuestion,
          CategoryQuestion,
          TraversalQuestion,
          ]

QUESTIONS = {q.slug: q for q in Q_LIST}
