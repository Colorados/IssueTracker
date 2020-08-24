from django.db import models



class Issues(models.Model):
    summary = models.CharField(max_length=200, null=False, blank=False, verbose_name='Краткое описание')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Полное описание')
    status = models.ForeignKey('issue_tracker.Status', null=False, blank=False, related_name='statuses',
                               on_delete=models.PROTECT,
                               verbose_name='Статус')
    types = models.ManyToManyField('issue_tracker.Type', related_name='issue_set', blank=True, verbose_name='Типы')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return "{}. {}".format(self.pk, self.summary)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

class Status(models.Model):
    status_name = models.CharField(max_length=15, null=False, blank=False, verbose_name='Название статуса')

    def __str__(self):
        return "{}. {}".format(self.pk, self.status_name)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Type(models.Model):
    type_name = models.CharField(max_length=15, null=False, blank=False, verbose_name='Название типа')

    def __str__(self):
        return "{}. {}".format(self.pk, self.type_name)

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'