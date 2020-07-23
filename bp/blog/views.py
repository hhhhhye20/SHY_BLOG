from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog, Comment, Like
from django.utils import timezone
# Create your views here.
def blog(request):
    blogs = Blog.objects.all()
    return render(request,'blog.html', { 'blogs' : blogs })

# R
def detail(request, blog_id):
    detail = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.all().filter(post = detail)

    #좋아요 기능구현
    user = request.user #현재 로그인된 유저를 받아옴

    if detail.likes.filter(id = user.id):  #detail에 블로그 객체 넣어놨음
        message="좋아요 취소"
    else:
        message="좋아요"   

    return render(request ,'detail.html', { 'detail' : detail, 'comments':comments, 'message':message, } )


def new(request):
    return render(request, 'new.html')

def create(request):
    blog = Blog() # 객체 틀 하나 가져오기
    blog.title = request.GET['title']  # 내용 채우기
    blog.body = request.GET['body'] # 내용 채우기
    blog.pub_date = timezone.datetime.now() # 내용 채우기
    blog.writer = request.user
    blog.save() # 객체 저장하기

    # 새로운 글 url 주소로 이동
    return redirect('/blog/' + str(blog.id))

#삭제
def delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    return redirect('/blog/')
#update

def update(request, blog_id):
    blog = get_object_or_404(Blog, pk =blog_id)

    if request.method == "POST":
        blog.title = request.POST['title']
        blog.body = request.POST['body']
        blog.pub_date = timezone.datetime.now()
        blog.save()
        return redirect('/blog/' +str(blog.id))
    else:
        return render(request,'update.html')


def comment(request, blog_id): #요청이 들어왔을때, blog_id도 받아서!
    if request.method == "POST":
        comment = Comment()
        comment.body = request.POST['body'] #POST방식으로 오는 거는, POST방식으로 받기! detail 의 name='body'
        comment.c_writer = request.user
        comment.pub_date = timezone.datetime.now()
        comment.post = get_object_or_404(Blog, pk=blog_id)
        comment.save()

        return redirect('/blog/'+str(blog_id))

    else:
        return redirect('/blog/'+str(blog_id))


def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    blog_id = comment.post.id

    comment.delete()

    return redirect('/blog/'+str(blog_id))

def post_like(request, blog_id): #아까 url로 연결한 post_like, request통해 blog_id를 받게 되면.. 

    user = request.user
    blog = get_object_or_404(Blog, pk=blog_id)

    if blog.likes.filter(id=user.id):
        blog.likes.remove(user)  #현재 user를 remove해준다.. save, delete함수랑 똑같음, 객체 하나를 삭제한다, 이 user인 순서쌍 하나 객체 하나를 삭제
    else:
        blog.likes.add(user) #현재 user로 된 likes 하나르 ㄹset에 추가해준다, ,,, 

    return redirect('/blog/'+str(blog_id))  #우린 다시 detail페이지로 돌아가야함. 지금 crud의 c, d를 한 함수에 나타냈음. 