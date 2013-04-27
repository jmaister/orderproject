from django import template


register = template.Library()


@register.inclusion_tag('base/formset.html')
def formset_table(formset, rowclass, *args, **kwargs):
    return {
        'formset': formset,
        'rowclass': rowclass,
    }


@register.inclusion_tag('base/formset_bootstrap.html')
def formset_table_bootstrap(formset, rowclass, *args, **kwargs):
    return {
        'formset': formset,
        'rowclass': rowclass,
    }

