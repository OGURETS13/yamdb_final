from random import randint

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import User, Category, Genre, Review, Title
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    AdminModeratorAuthorPermission
)
from .serializers import (
    AuthSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadDelSerializer,
    TitleCreateUpdateSerializer,
    TokenSerializer,
    UserSerializer,
)
from .filters import TitleFilter


class SendConfirmationCodeView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)

        if serializer.is_valid():
            confirmation_code = str(randint(100000, 999999))
            email = serializer.initial_data.get('email')
            send_mail(
                'YAMDB Confirmation code',
                (str(serializer.initial_data['username']
                 + '\n'
                 + str(confirmation_code))),
                'from@example.com',
                [email],
                fail_silently=False,
            )
            serializer.save(confirmation_code=confirmation_code)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.data.get('username')
            user = get_object_or_404(User, username=username)
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'destroy'):
            return TitleReadDelSerializer
        return TitleCreateUpdateSerializer


class MeViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        me = get_object_or_404(queryset, pk=request.user.pk)
        serializer = UserSerializer(me)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = User.objects.all()
        me = get_object_or_404(queryset, pk=request.user.pk)
        serializer = UserSerializer(me, data=request.data, partial=True)
        if serializer.is_valid():
            if 'role' in request.data:
                if me.role == 'admin' or me.is_superuser:
                    serializer.validated_data['role'] \
                        = request.data.get('role')
                else:
                    serializer.validated_data['role'] = me.role
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
