from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenVerifyView,
        TokenRefreshView
)
from rest_framework_simplejwt.serializers import (
        TokenObtainPairSerializer,
        TokenVerifySerializer,
        TokenRefreshSerializer
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import MyTokenObtainPairSerializer

from drf_spectacular.utils import extend_schema_view
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiResponse
from rest_framework_simplejwt.exceptions import TokenError

#region 自訂 TokenObtainPairView (Login時將會取得 TOKEN)
@extend_schema_view(
    post=extend_schema(
        tags=['權限處理 - JWT'],
        summary='登入取得Token',
        description='輸入帳號密碼後取得Token',
        request={
            'multipart/form-data': MyTokenObtainPairSerializer
        },
        responses={
            200: OpenApiResponse(response=OpenApiTypes.OBJECT, description="成功登入並取得Token"),
            400: OpenApiResponse(description="無效的請求"),
        }
    ),
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response
#endregion

#region (驗證Token)
@extend_schema_view(
    post=extend_schema(
        tags=['權限處理 - JWT'],
        summary='驗證Token是否有效',
        description='將 AccessToken進行驗證是否還有效',
        request={
            'multipart/form-data': TokenVerifySerializer
        },
        responses={
            200: OpenApiResponse(response=OpenApiTypes.OBJECT, description="驗證該Token有效"),
            400: OpenApiResponse(description="無效的請求"),
            401: OpenApiResponse(description="憑證失敗"),
        }
    ),
)
class CustomTokenVerifyView(TokenVerifyView):
    pass
#endregion


#region (刷新Token)
@extend_schema_view(
    post=extend_schema(
        tags=['權限處理 - JWT'],
        summary='刷新Token',
        description='刷新 RefreshToken',
        request={
            'multipart/form-data': TokenRefreshSerializer
        },
        responses={
            200: OpenApiResponse(response=OpenApiTypes.OBJECT, description="成功刷新Token"),
            400: OpenApiResponse(description="無效的請求"),
            401: OpenApiResponse(description="憑證失敗"),
        }
    ),
)
class CustomTokenRefreshView(TokenRefreshView):
    pass
#endregion

# 登出 View
@extend_schema_view(
    post=extend_schema(
        tags=['權限處理 - JWT'],
        summary='登出',
        description='將 RefreshToken進行登出(加入黑名單)',
        request={
            'multipart/form-data': TokenRefreshSerializer
        },
        responses={
            200: OpenApiResponse(response=OpenApiTypes.OBJECT, description="成功刷新Token"),
            400: OpenApiResponse(description="無效的請求"),
            401: OpenApiResponse(description="憑證失敗"),
        }
    ),
)
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "message": "Logged out successfully"
            }, status=200)
        except TokenError:
            # Token 過期或無效時仍返回成功
            return Response({"message": "Logged out successfully"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)