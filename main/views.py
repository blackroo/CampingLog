from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .forms import CommentForm, AnswerForm
from .models import Comment,camping, Answer
from django.core.paginator import Paginator
# Create your views here.
def index(request):
  
    return render(request, 'main/index.html')

def detail(request,id, comment_id):
    """
    후기 내용 출력
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    data = Comment.objects.get(id = comment_id)
    number = data.camping_id.id
    print(number)
    context = {
        'comment': comment,
        'number' : number,
        'area'  : id,
        }

    return render(request, 'main/comment_detail.html', context)


@login_required(login_url='common:login')
def comment_create(request,id,num):
    """
    후기등록
    """
    camping_name = camping.objects.get(id=num)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.camping_id = camping_name
            comment.save()
            return redirect(f'main:camping_detail',id,num)
    else:
        form = CommentForm()
    
    context = {'form': form}
    return render(request, 'main/comment.html', context)


@login_required(login_url='common:login')
def comment_modify(request,id, comment_id):
    """
    후기수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    num=comment.camping_id.id
    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('main:detail',id,comment_id)
    if request.method == "POST":
# 질문 수정을 위해 값 덮어쓰기
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now() # 수정일시 저장
            comment.save()
            return redirect('main:detail',id, comment_id)
    else:
        # 질문 수정 화면에 기존 제목, 내용 반영
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'main/comment.html', context)

@login_required(login_url='common:login')
def comment_delete(request,id, comment_id):
    """
    후기삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('main:detail',id, comment_id=comment.id)

    num=comment.camping_id.id

    comment.delete()
    return redirect(f'main:camping_detail',id,num)   

@login_required(login_url='common:login')
def answer_create(request,id, comment_id):
    """
    후기에 답변등록하기
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.author = request.user
        answer.create_date = timezone.now()
        answer.comment = comment
        answer.save()
        return redirect('main:detail',id, comment.id)
    else:
        form = AnswerForm()
    context = {'comment' : comment, 'form' : form}
    return render(request, 'main/comment_detail.html', id, context)

@login_required(login_url='common:login')
def answer_modify(request,id, answer_id):
    """
    질문 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('main:detail',id, answer.comment.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('main:detail',id, answer.comment.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'main/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request,id, answer_id):
    """
    질문 답변삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('main:detail',id, answer.comment.id)

@login_required(login_url='common:login')
def vote_comment(request,id, comment_id):
    """
    후기추천등록
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        comment.voter.add(request.user)
    return redirect('main:detail',id, comment.id)

@login_required(login_url='common:login')
def vote_answer(request,id, answer_id):
    """
    후기 답글추천등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('main:detail',id,answer.comment.id)
        
def camping_detail(request,id,num):

    page = request.GET.get('page','1')
    comment_list = Comment.objects.filter(camping_id=num).order_by("-create_date")
    data_list=[]
    x=0
    for i in range(len(comment_list),0,-1):
        data_list.append({'num':i,'comment_name':comment_list[x]})
        x=x+1



    paginator = Paginator(data_list, 10)
    page_obj = paginator.get_page(page)


    print(page_obj)



    camping_name = camping.objects.get(id=num)

    context = {
        'comment_list' : page_obj,
        'camping' : camping_name,
        'area': id,
        }
  
    return render(request, 'main/camping_detail.html', context)


def db(request):
    return render(request, 'main/receive_data.html')


def receive_data(request):
    import requests
    from ast import literal_eval


    pagenum=0   #0부터 시작
    page_data = 100 #페이지당 데이터개수, 약 2220개 데이터 있는걸로 확인됨.
    total_data = 2230
    total_page = total_data//page_data


    url = 'http://api.data.go.kr/openapi/tn_pubr_public_campg_api'
    key_decoding = '/CTZDSd8CqhcX7WCXl6dU6eRaw3qVVEvNVkcGsWlgEeuKSAK2Ty94Qg4Tkwebxm1C4emTuSX+jVv5S3S1NW9rw=='
    
    
    try:
        camping_list = camping.objects.all()
        camping_list.delete()
        pass
        
    except:
        pass
    
    camping_list = camping()
    for i in range(total_page):
        print(f"## 데이터 받는중 {i}/{total_page} Page##")
        params ={'serviceKey' : key_decoding, 'pageNo' : i, 'numOfRows' : page_data, 'type' : 'json'}

        #html 통신으로 값을 받음
        response = requests.get(url, params=params)

        #txt형식(str)으로 값을 저장함
        data = response.text

        # txt형식에서 필요 데이터 추출
        start = data.find('[')
        end = data.find('],')
        item = data[start:end+1]

        # 각 데이터를 사전으로 묶고 리스트로 저장

        dic_item = literal_eval(item)

        for a in range(page_data):
            try:
                camping_list = camping(
                    # id = ((i)*10)+a,
                    name = dic_item[a]["campgNm"],
                    type = dic_item[a]["campgSe"],
                    latitude = dic_item[a]["latitude"],
                    longitude = dic_item[a]["longitude"],
                    location = dic_item[a]["rdnmadr"],
                    location2 = dic_item[a]["lnmadr"],
                    phone = dic_item[a]["officePhoneNumber"],
                    people = dic_item[a]["dayAcmdCo"],
                    facilities = dic_item[a]["cvntl"],
                    safefacilities = dic_item[a]["safentl"],
                    otherfacilities = dic_item[a]["etcty"],
                    time = dic_item[a]["useTime"],
                    cost = dic_item[a]["useCharge"],
                    managerphone = dic_item[a]["phoneNumber"],
                    manager = dic_item[a]["institutionNm"],
                    managelocation = dic_item[a]["institutionNm"],
                )
                camping_list.save()
            except:
                pass
    camping_list.save()
    return redirect('main:index')



def location(request):
    return render(request, 'location/location.html')


def location_detail(request, id):

    try:
        data = camping.objects.filter(location__contains=id).values()
        camping_list = data.order_by("location")
    except:
        camping_list = None
    
    page = request.GET.get('page','1')
    paginator = Paginator(camping_list, 20)
    page_obj = paginator.get_page(page)

    context = {
        'area' : id,
        'camping_list' : page_obj
    }

    return render(request, 'location/location_detail.html',context)


def search(request):
    # data = camping.objects.filter(location__contains=id).values()
    # camping_list = data.order_by("location")
    if request.method == "POST":
        search= request.POST.get('search', '')
        radio=request.POST.get('radioTxt','')

        if search=="":
            return render(request, 'location/location.html')

        context = {
            'search' : search,
            'radio' : radio,
        }

        return render(request, 'location/search.html',context)
    
    else:
        return render(request, 'location/location.html')


def search_val(request, radio, search):

    if radio == "name":
        try:
            data = camping.objects.filter(name__contains=search).values()
            camping_list = data.order_by("location")
        except:
            camping_list = None

    if radio == "address":
        try:
            data = camping.objects.filter(location__contains=search).values()
            camping_list = data.order_by("location")
        except:
            camping_list = None

    if radio == "facilities":
        try:
            data = camping.objects.filter(facilities__contains=search).values()
            camping_list = data.order_by("-location")
        except:
            camping_list = None
    
    page = request.GET.get('page','1')
    paginator = Paginator(camping_list, 20)
    page_obj = paginator.get_page(page)

    context = {
        'area' : search,
        'camping_list' : page_obj,
        'type': radio,
    }

    return render(request, 'location/location_detail.html',context)