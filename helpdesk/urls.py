from django.urls import include, path
from rest_framework import routers
from .views import RequisitionsView, RequisitionsListView, RequisitionsCreateView, RequisitionsUpdateView, \
    RegistrationUserView, MyLoginView, MyUserLogoutView, CommentView, AcceptRequisitionsView, CancelRequisitionsView, \
    RecoveryRequisitionsView, AdminRecoveryRequisitionsView, AdminAcceptRecoveryRequisitionsView, \
    AdminCancelRecoveryRequisitionsView
from helpdesk.models import Requisitions, Comment
from helpdesk.api.resources import RegistrationViewSet, RequisitionsViewSet, CommentViewSet, CustomAuthToken

router = routers.SimpleRouter()
router.register(r'registrations', RegistrationViewSet)
router.register(r'requisitions', RequisitionsViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', RequisitionsView.as_view(), name='index'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('registration/', RegistrationUserView.as_view(), name='registration'),
    path('logout/', MyUserLogoutView.as_view(), name='logout'),
    path('create_requisitions/', RequisitionsCreateView.as_view(), name='create_requisitions'),
    path('requisitions_update/<int:pk>/', RequisitionsUpdateView.as_view(), name='requisitions_update'),
    path('requisitions_list/', RequisitionsListView.as_view(), name='requisitions_list'),
    path('comments/<int:pk>/', CommentView.as_view(), name='comments'),
    path('requisitions_accept/<int:pk>/', AcceptRequisitionsView.as_view(), name='requisitions_accept'),
    path('requisitions_cancel/<int:pk>/', CancelRequisitionsView.as_view(), name='requisitions_cancel'),
    path('requisitions_recovery/<int:pk>/', RecoveryRequisitionsView.as_view(), name='requisitions_recovery'),
    path('admin_requisitions_recovery/', AdminRecoveryRequisitionsView.as_view(), name='admin_requisitions_recovery'),
    path('admin_requisitions_accept_recovery/<int:pk>/', AdminAcceptRecoveryRequisitionsView.as_view(),
         name='admin_requisitions_accept_recovery'),
    path('admin_requisitions_cancel_recovery/<int:pk>/', AdminCancelRecoveryRequisitionsView.as_view(),
         name='admin_requisitions_cancel_recovery'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', CustomAuthToken.as_view())
]
