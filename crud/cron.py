from crud.models import Upvote


def ResetUpVotes():
    Upvote.objects.all().delete()
