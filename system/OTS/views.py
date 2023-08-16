from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from OTS.models import *
import random
# Create your views here.

def welcome(request):
    template = loader.get_template('welcome.html')
    return HttpResponse(template.render())

def candidateRegistrationForm(request):
    res = render(request, 'registration_form.html')
    return res

def candidateRegistration(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        
        if (len(Candidate.objects.filter(username = username))):
            userStatus = 1
        else:
            candidate = Candidate()
            candidate.username = request.POST['username']
            candidate.password = request.POST['password']
            candidate.name = request.POST['name']
            candidate.save()
            userStatus = 2
            
    else: 
        userStatus = 3
        
    context = {'userStatus': userStatus}
    res = render(request, 'registration.html', context)
    return res

def loginView(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        candidate = Candidate.objects.filter(username = username, password = password)
        if len(candidate) == 0:
            loginError = "Invalid Username or Password"
            res = render(request, 'login.html', {'loginError': loginError})
        else:
            # login Success
            request.session['username'] = candidate[0].username
            request.session['name'] = candidate[0].name
            res = render(request, 'home.html')
    else:  
        res = render(request, 'login.html')
    
    return res

def candidateHome(request):
    if 'name' not in request.session.keys():
        res = render("login")
    else:
        res = render(request, 'home.html')
    return res

def testPaper(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect("login")
    n = int(request.GET['n'])
    question_pool = list(Question.objects.all())
    random.shuffle(question_pool) 
    question_list = question_pool[:n]
    context = {'question': question_list}
    res = render(request,'test_paper.html', context)
    return res
    
def calculateTestResult(request):
    if 'name' not in request.session.keys():
        res = render("login")  
    total_attempt = 0
    total_wrong = 0
    total_right = 0
    que_id_list = []
    for k in request.POST:
        if k.startswith('que_no'):
            que_id_list.append(int(request.POST[k]))     
    for n in que_id_list:
        question = Question.objects.get(que_id = n)
        try: 
            if question.ans == request.POST['q' + str(n)]:
                total_right += 1
            else:
                total_wrong += 1
        except:
            pass
    total_attempt += 1
    points = (total_right - total_wrong)/len(que_id_list)*10 
    # Total result in Result Table
    result = Result()
    result.username = Candidate.objects.get(username = request.session['username'])
    result.attempt = total_attempt
    result.right = total_right
    result.wrong = total_wrong
    result.points = points
    result.save()
    # update candidate table
    candidate = Candidate.objects.get(username = request.session['username'])
    candidate.test_attempt += 1
    candidate.points = (candidate.points + points)
    candidate.save()
    return HttpResponseRedirect('result')

def testResultHistory(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect("login")
    candidate = Candidate.objects.filter(username=request.session['username'])
    results= Result.objects.filter(username_id=candidate[0].username)
    context = {'candidate': candidate[0], 'result': results}
    res = render(request,'candidate_history.html',context)
    return res

def showTestResult(request):
    if 'name' not in request.session.keys():
       res = render("login")
    result = Result.objects.filter(result_id=Result.objects.latest('result_id').result_id, username_id = request.session['username'])
    context = {'result': result}
    res = render(request, 'show_result.html', context)
    return res

def logout(request):
    if 'name' in request.session.keys():
        del request.session['username']
        del request.session['name']
    return HttpResponseRedirect("login")