from rest_framework import mixins,generics,status
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import connections, models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from .utils import send_verification_code,send_code_to_number
from .models import UserProfile
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from rest_framework import status


class CreateUserApiView(mixins.CreateModelMixin,generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_or_phone = serializer.validated_data['email_or_phone']
        serializer.save()

        if "@" in email_or_phone:
            send_verification_code(email_or_phone=email_or_phone)
        else:
            send_code_to_number(email_or_phone=int(email_or_phone))

        return Response("Код был отправлен на указанный реквизит", status=status.HTTP_201_CREATED)



class CheckCode():
        @staticmethod
        def check_code(code):
            try:
                user = UserProfile.objects.get(code=code)
                if not user.is_active:
                    user.is_active=True
                    user.save()
                    refresh = RefreshToken.for_user(user=user)
                    return Response({
                        'detail': 'Successfully confirmed your code',
                        'refresh-token': str(refresh),
                        'access': str(refresh.access_token),
                        'refresh_lifetime_days': refresh.lifetime.days,
                        'access_lifetime_days': refresh.access_token.lifetime.days
                    })
                else:
                    return Response({'status': 'The user is already active'}, status=status.HTTP_202_ACCEPTED)
            except UserProfile.DoesNotExist:
                return Response("Пользователь не найден", status=status.HTTP_404_NOT_FOUND)



class ChangePassword:
    
    @staticmethod
    def change_password_on_profile(request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_new_password')

        if not check_password(old_password, user.password):
            return "Старый пароль неверный"
        
        if new_password != confirm_password:
            return "Пароли не совпадают"

        try:
            user.set_password(new_password)
            user.save()
            return "success"
        except Exception as e:
            return str(e)
        
    def change_password_on_reset(self,request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_password = serializer.validated_data.get('password')
        confirm_password = serializer.validated_data.get('confirm_password')

        if new_password != confirm_password:
            return Response("Пароли не совпадают", status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response("Пароль был успешно изменен", status=status.HTTP_200_OK)
    
    
    def send_email_code(email_or_phone):

        if CustomUser.objects.get(email_or_phone=email_or_phone):
            if "@" in email_or_phone:
                send_verification_code(email_or_phone=email_or_phone)
                return Response("Код был отправлен на ваш email")
            elif "996" in email_or_phone:
                send_code_to_number(email_or_phone=int(email_or_phone))
                return Response("Код был отправлен на ваш номер")
            else:
                return Response("The given data invalid")
        else:
            return Response("Вы не зарегистрированы")
        
    

