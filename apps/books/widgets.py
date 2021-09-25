from django.forms import widgets
from django.utils.safestring import mark_safe


class SlimSelect(widgets.SelectMultiple):
    def __init__(self, empty=False, *args, **kwargs):
        self.empty = empty
        self.options = {
            "show_search": str(kwargs.pop("show_search", True)).lower(),
            "extra": "",
            "deselectLabel": kwargs.pop("deselectLabel", False),
            "allowDeselect": kwargs.pop("allowDeselect", False),
        }
        super(SlimSelect, self).__init__(*args, **kwargs)
        self.script = """
            var id_{name_var} = new window.SlimSelect({{
              select: "#id_{name}",
              showSearch: {show_search},
              {extra}
            }});
            $(document).ready(function(){{
                $('#' + id_{name_var}.config.id + ' .ss-deselect').addClass('hidden');
                $('#id_{name}').change(function(){{
                    if($(this).val()){{
                        $('#' + id_{name_var}.config.id + ' .ss-deselect').removeClass('hidden')
                    }}else{{
                        $('#' + id_{name_var}.config.id + ' .ss-deselect').addClass('hidden')
                    }}
                }});
            }})
        """

    def render(self, name, value, attrs=None, renderer=None):
        options = self.options.copy()
        if options["deselectLabel"]:
            options[
                "extra"
            ] += """deselectLabel: '<span class="red">✖</span>',"""
        if options["allowDeselect"]:
            options["extra"] += """allowDeselect: true,"""
        script = """<script type="text/javascript">
        $(document).ready(function(){
            %s
        })
        </script>""" % (
            self.script.format(
                name=name,
                name_var=name.replace("-", "_"),
                **options,
            )
        )
        return super(SlimSelect, self).render(
            name, value, attrs=attrs, renderer=renderer
        ) + mark_safe(script)

    def optgroups(self, name, value, attrs=None):
        optgroups = super(SlimSelect, self).optgroups(name, value, attrs=attrs)
        if not self.empty:
            return optgroups
        if (
            len(optgroups) > 0
            and optgroups[0][1][0]["selected"]
            and optgroups[0][1][0]["value"] == ""
        ):
            optgroups[0][1][0]["selected"] = False
            optgroups[0][1][0]["attrs"].update({"selected": False})
        return optgroups
