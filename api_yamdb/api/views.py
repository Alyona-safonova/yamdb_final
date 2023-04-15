from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase
from reviews.models import Category, Genre, Review, Title
from users.models import User
from django.core.exceptions import ObjectDoesNotExist

from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly, IsAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenerateTokenSerializer, GenreSerializer,
                          ReviewSerializer, TitleSerializer,
                          UserSignUpSerializer, UserSignUpValidationSerializer,
                          UserSerializerOrReadOnly, UserSerializer)


class Signup(APIView):
    """Отправка письма c кодом подтверждения на почту."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get(
                username__iexact=username, email__iexact=email)
        except ObjectDoesNotExist:
            user_serializer = UserSignUpValidationSerializer(data=request.data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        mail_subject = 'Ваш код подтверждения для получения API токена'
        message = f'Код подтверждения - {confirmation_code}'
        send_mail(mail_subject, message, settings.EMAIL_FROM, (email, ))
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GetToken(TokenViewBase):
    ''' Получение JWT-токена в обмен на username и confirmation code. '''

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GenerateTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(
            user, serializer.validated_data.get("confirmation_code")
        ):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': ['Код не действителен!']},
            status=status.HTTP_400_BAD_REQUEST
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''Получение списка всех категорий.'''

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    search_fields = ['=name']
    filter_backends = [filters.SearchFilter]
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''Получение списка всех жанров.'''

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    search_fields = ['=name']
    filter_backends = [filters.SearchFilter]
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    '''Получение списка всех произведений.'''

    serializer_class = TitleSerializer
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username', )
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        """
        Запрос и возможность редактирования
         информации профиля пользователя.
        """
        user = request.user
        if request.method == 'GET':
            serialized = UserSerializer(user)
            return Response(
                serialized.data,
                status=status.HTTP_200_OK
            )
        if request.method == 'PATCH':
            serializer = UserSerializerOrReadOnly(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
