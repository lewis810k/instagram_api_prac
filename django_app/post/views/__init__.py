from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from post.models import Post, PostPhoto

User = get_user_model()


def post_list(request):
    context = {
        'post_list': [post.to_dict() for post in Post.objects.all()],
    }
    return JsonResponse(data=context)


@csrf_exempt
def post_create(request):
    if request.method == 'POST':
        try:
            author_id = request.POST['author_id']
            author = User.objects.get(id=author_id)
        except KeyError as e:
            return HttpResponse('key "author_id" is required', status=403)
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
