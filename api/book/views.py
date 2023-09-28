from django.shortcuts import get_object_or_404
from apps.product.models import *
from .serializers import AuthorSerializer, BookCreateSerializer, BookImageSerializer, BookListSerializer, BookSerializer, PrintedSerializer
from rest_framework import mixins, generics, status, viewsets, response
from rest_framework.decorators import action

class BookModelViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'



    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        elif self.action == 'retrieve':
            return BookSerializer
        elif self.action == 'create':
           return BookCreateSerializer
        return BookSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data
        sz_ = BookCreateSerializer(data=data)
        sz_.is_valid(raise_exception=True)
        sz_.save()
        images = {
           
        }
        files = request.FILES
        for file in files:
            images[file] = []
            for i in files.getlist(file):
                sz = BookImageSerializer(data={'image': i,'wrapper':str(file), 'product': sz_.data['id'], 'price':data[f'price_{str(file)}']})
                sz.is_valid(raise_exception=True)
                sz.save()
                images[file].append(sz.data)

        return response.Response({'data':sz_.data,'images':images}, status=status.HTTP_201_CREATED)

    
    @action(methods=['delete'], detail=False)
    def remove_image(self,request):
        wrapper = request.GET.get('wrapper')
        product = request.GET.get('product')
        product = get_object_or_404(Product, id=product)
        images = ProductImage.objects.filter(wrapper=wrapper, product=product)
        images.delete()
        return response.Response({'data':'removed'},status=status.HTTP_204_NO_CONTENT)


    
class ProductImageModelViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = BookImageSerializer
    lookup_field = 'id'

class AuthorModelViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'id'


class PrintedModelViewSet(viewsets.ModelViewSet):
    queryset = Printed.objects.all()
    serializer_class = PrintedSerializer
    lookup_field = 'id'


