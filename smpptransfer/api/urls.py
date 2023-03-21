from rest_framework import routers, serializers, viewsets

from smpptransfer.api.views import UnreadInboundMessagesView

router = routers.DefaultRouter()
router.register(r'send-tnm', UnreadInboundMessagesView.as_view(), basename="smpp")
urlpatterns = router.urls
