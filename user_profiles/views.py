from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions

from .services import *
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



class ForgetPasswordSendCodeView(generics.UpdateAPIView):
    serializer_class = SendCodeSerializer

    def put(self, request, *args, **kwargs):
        email_or_phone = request.data.get("email_or_phone")
        return ChangePassword.send_email_code(email_or_phone=email_or_phone)

        


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
        
        result = ChangePassword.change_password_on_reset(self=self,request=request)

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



class UpdateUserProfileApi(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = 'id'

class DetailUserProfileApi(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'


class SellerUpdateProfileApi(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = SellerProfileSerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = 'id'


class SellerDetailProfileApi(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = SellerProfileSerializer
    lookup_field = 'id'


class MarketView(generics.ListAPIView):
    serializer_class = MarketSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        podcategory_id = self.kwargs.get('podcategory_id')
        
        queryset = Seller.objects.prefetch_related('products__category', 'products__podcategory').all()
        
        if category_id:
            queryset = queryset.filter(products__category_id=category_id)
            if podcategory_id:
                queryset = queryset.filter(products__podcategory_id=podcategory_id)
        
        return queryset

