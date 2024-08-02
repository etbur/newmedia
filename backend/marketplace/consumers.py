
import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Products
from .serializers import ProductSerializer
from django.core.files.base import ContentFile
import base64

class ProductCreateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'create_product':
            product_data = text_data_json.get('product_data', {})
            await self.create_product(product_data)
        else:
            await self.send(text_data=json.dumps({
                'action': 'error',
                'error': 'Invalid action'
            }))

    async def create_product(self, product_data):
        try:
            required_fields = ['name', 'price', 'seller_profile_name']
            if not all(field in product_data for field in required_fields):
                raise ValueError("Missing required product data fields")

            # Decode base64 image data
            image = None
            if 'image' in product_data and product_data['image']:
                image_data = product_data['image'].split(",")[1]
                image = ContentFile(base64.b64decode(image_data), 'product_image.jpg')

            # Decode base64 seller profile picture data
            seller_profile_picture = None
            if 'seller_profile_picture' in product_data and product_data['seller_profile_picture']:
                picture_data = product_data['seller_profile_picture'].split(",")[1]
                seller_profile_picture = ContentFile(base64.b64decode(picture_data), 'seller_profile_picture.jpg')

            # Convert category to lowercase to match choices
            category = product_data.get('category', '').lower()

            # Prepare product data for serialization
            serializer = ProductSerializer(data={
                'name': product_data['name'],
                'price': product_data['price'],
                'description': product_data.get('description', ''),
                'image': image,
                'seller_profile_name': product_data['seller_profile_name'],
                'seller_profile_picture': seller_profile_picture,
                'category': category
            })

            if serializer.is_valid():
                # Save the product
                product = await database_sync_to_async(serializer.save)()
                
                # Respond with success and product ID
                await self.send(text_data=json.dumps({
                    'action': 'create_product_success',
                    'product_id': product.id
                }))
            else:
                # Raise validation error with serializer errors
                raise ValueError(serializer.errors)

        except Exception as e:
            # Send error response with exception message
            await self.send(text_data=json.dumps({
                'action': 'create_product_error',
                'error': str(e)
            }))

class ProductCategory(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'fetch_categories':
            await self.fetch_categories()
        else:
            await self.send(text_data=json.dumps({
                'action': 'error',
                'error': 'Invalid action'
            }))

    async def fetch_categories(self):
        try:
            categories = Products.CATEGORY_CHOICES
            category_list = [
                {'id': index, 'name': name}
                for index, (value, name) in enumerate(categories)
            ]

            await self.send(text_data=json.dumps({
                'action': 'fetch_categories_success',
                'categories': category_list
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'action': 'fetch_categories_error',
                'error': str(e)
            }))


class ProductListConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'fetch_all_products':
            self.fetch_all_products()
        else:
            self.send(text_data=json.dumps({
                'action': 'error',
                'error': 'Invalid action'
            }))

    def fetch_all_products(self):
        try:
            products = Products.objects.all()
            serializer = ProductSerializer(products, many=True)
            product_list = serializer.data

            self.send(text_data=json.dumps({
                'action': 'fetch_all_products_success',
                'products': product_list
            }))
        except Exception as e:
            self.send(text_data=json.dumps({
                'action': 'fetch_all_products_error',
                'error': str(e)
            }))




class ProductUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.product_id = self.scope['url_route']['kwargs'].get('product_id')
        if not self.product_id:
            await self.close()
            return
        
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'update_product_view':
            await self.update_product_view()
        else:
            await self.send(text_data=json.dumps({
                'action': 'error',
                'error': 'Invalid action'
            }))

    async def update_product_view(self):
        try:
            product = await Products.objects.aget(id=self.product_id)
            product.num_views += 1
            await database_sync_to_async(product.save)()

            await self.send(text_data=json.dumps({
                'action': 'update_product_view_success',
                'num_views': product.num_views
            }))
        except Products.DoesNotExist:
            await self.send(text_data=json.dumps({
                'action': 'update_product_view_error',
                'error': 'Product does not exist'
            }))




class ProductDeleteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.product_id = self.scope['url_route']['kwargs'].get('product_id')
        if not self.product_id:
            await self.close()
            return
        
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'delete_product':
            await self.delete_product()
        else:
            await self.send(text_data=json.dumps({
                'action': 'error',
                'error': 'Invalid action'
            }))

    async def delete_product(self):
        try:
            product = await Products.objects.aget(id=self.product_id)
            await database_sync_to_async(product.delete)()

            await self.send(text_data=json.dumps({
                'action': 'delete_product_success',
                'product_id': self.product_id
            }))
        except Products.DoesNotExist:
            await self.send(text_data=json.dumps({
                'action': 'delete_product_error',
                'error': 'Product does not exist'
            }))

