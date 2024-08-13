
import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Products,Rating
from django.db.models import Avg
from .serializers import ProductSerializer
from django.core.files.base import ContentFile
import base64
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ProductCreateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
           
    async def disconnect(self, close_code):
        print(f"WebSocket closed: {close_code}")  
    
    async def receive(self, text_data):
        print(f"Received data: {text_data}")  
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
        elif action == 'filter_by_category':
            category = text_data_json.get('category')
            self.filter_by_category(category)
        elif action == 'filter_by_price':
            min_price = text_data_json.get('min_price')
            max_price = text_data_json.get('max_price')
            self.filter_by_price(min_price, max_price)
        elif action == 'filter_by_location':
            location = text_data_json.get('location')
            self.filter_by_location(location)
        elif action == 'filter_by_rating':
            min_rating = text_data_json.get('min_rating')
            max_rating = text_data_json.get('max_rating')
            self.filter_by_rating(min_rating, max_rating)
        else:
            self.send(text_data=json.dumps({
                'action': 'error',
                'error': 'Invalid action'
            }))

    def fetch_all_products(self):
        try:
            products = Products.objects.all().order_by('-created_at')
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
            logger.error("Error fetching all products: %s", str(e))

    def filter_by_category(self, category):
        try:
            valid_categories = [c[0] for c in Products.CATEGORY_CHOICES]
            if category not in valid_categories:
                self.send(text_data=json.dumps({
                    'action': 'filter_by_category_error',
                    'error': 'Invalid category'
                }))
                return

            products = Products.objects.filter(category=category)
            serializer = ProductSerializer(products, many=True)
            product_list = serializer.data
            self.send(text_data=json.dumps({
                'action': 'filter_by_category_success',
                'products': product_list
            }))
        except Exception as e:
            self.send(text_data=json.dumps({
                'action': 'filter_by_category_error',
                'error': str(e)
            }))
            logger.error("Error filtering products by category %s: %s", category, str(e))

    def filter_by_price(self, min_price, max_price):
        try:
            products = Products.objects.filter(price__gte=min_price, price__lte=max_price)
            serializer = ProductSerializer(products, many=True)
            product_list = serializer.data
            self.send(text_data=json.dumps({
                'action': 'filter_by_price_success',
                'products': product_list
            }))
        except Exception as e:
            self.send(text_data=json.dumps({
                'action': 'filter_by_price_error',
                'error': str(e)
            }))
            logger.error("Error filtering products by price range %s-%s: %s", min_price, max_price, str(e))

    def filter_by_location(self, location):
        try:
            # Assuming location is a field in Products model
            products = Products.objects.filter(location=location)
            serializer = ProductSerializer(products, many=True)
            product_list = serializer.data
            self.send(text_data=json.dumps({
                'action': 'filter_by_location_success',
                'products': product_list
            }))
        except Exception as e:
            self.send(text_data=json.dumps({
                'action': 'filter_by_location_error',
                'error': str(e)
            }))
            logger.error("Error filtering products by location %s: %s", location, str(e))

    def filter_by_rating(self, min_rating, max_rating):
        try:
            products = Products.objects.filter(rating__gte=min_rating, rating__lte=max_rating)
            serializer = ProductSerializer(products, many=True)
            product_list = serializer.data
            self.send(text_data=json.dumps({
                'action': 'filter_by_rating_success',
                'products': product_list
            }))
        except Exception as e:
            self.send(text_data=json.dumps({
                'action': 'filter_by_rating_error',
                'error': str(e)
            }))
            logger.error("Error filtering products by rating range %s-%s: %s", min_rating, max_rating, str(e))



class ProductUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.product_id = self.scope['url_route']['kwargs'].get('product_id')
        self.room_group_name = f'product_{self.product_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'update_product_view':
            await self.update_product_view()

        elif action == 'update_product_rating':
            rating = data.get('rating')
            await self.update_product_rating(rating)

    async def update_product_view(self):
        # Update the view count in the database
        product = Products.objects.get(id=self.product_id)
        product.views += 1
        product.save()

        await self.send(text_data=json.dumps({
            'action': 'update_product_view_success',
            'num_views': product.views
        }))

    async def update_product_rating(self, rating):
        # Update the rating in the database
        product = Products.objects.get(id=self.product_id)
        product.rating = rating
        product.save()

        await self.send(text_data=json.dumps({
            'action': 'update_product_rating_success',
            'rating': product.rating
        }))


class ProductCategory(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'fetch_categories':
            self.fetch_categories()
        else:
            self.send(text_data=json.dumps({
                'action': 'error',
                'error': 'Invalid action'
            }))

    def fetch_categories(self):
        try:
            categories = Products.CATEGORY_CHOICES
            category_list = [
                {'id': index, 'name': name}
                for index, (value, name) in enumerate(categories)
            ]
            self.send(text_data=json.dumps({
                'action': 'fetch_categories_success',
                'categories': category_list
            }))
        except Exception as e:
            self.send(text_data=json.dumps({
                'action': 'fetch_categories_error',
                'error': str(e)
            }))
            logger.error("Error fetching categories: %s", str(e))



class ProductViewAndRatingUpdateConsumer(AsyncWebsocketConsumer):
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
        elif action == 'update_product_rating':
            rating = text_data_json.get('rating')
            if rating is not None:
                await self.update_product_rating(float(rating))
            else:
                await self.send(text_data=json.dumps({
                    'action': 'error',
                    'error': 'Rating value is missing'
                }))
        else:
            await self.send(text_data=json.dumps({
                'action': 'error',
                'error': 'Invalid action'
            }))

    async def update_product_view(self):
        try:
            product = await database_sync_to_async(Products.objects.get)(id=self.product_id)
            product.views += 1
            await database_sync_to_async(product.save)()

            await self.send(text_data=json.dumps({
                'action': 'update_product_view_success',
                'views': product.views
            }))
        except Products.DoesNotExist:
            await self.send(text_data=json.dumps({
                'action': 'update_product_view_error',
                'error': 'Product does not exist'
            }))

    async def update_product_rating(self, rating):
        user = self.scope['user']
        if not user.is_authenticated:
            await self.send(text_data=json.dumps({
                'action': 'update_product_rating_error',
                'error': 'User is not authenticated'
            }))
            return

        try:
            product = await database_sync_to_async(Products.objects.get)(id=self.product_id)
            existing_rating, created = await database_sync_to_async(Rating.objects.get_or_create)(
                user=user,
                product=product,
                defaults={'rating': rating}
            )

            if not created:
                existing_rating.rating = rating
                await database_sync_to_async(existing_rating.save)()

            avg_rating = await database_sync_to_async(Rating.objects.filter(product=product).aggregate)(Avg('rating'))
            product.average_rating = avg_rating['rating__avg']
            await database_sync_to_async(product.save)()

            await self.send(text_data=json.dumps({
                'action': 'update_product_rating_success',
                'rating': float(product.average_rating)  # Convert Decimal to float
            }))
        except Products.DoesNotExist:
            await self.send(text_data=json.dumps({
                'action': 'update_product_rating_error',
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
