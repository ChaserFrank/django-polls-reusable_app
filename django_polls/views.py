from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions.(not including those set to be published in the future)"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


# ---- JSON API endpoints ----

def api_index(request):
    """Return JSON list of polls."""
    polls = list(Question.objects.filter(pub_date__lte=timezone.now()).values("id", "question_text", "pub_date"))
    return JsonResponse({"polls": polls})


def api_detail(request, pk):
    """Return JSON detail for a poll."""
    poll = get_object_or_404(Question, pk=pk, pub_date__lte=timezone.now())
    choices = list(poll.choice_set.values("id", "choice_text", "votes"))
    return JsonResponse({"id": poll.id, "question_text": poll.question_text, "choices": choices})


@require_http_methods(["POST"])
def api_vote(request, pk):
    """Accept JSON body {"choice_id": <id>} and increment votes."""
    poll = get_object_or_404(Question, pk=pk, pub_date__lte=timezone.now())
    try:
        import json

        data = json.loads(request.body or b"{}")
        choice_id = data.get("choice_id")
        if choice_id is None:
            raise ValueError("choice_id missing")
        choice = poll.choice_set.get(pk=choice_id)
    except Exception:
        return HttpResponseBadRequest("Invalid request body or choice")

    choice.votes = F("votes") + 1
    choice.save()
    choice.refresh_from_db()
    return JsonResponse({"status": "ok", "choice": {"id": choice.id, "votes": choice.votes}})


def api_results(request, pk):
    poll = get_object_or_404(Question, pk=pk, pub_date__lte=timezone.now())
    choices = list(poll.choice_set.values("choice_text", "votes"))
    return JsonResponse({"question_text": poll.question_text, "results": choices})

