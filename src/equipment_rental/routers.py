from rest_framework import routers

from rental.api.viewsets import RentalViewSet
from ssr.api.viewsets import SsrViewSet


class Router(routers.DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        root_view = super(Router, self).get_api_root_view(api_urls=api_urls)
        root_view.cls.__doc__ = "N4 Rental API"
        root_view.cls.__name__ = "N4 Rental API"
        return root_view


# router = routers.DefaultRouter()
router = Router()

router.register(r'rental', RentalViewSet)
router.register(r'ssr', SsrViewSet)



# router.get_api_root_view().cls.__name__ = 'N4 Rental API'
# router.get_api_root_view().cls.__doc__ = 'N4 Rental API'