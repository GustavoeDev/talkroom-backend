from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.timezone import now

from rest_framework_simplejwt.tokens import RefreshToken

from .auth import Authentication
from .serializers import UserSerializer
from .models import User

from core.utils.exceptions import ValidationError

import uuid

class UserSignInView(APIView, Authentication):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        signin = self.signin(email, password)

        if not signin:
            raise AuthenticationFailed
        
        user = UserSerializer(signin).data
        access_token = RefreshToken.for_user(signin).access_token

        return Response({
            'user': user,
            'access_token': str(access_token)
        })

class UserSignUpView(APIView, Authentication):
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get('name', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        if not name or not email or not password:
            raise AuthenticationFailed

        signup = self.signup(name, email, password)

        if not signup:
            raise AuthenticationFailed
        
        user = UserSerializer(signup).data
        access_token = RefreshToken.for_user(signup).access_token

        return Response({
            'user': user,
            'access_token': str(access_token)
        })
    
class UserView(APIView):
    def get(self, request):
        User.objects.filter(id=request.user.id).update(last_login=now())

        user = UserSerializer(request.user).data

        return Response({
            'user': user
        })
    
    def put(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        avatar = request.FILES.get('avatar')
        
        data = {
            'name': name,
            'email': email,
            'avatar': request.user.avatar  # Value default
        }
        
        # Update avatar
        if avatar:
            content_type = avatar.content_type
            extension = avatar.name.split('.')[-1]
            
            # Avatar validation
            if content_type not in ['image/jpeg', 'image/png']:
                raise ValidationError('Suportamos apenas imagens JPEG e PNG')
            
            # Configure storage
            storage = FileSystemStorage(
                settings.MEDIA_ROOT / 'avatars',
                settings.MEDIA_URL + 'avatars'
            )
            
            # Save avatar
            filename = f'{uuid.uuid4()}.{extension}'
            file = storage.save(filename, avatar)
            avatar_url = storage.url(file)
            data['avatar'] = avatar_url
        
        # Validar e salvar dados
        serializer = UserSerializer(request.user, data=data)

        if not serializer.is_valid():
            # Delete old avatar if was changed
            if avatar and 'avatar_url' in locals():
                storage.delete(filename)
            
            first_error = list(serializer.errors.values())[0][0]
            raise ValidationError(first_error)
        
        # Deletar avatar antigo se um novo foi enviado
        old_avatar = request.user.avatar
        if avatar and old_avatar and old_avatar != "/media/avatars/avatar-default.png":
            try:
                old_filename = old_avatar.split('/')[-1]
                storage = FileSystemStorage(
                    settings.MEDIA_ROOT / 'avatars',
                    settings.MEDIA_URL + 'avatars'
                )
                storage.delete(old_filename)
            except Exception as e:
                # Tratar ou registrar o erro, mas não impedir a atualização
                pass
        
        # Update password if provided
        if password:
            request.user.set_password(password)
        
        # Save user update
        serializer.save()
        
        return Response({
            'user': serializer.data
        })

