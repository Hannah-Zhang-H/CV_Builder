from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io


# Create your views here.

def accept(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        summary = request.POST.get('summary', '')
        degree = request.POST.get('degree', '')
        school = request.POST.get('school', '')
        university = request.POST.get('university', '')
        previous_work = request.POST.get('previous_work', '')
        skills = request.POST.get('skills', '')

        # Created an object of class Profile, the object name is profile
        profile = Profile(name=name, email=email, phone=phone, summary=summary, degree=degree,
                          school=school, university=university, previous_work=previous_work, skills=skills)
        # Save the object into database
        profile.save()

    return render(request, 'pdf/accept.html')


def cv(request, id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template('pdf/cv.html')  # now this template is empty, not any dynamic user data exists
    html = template.render({'user_profile': user_profile})
    # Now we can pass this html to our pdf library to convert to a downloadable pdf
    # before do the following, let's define the output pdf options
    # 'page-size': 'Letter',是指定生成的 PDF 文件的页面大小为美国的标准信纸大小，即 8.5 x 11 英寸。 Letter 大小是一种常见的页面大小标准，适用于许多文档和打印需求。
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
    }
    pdf = pdfkit.from_string(html, False, options)  # takes a html as a parameter and convert it into a pdf

    response = HttpResponse(pdf, content_type='application/pdf')
    # 这行代码设置了 HTTP 响应头部的 Content-Disposition 属性，告诉浏览器如何处理响应内容。
    # 具体来说，attachment 表示告诉浏览器将响应内容作为附件下载，而 filename="{user_profile.name}.pdf" 则指定了下载的文件名为用户的名称加上 .pdf 后缀。
    # 因此，浏览器在接收到这个响应后，会将内容保存为一个名为用户名称的 PDF 文件。
    # response['Content-Disposition'] = 'attachment'
    # filename="cv.pdf"
    response['Content-Disposition'] = f'attachment; filename="{user_profile.name} CV.pdf"'
    return response

    # return render(request, 'pdf/cv.html', {'user_profile': user_profile})


def userlist(request):
    profiles = Profile.objects.all()
    return render(request, 'pdf/userlist.html', {'profiles': profiles})