from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.template import Context
from ..models import Player, CourseTee, Club
from django.http import HttpResponse

def printPlayers(request):
    """
    View function for printing player roster, handicaps, and course index (if default)
    """
    context = {
        'players': Player.objects.all(),
        'clubs': Club.objects.all(),
        'courseTees': CourseTee.objects.filter(default=True).values('id', 'name', 'slope', 'course__name')
    }
    htmlTemplate = get_template('golf/playerpdf.html')
    renderedHtml = htmlTemplate.render(context).encode(encoding='UTF-8')
    pdfFile = HTML(string=renderedHtml).write_pdf()
    response = HttpResponse(pdfFile, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="players.pdf"'
    return response

def printSignupSheets(request):
    """
    View function for printing signup sheet and starter sheet
    """
    context = {
        'clubs': Club.objects.all()
    }
    htmlTemplate = get_template('golf/signupsheets.html')
    renderedHtml = htmlTemplate.render(context).encode(encoding='UTF-8')
    pdfFile = HTML(string=renderedHtml).write_pdf()
    response = HttpResponse(pdfFile, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="signupsheets.pdf"'
    return response