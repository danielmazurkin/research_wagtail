**Проект ресерча работы с wagtail** <br/>

Переопределен метод **ready** в apps.py который задает значения для таблцы

Там описан механизм который создает таблицу в **TablePage**

В дальнейшем это может использоваться для подключения API

Также в info/management есть manage.py команда, которая позволит создать график программно

Еще стоит отметить что есть такое понятие как hooks, hooks позволяет переопределить список
получаемых данных, hooks содержится по пути info/wagtail_hooks.py

Также стоит обратить внимание на templates/wagtailadmin .html шаблоны, это шаблоны переопределили
базовое поведение админ панели, например, там содержится страница в которой сверстана таблица исходя из ролей.

В файле templates/wagtailadmin/tariffs_shows.html есть внизу javascript скрипт, который формирует эту таблицы
Так было сделано для того чтобы при подключении стилей bootstrap не возникало конфликта. Возможно есть 
более грамотный способ это сделать

Имеются url которые переопределили базовое поведение админки wagtail, а в частности CustomPageEditCustom
и InfoPageViewCustom. Эти view переопределяют базовое поведение админки wagtail. Добавил дополнительную логику
что если у страницы wagtail установлено поле edit_view_template_custom, то берется .html документ из этого поля.

Также у нас есть две библиотеки для работы с видео на проекте, это wagtailmedia, и wagtailvideo. Предпочтительнее
использовать wagtailvideo, он более заточен под работу с видео. Сами видео отображаются на HTML5 теге video.

Тезисно про видео, есть класс VideoChooserCustomPanel. Этот класс определяет внутри себя template_name. Template 
name в свою очередь определяет тот шаблон который будет отрисовываться при рендеринге видео. 

Также там переопределен метод: Внутри метод встраивается ссылка на видео если таковая имеется
в дальнейшем эта ссылка отрисовывается в HTML шаблоне.

```commandline
        def get_context_data(self, parent_context=None):
            context = super().get_context_data(parent_context)

            if hasattr(context['self'], 'instance') and context['self'].instance.header_video is not None:
                context['video_url'] = context['self'].instance.header_video.file.url
            if self.read_only:
                context.update(self.get_read_only_context_data())
            else:
                context.update(self.get_editable_context_data())
            return context
```


