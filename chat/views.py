from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User,auth
# Create your views here.
 

@login_required
def finding_all_chatrooms(request):
    username=request.user.username
    chat_rooms = ChatRoom.objects.filter(name=username)
    chat_room_codes = chat_rooms.values('pk','code')
    chat_room_codes_list = list(chat_room_codes)
    print(chat_room_codes_list)
    # Store chat room codes in session to use in the redirected view
    request.session['chat_room_codes'] = chat_room_codes_list


@login_required
def create_chat_room(request):
        
        user = request.user.username
        print(user)
        chat_room = ChatRoom.objects.create(name=user)
        chat_room.save()
        finding_all_chatrooms(request)
        return HttpResponseRedirect(f'/{request.user.username}/login')

@login_required
def room_delete(request,room_name):
    chat_room = ChatRoom.objects.get(name=request.user.username,code=room_name)
    chat_room.delete()
    finding_all_chatrooms(request)
    return redirect(f'/{request.user.username}/login')

def addmember(request):
    if request.method == 'POST':
        print("Dsfvjdknvfnjvfjkdngjkfdnjkdngjkdnjkdnfkjbnnjkbnfjkjnbfjkdnbjkfnjknjknknkjdsfsf")
        user = request.user.username
        code=request.POST['code']
        print(user)
        try:
            obj = ChatRoom.objects.get(code=code, name=user)
            print("yes")
            return HttpResponseRedirect(f'/chat/{code}')
        except ChatRoom.DoesNotExist:
            chat_room = ChatRoom.objects.create(name=user, code=code)
            chat_room.save()
            finding_all_chatrooms(request)
            return redirect(f'/{request.user.username}/login')


@login_required
def chat_room_detail(request, room_code):
    chat_room = ChatRoom.objects.get(code=room_code)
    return render(request, 'chat_room.html', {'chat_room': chat_room})


@login_required
def all_chatroom(request):
    username=request.user.username
    
    obj=ChatRoom.objects.filter(name=username)
    # return HttpResponseRedirect(f'/{username}/login',{'list_obj':obj})