from django.urls import reverse
import logging

info = logging.info
debuf = logging.debug

from uil.questions.blueprints import Blueprint

from .models import Registration
from .forms import NewRegistrationQuestion, CategoryQuestion, \
    TraversalQuestion, QUESTIONS, FacultyQuestion, \
    UsesInformationQuestion, ConfirmInformationUseQuestion, \
    SubmitQuestion



class RegistrationBlueprint():

    model = Registration
    primary_questions = [NewRegistrationQuestion,
    ]

    def __init__(self, registration):

        self.required = []
        self.completed = []

        self.consumers = [BasicDetailsConsumer]
        self.registration = registration
        self.desired_next = None

        self.evaluate()

    def evaluate(self, consumers=None):
        """Go through the list of consumers and try to satisfy their needs"""

        # First run, get all consumers
        if consumers == None:
            consumers = self.consumers

        # We've run out of consumers
        if consumers == []:
            return True

        current = consumers[0](self)

        next_consumers = current.consume() + consumers[1:]

        return self.evaluate(consumers=next_consumers)

    def get_desired_next_url(self):
        if self.desired_next in QUESTIONS.values():
            if self.desired_next.model == Registration:
                question = self.desired_next(instance=self.registration)
                info(question.instance)
                return question.get_edit_url()
        return reverse(
            "registrations:overview",
            kwargs={
                "reg_pk": self.registration.pk,
            })


def instantiate_question(registration, question):
    """Take a question and registration, and return an
    instantiated question for validation and introspection
    """
    q_model_name = question.model.__name__
    q_object = getattr(registration, q_model_name)
    return question(instance=q_object)


class BaseConsumer:

    def __init__(self, blueprint):

        self.blueprint = blueprint

    def complete(self, out_list):

        return out_list

class BaseQuestionConsumer(BaseConsumer):

    questions = []

    def get_question_errors(self):

        self.question = instantiate_question(
            self.registration,
            self.question,
        )

        errors = self.question.errors
        info(f'Errors in question {self.question}: {errors}')

        return errors

    def complete(self, out_list):

        self.blueprint.completed += self.questions

        return super().complete(out_list)

class BasicDetailsConsumer(BaseConsumer):

    questions = [
        NewRegistrationQuestion,
        FacultyQuestion,
        ]

    def consume(self):

        if self.check_details():
            self.blueprint.desired_next = UsesInformationQuestion
        else:
            return self.complete([])

        return [UsesInformationConsumer]

    def check_details(self):

        registration = self.blueprint.registration

        for field in [registration.title,
                      registration.faculty,
                      ]:
            info(field)

        return fields_not_empty(
            [registration.title,
             registration.faculty,
            ]
        )

class TraversalConsumer(BaseQuestionConsumer):

    questions = [TraversalQuestion]

    def consume(self):

        if self.check_details():
            self.blueprint.desired_next = UsesInformationQuestion

        return []

    def check_details(self):

        return fields_not_empty(self.question.Meta.fields)


class UsesInformationConsumer(BaseQuestionConsumer):

    questions = [UsesInformationQuestion]

    def consume(self):

        if not self.check_details():
            return []

        answer = self.blueprint.registration.uses_information
        if answer  == False:
            self.blueprint.desired_next = ConfirmInformationUseQuestion
            return []
        elif answer == True:
            self.blueprint.desired_next = TraversalQuestion

        return []

    def check_details(self):

        return fields_not_empty(self.questions[0].Meta.fields)




class ConfirmInformationUseConsumer(BaseQuestionConsumer):

    questions = [ConfirmInformationUseQuestion]

    def consume(self):

        return []

    def check_details(self):

        return fields_not_empty(self.questions[0].Meta.fields)

        

        
def fields_not_empty(fields):
    for f in fields:
        if f in ['', None]:
            info(f, 'was not filled in')
            return False
    return True
