from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.template import Context
from ..models import Player, CourseTee, Club, Course, Hole, Tee, PlayerPlugin, FormatPlugin, TournamentRoundImportPlugin
from django.http import HttpResponse, JsonResponse, FileResponse
import json
from django.forms.models import model_to_dict
import zipfile
import os
import tempfile
from django.conf import settings

def printPlayers(request):
    """
    View function for printing player roster, handicaps, and course index (if default)
    """
    context = {
        'clubs': Club.objects.all(),
        'players': Player.objects.all(),
        'courseTees': CourseTee.objects.filter(default=True).values('id', 'name', 'slope', 'course__name')
    }
    htmlTemplate = get_template('golf/playerpdf.html')
    renderedHtml = htmlTemplate.render(context).encode(encoding='UTF-8')
    pdfFile = HTML(string=renderedHtml).write_pdf()
    response = HttpResponse(pdfFile, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="players.pdf"'
    return response

def clubPrintouts(request):
    """
    View function for printing roster, signup, starter and proximity sheets
    """
    retObject = {}
    retObject['club'] = list(Club.objects.all().values('name', 'logo', 'default_tournament_name', 'players_last_updated').order_by('-id'))[0]
    if (int(request.GET['cr']) > 0):
        retObject['players'] = list(Player.objects.all().order_by('priority', 'name'))
        if (int(request.GET['c1']) > 0):
            retObject['c1'] = list(CourseTee.objects.filter(id=request.GET['c1']).values('id', 'name', 'slope', 'course__name'))[0]
        if (int(request.GET['c2']) > 0):
            retObject['c2'] = list(CourseTee.objects.filter(id=request.GET['c2']).values('id', 'name', 'slope', 'course__name'))[0]
    retObject['cr'] = int(request.GET['cr'])
    retObject['crRange'] = range(retObject['cr'])
    retObject['su'] = int(request.GET['su'])
    retObject['suRange'] = range(retObject['su'])
    retObject['ss'] = int(request.GET['ss'])
    retObject['ssRange'] = range(retObject['ss'])
    retObject['pc'] = int(request.GET['pc'])
    retObject['pcRange'] = range(retObject['pc'])
    retObject['nm'] = int(request.GET['nm'])
    retObject['nmRange'] = range(retObject['nm'])
    retObject['mp'] = int(request.GET['mp'])
    retObject['mpRange'] = range(retObject['mp'])
    import logging
    logger = logging.getLogger('weasyprint')
    logger.handlers = []  # Remove the default stderr handler
    logger.addHandler(logging.FileHandler('/home/ubuntu/workspace/weasyprint.log'))

    htmlTemplate = get_template('golf/clubprintouts.html')
    context = {'clubPrintouts':retObject}
    renderedHtml = htmlTemplate.render(context).encode(encoding='UTF-8')
    pdfFile = HTML(string=renderedHtml).write_pdf()
    response = HttpResponse(pdfFile, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="clubprintouts.pdf"'
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