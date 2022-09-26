from ast import Try
from glob import escape
from django.shortcuts import render,redirect

from .forms import TodoItemForm
from .models import TodoItem
from django.contrib.auth.decorators import login_required
# Create your views here.

def HomeView(request):
    return render(request,'todoapp/home.html')


@login_required(login_url='/accounts/login')
def todo_list_view(request):
    user=request.user
    query=TodoItem.objects.filter(owner=user)
    if request.method=='POST':
        print(request.POST)
        checked_list=request.POST.getlist('checked')
        checked_list=[int(i) for i in checked_list]
        for todo_item in query:
            if todo_item.id in checked_list:
                TodoItem.objects.filter(id=todo_item.id).update(checked=True)
            else:
                TodoItem.objects.filter(id=todo_item.id).update(checked=False)

        return redirect('/list')

    todo_list_len=len(query)

    return render(request,'todoapp/todo_list.html',{'todolist':query,'todo_list_len':todo_list_len})



@login_required(login_url='/accounts/login')
def todo_item_create(request):
    user=request.user
    if request.method=='POST':
        form=TodoItemForm(request.POST)
        if form.is_valid():
           instance=form.save() #instance=form.save(commit=False)
           instance.owner=user
           instance.save()
        #    return redirect('/list')
           return redirect('todoapp:todo_list')

    form=TodoItemForm()

    return render(request,'todoapp/create_todo_item.html',{'form':form})

@login_required(login_url='/accounts/login')
def todo_item_delete(request,id):
    try:
        item=TodoItem.objects.get(id=id)
    except:
        return redirect('todoapp:todo_list')

    if item.owner==request.user:
        item.delete()
        return redirect('todoapp:todo_list')
    else:
        return redirect('todoapp:todo_list')


def test_view(request):
    return render(request,'todoapp/test.html')

