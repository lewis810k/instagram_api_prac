from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from post.models import Post, PostPhoto

User = get_user_model()


def post_list(request):
    post_list = Post.objects.select_related('author')
    post_dict_list = []
    for post in post_list:
        cur_post_photo_list = post.postphoto_set.all()
        cur_post_photo_dict_list = []
        for post_photo in cur_post_photo_list:
            cur_post_photo_dict = {
                'pk': post_photo.pk,
                'photo': post_photo.photo.url,
            }
            cur_post_photo_dict_list.append(cur_post_photo_dict)
        cur_post_dict = {
            'pk': post.pk,
            'created_date': post.created_date,
            'photo_list': cur_post_photo_dict_list,
            'author': {
                'pk': post.author.pk,
                'username': post.author.username,
            },
        }
        post_dict_list.append(cur_post_dict)
    context = {
        'post_list': post_dict_list,
    }
    return JsonResponse(data=context)


@csrf_exempt
def post_create(request):
    if request.method == 'POST':
        try:
            author_id = request.POST['author_id']
            author = User.objects.get(id=author_id)
        except KeyError as e:
            return HttpResponse('key "author_id" is required')
        except User.DoesNotExist:
            return HttpResponse('author_id {} does not exist'.format(
                request.POST['author_id']
            ))

        post = Post.objects.create(author=author)
        return HttpResponse('{}'.format(post.pk))
    else:
        return HttpResponse('Post create view')


@csrf_exempt
def post_photo_add(request):
    if request.method == 'POST':
        try:
            post_id = request.POST['post_id']
            photo = request.FILES['photo']
            post = Post.objects.get(id=post_id)
        except KeyError:
            return HttpResponse('post_id and photo are required fields')
        except Post.DoesNotExist:
            return HttpResponse('post_id {} is not exist'.format(
                request.POST['post_id']
            ))
        PostPhoto.objects.create(
            post=post,
            photo=photo
        )
        return HttpResponse('Post: {}, PhotoList: {}'.format(
            post.id,
            [photo.id for photo in post.postphoto_set.all()]
        ))
    else:
        return HttpResponse('Post photo add view')
