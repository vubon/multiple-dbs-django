from rest_framework.response import Response
from rest_framework.views import APIView

from vubon.models import ContactInfo


class GetAndCreate(APIView):

    def get(self, request):
        response = ContactInfo.objects.all().values().order_by('-id')
        return Response(response, status=200)

    def post(self, request):
        response, status_code = ContactInfo.objects.create_data(request.data)
        return Response(response, status=status_code)
