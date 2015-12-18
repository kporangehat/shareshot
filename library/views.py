from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
import logging
from .models import Bundle, BundleRating, BundleType

import base64
import markdown2
from library.models import Release

class IndexView(generic.ListView):
    template_name = 'library/index.html'
    context_object_name = 'bundle_list'

    def get_queryset(self):
        """Return the last five updated bundles."""
        return Bundle.objects.order_by('-last_modified')[:15]


class DetailView(generic.DetailView):
    model = Bundle
    template_name = 'library/detail.html'

    def get_releases(self):
        release_list = Release.objects.filter(bundle=self.object)
        return release_list

    def get_labels(self):
        label_list = self.object.tags.split(",")
        return label_list

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['readme_html'] = markdown2.markdown(base64.b64decode(self.object.readme))
        context['release_list'] = self.get_releases()
        context['label_list'] = self.get_labels()
        return context

class CategoryListView(generic.ListView):
    template_name = 'library/index.html'
    context_object_name = 'bundle_list'

    # category = get_object_or_404(BundleType, pk=self.kwargs['bundle_type_id'])
    def get_queryset(self):
        """Return all bundles for the category."""
        self.category = get_object_or_404(BundleType, name=self.kwargs['bundle_type'])
        return Bundle.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['category'] = self.category.name
        return context


def bundle_type_list(request, bundle_type_id):
    response = "Library list by bundle type %s."
    return HttpResponse(response % bundle_type_id)


def rate(request, bundle_id):
    bundle = get_object_or_404(Bundle, pk=bundle_id)
    try:
        rating = int(request.POST['rating'])
        if rating not in range(1,5):
            raise ValueError
    except ValueError:
        # Redisplay the question voting form.
        return render(request, 'library/detail.html', {
            'bundle': bundle,
            'error_message': "Invalid rating",
        })
    rating = BundleRating(bundle_id=bundle_id, rating=request.POST['rating'])
    rating.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('library:detail', args=(bundle.id,)))