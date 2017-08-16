from django.core.management.base import BaseCommand
from questions.models import Question
from tags.models import Tag

class Command(BaseCommand):

    titles = ['a','b','c','d','e','f','g','h']
    descriptions = ['A','B','C','D','E','F','G','H']
    tags = ['Javascript','Ruby','Python','Node.js','Rails','Django','HTML','CSS']

    def _create_tags_and_questions(self):
        for i in range(len(self.titles)):
            current_question = Question(id = i, title = self.titles[i], user_id=0, details = self.descriptions[i])
            current_question.save()
            tag = Tag(id = i, name = self.tags[i])
            tag.save()

    def handle(self, *args, **options):
        self._create_tags_and_questions()
