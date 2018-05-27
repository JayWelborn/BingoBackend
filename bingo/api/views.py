from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.views import APIView

from .serializers import EmailFormSerializer


class EmailFormView(APIView):
    """Endpoint for sending contact emails

    Fields:
        allowed_methods: restrict allowed methods to `POST`

    Methods:
        post: send email on post request
    """

    allowed_methods = ['POST']
    serializer_class = EmailFormSerializer

    def post(self, request):
        """
        Send email on POST requests
        """
        serializer = EmailFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send_email()
            return Response(request.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
