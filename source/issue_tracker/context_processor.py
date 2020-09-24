from issue_tracker.forms import SimpleSearchForm

def search_form(request):
    form = SimpleSearchForm(request.GET)
    return {'search_form': form}