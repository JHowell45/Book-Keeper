from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World! From Django.")


class Register(APIView):
    def post(self, request):
        required_params = ["username", "password", "email"]
        try:
            data = request.data
            if all(key in data for key in required_params):
                try:
                    username = self.validate_required_input(
                        required_params[0], data[required_params[0]]
                    )
                    password = self.validate_required_input(
                        required_params[1], data[required_params[1]]
                    )
                    email = self.validate_required_input(
                        required_params[2], data[required_params[2]]
                    )
                except ValidationError as error:
                    return Response(
                        {"error": str(error.messages[0])},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                new_user = User()
                new_user.username = username
                new_user.set_password(password)
                new_user.email = email

                try:
                    new_user.first_name = (
                        data["firstname"] if data["firstname"] is not None else ""
                    )
                except KeyError:
                    print("Error while parsing firstname!")

                try:
                    new_user.last_name = (
                        data["lastname"] if data["lastname"] is not None else ""
                    )
                except KeyError:
                    print("Error while parsing lastname!")

                new_user.save()
                return Response({"status": "Success"}, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {
                        "error": "Required param(s) missing, Please include and retry "
                        "again"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as error:
            print(f"Unexpected exception: {error}")
            return Response(
                {"error": "Unexpected error occurred, please report this to Admin"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class Login(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response("Authentication Successful.")
