from haystack.signals import (
    RealtimeSignalProcessor as AbstractRealtimeSignalProcessor,
)


class RealtimeSignalProcessor(AbstractRealtimeSignalProcessor):
    def handle_save(self, sender, instance, **kwargs):
        super().handle_save(sender, instance, **kwargs)
        if hasattr(instance, "book"):
            self.update_books(sender, instance, **kwargs)

    def handle_delete(self, sender, instance, **kwargs):
        super().handle_delete(sender, instance, **kwargs)
        if hasattr(instance, "book"):
            self.update_books(sender, instance, **kwargs)

    def update_books(self, sender, instance, **kwargs):
        from books.models import Books

        if isinstance(instance.book, Books):
            for using in self.connection_router.for_write(instance=instance):
                index = (
                    self.connections[using]
                    .get_unified_index()
                    .get_index(Books)
                )
                index.update_object(instance.book, using=using)
