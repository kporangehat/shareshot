from django.shortcuts import get_object_or_404, render, redirect

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse


from .models import Bundle, BundleRating

def index(request):
    latest_bundle_list = Bundle.objects.order_by('-last_modified')[:5]
    context = {'latest_bundle_list': latest_bundle_list}
    return render(request, 'library/index.html', context)


def detail(request, bundle_id):
    bundle = get_object_or_404(Bundle, pk=bundle_id)
    return render(request, 'library/detail.html', {'bundle': bundle})



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