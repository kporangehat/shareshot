from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Bundle, BundleRating


class IndexView(generic.ListView):
    template_name = 'library/index.html'
    context_object_name = 'latest_bundle_list'

    def get_queryset(self):
        """Return the last five updated bundles."""
        return Bundle.objects.order_by('-last_modified')[:5]


class DetailView(generic.DetailView):
    model = Bundle
    template_name = 'library/detail.html'


# class CategoryListView(generic.ListView):
#     template_name = 'library/category.html'
#     context_object_name = 'category_list'
#
#     def get_queryset(self):
#         """Return the last five updated bundles."""
#         return Bundle.objects.order_by('-last_modified')[:5]


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