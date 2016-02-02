import random
from django.db import models


class LottoResult(models.Model):
    """
    Represents a result of Lotto system
    """
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    result = models.TextField(auto_created=True, editable=False, null=True)

    class Meta:
        ordering = ('created_at',)

    def save(self, *args, **kwargs):
        """
        Use the `random` library to create a new Lotto Result
        """
        self.result = ' '.join([str(x) for x in sorted(random.sample(range(1, 60), 6))])
        super(LottoResult, self).save(*args, **kwargs)
