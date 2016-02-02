from django.db import models


class BetTicket(models.Model):
    """
    Represents a bet ticket of Lotto owned by a specific user
    """
    created_at = models.DateTimeField(auto_now_add=True)
    bet = models.CharField(null=False, max_length=18)
    lotto_id = models.IntegerField(auto_created=True, null=True, editable=False)
    owner = models.ForeignKey('auth.User', related_name='food_orders')

    class Meta:
        ordering = ('created_at',)

    def save(self, *args, **kwargs):
        """
        Use the `random` library to create a new Lotto Result
        """
        try:
            number_list = [int(x) for x in self.bet.split(' ')]
        except ValueError:
            raise AttributeError('You should provide only numbers separated by whitespaces.')
        if len(number_list) != 6:
            raise AttributeError('You should provide 6 numbers separated by whitespaces.')
        self.bet = ' '.join([str(x) for x in sorted(number_list)])
        super(BetTicket, self).save(*args, **kwargs)
