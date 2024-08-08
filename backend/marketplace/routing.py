
from django.urls import path
from .consumers import ProductCreateConsumer, ProductListConsumer, ProductUpdateConsumer, ProductDeleteConsumer,ProductCategory,ProductUpdateConsumer

websocket_urlpatterns = [
    path('ws/products/create/', ProductCreateConsumer.as_asgi()),
    path('ws/products/fetch/', ProductListConsumer.as_asgi()),
    path('ws/products/update/', ProductUpdateConsumer.as_asgi()),
    path('ws/products/delete/', ProductDeleteConsumer.as_asgi()),
    path('ws/products/categories/', ProductCategory.as_asgi()),
    path('ws/products/categories/', ProductCategory.as_asgi()),
    path('ws/products/update/<int:product_id>/', ProductUpdateConsumer.as_asgi()),
    
]
