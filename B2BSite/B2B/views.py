from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Company, Person

import requests
import sys
sys.path.append('.\..\checkmate')
import checkmate
from checkmate import SiteBookData
#from .checkmate import *
# Create your views here.

@login_required
def home(request):

    #print(checkmate.get_book_site('lc').slug)
    
    context = {

    }
    return render(request, 'home.html', context = context)

    

class Results(LoginRequiredMixin, generic.ListView):
    queryset = SiteBookData
    template_name = 'results.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        book_title = self.request.GET.get("title_field")
        author_list = self.request.GET.get("authors_field")
        book_ISBN = self.request.GET.get("ISBN_field")
        #book_match_percentage = self.request.GET.get("isbn_field")
        book_JSON = self.request.GET.get("JSON_field")
        error_message = ''

        #testing this
        if book_JSON != '':
            if book_title == '' and author_list == '' and book_ISBN == '':
                print("1")
                pass #searching with only JSON
            else:
                print("2")
                context['error_message'] = "You must enter only JSON data OR title, author, and/or ISBN information into the search fields. Return Home to retry." #to home with must search by JSON only or not error
                return context
        else:
            if book_title == '' and author_list == '' and book_ISBN == '':
                print("3")
                context['error_message'] = "Search fields were left blank. Please return to Home and enter search information." #to home with empty exception
                return context
            else:
                print("4")
                pass #search using only non-JSON
        
        
        book_authors = []
        temp = ""
        if author_list != None:
            for letter in author_list:
                if letter == ",":
                    book_authors.append(temp)
                    temp = ""
                else:
                    temp = temp + letter
            book_authors.append(temp)
        

        book_data = SiteBookData(book_ISBN, book_title, book_authors)

        #needs to come from active company
        KB_toggle = True
        KB_list = checkmate.get_book_site('kb').find_book_matches_at_site(book_data)
        GB_toggle = False
        GB_list = checkmate.get_book_site('gb').find_book_matches_at_site(book_data)
        LC_toggle = True
        LC_list = checkmate.get_book_site('lc').find_book_matches_at_site(book_data)
        SD_toggle = False
        SD_list = checkmate.get_book_site('sd').find_book_matches_at_site(book_data)
        TB_toggle = False
        TB_list = checkmate.get_book_site('tb').find_book_matches_at_site(book_data)

        
        context['book_title'] = book_title
        context['book_authors'] = book_authors
        context['book_ISBN'] = book_ISBN
        context['book_JSON'] = book_JSON
        context['KB_toggle'] = KB_toggle
        context['KB_list'] = KB_list
        context['GB_toggle'] = GB_toggle
        context['GB_list'] = GB_list
        context['LC_toggle'] = LC_toggle
        context['LC_list'] = LC_list
        context['SD_toggle'] = SD_toggle
        context['SD_list'] = SD_list
        context['TB_toggle'] = TB_toggle
        context['TB_list'] = TB_list
        return context

@login_required
def book_detail(request):
    book_title = "stuff"
    book_subtitle = "lesser stuff"
    book_series = "even lesser stuff"
    book_volume = "a number"
    book_authors = "a list of stuff"
    book_format = "fancy stuff"
    book_ISBN = "a long number"
    book_url = "complex stuff"
    book_match_percentage = "a fancy number"
    book_description = "dear lord the text"

    context = {
        'book_title': book_title,
        'book_subtitle': book_subtitle,
        'book_series': book_series,
        'book_volume': book_volume,
        'book_authors': book_authors,
        'book_format': book_format,
        'book_ISBN': book_ISBN,
        'book_url': book_url,
        'book_match_percentage': book_match_percentage,
        'book_description': book_description,
    }
    return render(request, 'book_detail.html', context = context)

class CompanyDetail(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing companies, their users, and their search counts"""
    model = Company
    template_name = 'company_detail.html'
    paginate_by = 3

    def get_queryset(self):
        u = self.request.user

        if u.is_staff:
            return Company.objects.order_by('company_name')
        elif u.person is not None:
            return Company.objects.filter(company_name=u.person.company).order_by('company_name')
        else: return None
