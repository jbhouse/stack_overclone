from django.db import models
# import misaka
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from django import template
register = template.Library()

class Question(models.Model):
    title = models.CharField(max_length=256,unique=True)
    user = models.ForeignKey(User,related_name='questions')
    created_at = models.DateTimeField(auto_now=True)
    details = models.TextField()
    votes = models.IntegerField(default=0)

    # def upvote(self, user):
    #     try:
    #         self.question_votes.create(user=user, question=self, vote_type="up")
    #         self.votes += 1
    #         self.save()
    #     except IntegrityError:
    #         return 'you can only cast one upvote'
    #     return 'upvoted'
    #
    # def downvote(self, user):
    #     try:
    #         self.question_votes.create(user=user, question=self, vote_type='down')
    #         self.votes -= 1
    #         self.save()
    #     except IntegrityError:
    #         return 'you can only cast one downvote'
    #     return 'downvoted'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("questions:detail", pk=self.pk)

    class Meta:
        ordering = ['created_at']
#
# class UserVotes(models.Model):
#     user = models.ForeignKey(User, related_name="user_votes")
#     question = models.ForeignKey(Question, related_name="question_votes")
#     vote_type = models.CharField(max_length=10)
#
#     class Meta:
#         unique_together = ('user', 'question', 'vote_type')
