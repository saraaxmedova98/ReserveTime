from rest_framework.routers import DefaultRouter
from core.api.views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'tables', TableViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'menucategories', MenuCategoryViewSet)
router.register(r'photos', PhotoViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'savedrestaurants', SavedRestaurantViewSet)
router.register(r'portions', PortionViewSet)
router.register(r'times', TimeViewSet)



