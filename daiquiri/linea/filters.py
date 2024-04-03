from daiquiri.contact.filters import DefaultMessageFilter


class LineaMessageFilter(DefaultMessageFilter):

    CHOICES = DefaultMessageFilter.CHOICES + (
        ("custom_condition", "Show to the custom group of users"),
    )

    def custom_condition(request):
        return True
