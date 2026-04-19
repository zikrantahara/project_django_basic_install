from django.contrib.syndication.views import Feed
from django_comments.models import Comment # Menggunakan modul comment yang baru
from django.urls import reverse

class DreamrealCommentsFeed(Feed):
    title = "Dreamreal's comments"
    link = "/drcomments/"
    description = "Updates on new comments on Dreamreal entry."

    # Mengambil 5 komentar terbaru
    def items(self):
        return Comment.objects.all().order_by("-submit_date")[:5]
		
    def item_title(self, item):
        return item.user_name
		
    def item_description(self, item):
        return item.comment
		
    def item_link(self, item):
        return reverse('comment', kwargs={'object_pk': item.pk})