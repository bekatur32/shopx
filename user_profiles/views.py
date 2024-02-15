from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.hashers import check_password
from .utils import send_verification_code
from .services import *
from .permissions import *

from .serializers import *

# апи для регистрации user sellers wholeseller
class UserRegisterView(CreateUserApiView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class SellerRegisterView(CreateUserApiView):
    queryset = Seller.objects.all()
    serializer_class = SellerRegisterSerializer


# class WholeSellerRegisterView(CreateUserApiView):
#     queryset = WholeSeller.objects.all()
#     serializer_class = WholeSellerRegisterSerializer



# апи который проверяет код который был отправлен на указанный email и в ответ передает токен
class UserVerifyRegisterCode(generics.UpdateAPIView):
    serializer_class = VerifyCodeSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        return CheckCode.check_code(code=code)



# если забыл пароль он должен пройти верификацию этот апи отправляет на указанный email код
class ForgetPasswordSendCodeView(generics.UpdateAPIView):
    serializer_class = SendCodeSerializer

    def patch(self, request, *args, **kwargs):
        email = request.data.get("email")
        result = ChangePassword.send_email_code(email=email)

        if result == "success":
            return Response("Код для верификации отправлен на указанный email ", status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


        


# апи для того чтобы сттать продавцом 
class BecomeSellerView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        user.is_seller = True
        user.save()
        return Response("Вы успешно стали продавцом", status=status.HTTP_200_OK)



# если user забыл пароль при входе
class ForgetPasswordView(generics.UpdateAPIView):
    serializer_class = ForgetPasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        
        result = ChangePassword.set_new_password(self=self,request=request)

        if result == "success":
            return Response("Пароль успешно изменен", status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)



# апи менят пароль в профиле 
class UserResetPasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
            result = ChangePassword.change_password_on_profile(request=request)

            if result == "success":
                return Response("Пароль успешно изменен", status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)



class ListProfileApi(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    

class UpdateProfileApi(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

class DetailProfileApi(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'



