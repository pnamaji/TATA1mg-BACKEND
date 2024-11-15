from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken, AccessToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from twilio.rest import Client
import json, random, string, logging
from .models import UserData, LoginHistory
from Account.serializers import *
from decouple import config
import logging
import jwt
import datetime

account_sid = config('TWILIO_ACCOUNT_SID')  # Replace with your Account SID
auth_token =  config('TWILIO_AUTH_TOKEN')    # Replace with your Auth Token
twilio_phone_number = config('TWILIO_PHONE_NO')  # Replace with your Twilio phone number

client = Client(account_sid, auth_token)

# Create your views here.

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        # Update the last login history entry with logout time
        try:
            login_history = LoginHistory.objects.filter(user=user).order_by('-login_time').first()
            if login_history:
                login_history.logout_time = timezone.now()
                login_history.save()

            # Get the refresh token from the request
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate the refresh token and get the corresponding outstanding token
            outstanding_token = OutstandingToken.objects.filter(token=refresh_token).first()
            if not outstanding_token:
                return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the token using the OutstandingToken instance
            BlacklistedToken.objects.create(token=outstanding_token)

            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class LoginWithEmail(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email = data.get('email')
            
            if User.objects.filter(email=email).exists():
                
                # Generate OTP for SMS
                otp = ''.join(random.choices(string.digits, k=5))
                
                # Set OTP expiration time (5 minutes from now)
                otp_expiry_time = timezone.now() + timedelta(minutes=5)

                # Token Expiration set to 1 hour
                token_expiry_time = timezone.now() + timedelta(hours=5)

                temp_token = jwt.encode(
                {
                    'email': email,
                    'otp': otp,
                    'exp': int(token_expiry_time.timestamp()),     # Convert to integer timestamp
                    'expotp': int(otp_expiry_time.timestamp())      # Convert to integer timestamp
                    
                },
                settings.SECRET_KEY,
                algorithm='HS256'
            )
                
                # request.session['otp'] = otp
                # request.session['email'] = email
                # request.session['otp_expiry_time'] = otp_expiry_time.isoformat()
                
                send_mail(
                    "OTP",
                    f'OTP is {otp}. Do not share this with anyone.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                return Response({'message': 'OTP Sent Successfully',
                                 'temp_token': temp_token  # Return temp token with OTP details
                                 })
            elif UserData.objects.filter(mobile_number=email).exists():

                mobile_number = email

                # Generate OTP for SMS
                otp_sms = ''.join(random.choices(string.digits, k=5))
                
                # Set OTP expiration time (5 minutes from now)
                otp_expiry_time = timezone.now() + timedelta(minutes=5)

                # Token Expiration set to 1 hour
                token_expiry_time = timezone.now() + timedelta(hours=5)

                temp_token = jwt.encode(
                {
                    'mobile_number': mobile_number,
                    'otp': otp_sms,
                    'exp': int(token_expiry_time.timestamp()),     # Convert to integer timestamp
                    'expotp': int(otp_expiry_time.timestamp())      # Convert to integer timestamp
                    
                },
                settings.SECRET_KEY,
                algorithm='HS256'
            )
                
                if not mobile_number.startswith('+91'):
                    mobile_numbers = '+91' + mobile_number
                
                try:
                    message = client.messages.create(
                        body=f'Your OTP is {otp_sms}. Do not share this with anyone.',
                        from_=twilio_phone_number,
                        to=mobile_numbers
                    )

                except Exception as e:
                    return Response({'error': str(e)}, status=500)
            
                return Response({'message': 'OTP sent. Please Enter OTP to verify your Mobile Number',
                             'temp_token': temp_token  # Return temp token with OTP details
                             }, status=200)
        
            else:
                return Response({'error': 'Mobile Number and Email does not exist'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid Json format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class ResendOTPForEmail(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            temp_token = data.get('temp_token')

            # Decode the temporary token
            try:
                payload = jwt.decode(temp_token, settings.SECRET_KEY, algorithms=['HS256'])
                if 'email' in payload:
                    identifier = payload['email']
                    identifier_type = 'email'
                elif 'mobile_number' in payload:
                    identifier = payload['mobile_number']
                    identifier_type = 'mobile_number'
                else:
                    return JsonResponse({'error': 'Invalid token payload'}, status=400)
                
                session_otp = payload['otp']
                session_otp_expiry_time = datetime.datetime.fromtimestamp(payload['expotp'])
                session_otp_expiry_time = timezone.make_aware(session_otp_expiry_time)  # Ensure it's timezone-aware

            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Temporary token expired'}, status=400)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

            
            # Generate a new OTP if the current OTP is expired
            if timezone.now() > session_otp_expiry_time:
                otp = ''.join(random.choices(string.digits, k=5))
                otp_expiry_time = timezone.now() + timedelta(minutes=5)
                
                # Update the temp_token with new OTP details
                temp_token = jwt.encode(
                    {   

                        identifier_type: identifier,
                        'otp': otp,
                        'exp': timezone.now() + timedelta(hours=5),  # Token expiry
                        'expotp': otp_expiry_time.timestamp()  # OTP expiry
                    },
                    settings.SECRET_KEY,
                    algorithm='HS256'
                )
            else:
                otp = session_otp
            
            # Resend OTP via email or SMS
            if identifier_type == 'email':
                send_mail(
                    'OTP',
                    f'Your OTP is {otp}. Do not share this with anyone.',
                    settings.DEFAULT_FROM_EMAIL,
                    [identifier]
                )
            else:
                if not identifier.startswith('+91'):
                    identifier = '+91' + identifier
                message = client.messages.create(
                    body=f'Your OTP is {otp}. Do not share this with anyone.',
                    from_=twilio_phone_number,
                    to=identifier
                )
            
            return JsonResponse({'message': 'OTP resent Successfully. Please check your email.',
                             'temp_token': temp_token  # Return temp token with OTP details
                             })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500) 
        
class VerifyOTPForEmail(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            
            data = json.loads(request.body)
            
            otp = data.get('otp')
            temp_token = data.get('temp_token')

            # Decode the temporary token
            try:
                payload = jwt.decode(temp_token, settings.SECRET_KEY, algorithms=['HS256'])
                if 'email' in payload:
                    identifier = payload['email']
                    identifier_type = 'email'
                elif 'mobile_number' in payload:
                    identifier = payload['mobile_number']
                    identifier_type = 'mobile_number'
                else:
                    return JsonResponse({'error': 'Invalid token payload'}, status=400)
                
                session_otp = payload['otp']
                session_otp_expiry_time = datetime.datetime.fromtimestamp(payload['expotp'])
                session_otp_expiry_time = timezone.make_aware(session_otp_expiry_time)  # Ensure it's timezone-aware

            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Temporary token expired'}, status=400)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
            
            # Check if OTP is expired
            if timezone.now() > session_otp_expiry_time:
                return JsonResponse({'error': 'OTP has expired'}, status=400)


            # session_otp = request.session.get('otp')
            # session_otp_expiry_time = request.session.get('otp_expiry_time')
            
            # if not session_otp or not session_otp_expiry_time:
            #     return Response({'error': 'Session Data not fount'}, status=400)
            
            # Convert session_otp_expiry_time back to a datetime object
            # otp_expiry_time = timezone.datetime.fromisoformat(session_otp_expiry_time)
            
            # if timezone.now() > otp_expiry_time:
            #     return JsonResponse({'error': 'OTP has expired'}, status=400)
            
            if otp == session_otp:
                
                # email = request.session.get('email')
                
                # Ensure that the user exists
                try:
                    if identifier_type == 'email':
                        user = User.objects.get(email=identifier)
                    else:
                        mobile_number_user = UserData.objects.get(mobile_number=identifier)
                        user = mobile_number_user.user
                except User.DoesNotExist:
                    return JsonResponse({'error': 'User not fount.'}, status=400)
                
                LoginHistory.objects.create(
                        user=user,
                        ip_address=request.META.get('REMOTE_ADDR'),
                        login_time=timezone.now()
                    )
                
                # Create tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                
                return JsonResponse({
                    'refresh_token': str(refresh),
                    'access_token': access_token
                    }, status=200)
            else:
                return JsonResponse({'error': 'Invalid OTP'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
                

class LoginWithSMS(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            
            data = json.loads(request.body)
            
            mobile_number = data.get('mobile_number')
            is_profession = data.get('is_profession')
            
            # Generate OTP for SMS
            otp_sms = ''.join(random.choices(string.digits, k=5))
            
            print(otp_sms)
        
            # Set OTP expiration time (5 minutes from now)
            otp_expiry_time = timezone.now() + timedelta(minutes=5)
            # otp_expiry_time = timezone.make_aware(otp_expiry_time)  # Ensure it's timezone-aware

            # Token expiration set to 1 hour
            token_expiry_time = timezone.now() + timedelta(hours=5)
            
            # request.session['otp_sms'] = otp_sms
            # request.session['otp_expiry_time'] = otp_expiry_time.isoformat()
            # request.session['mobile_number'] = mobile_number
            
            # If the mobile number doesn't start with +91, add it

            # Create a temporary token containing the mobile number and OTP
            temp_token = jwt.encode(
                {
                    'mobile_number': mobile_number,
                    'is_profession': is_profession,
                    'otp': otp_sms,
                    'exp': token_expiry_time.timestamp(),
                    'expotp': otp_expiry_time.timestamp()
                    
                },
                settings.SECRET_KEY,
                algorithm='HS256'
            )
            
            if not mobile_number.startswith('+91'):
                mobile_numbers = '+91' + mobile_number

            try:
                message = client.messages.create(
                    body=f'Your OTP is {otp_sms}. Do not share this with anyone.',
                    from_=twilio_phone_number,
                    to=mobile_numbers
                )
                print("Successfully")
            except Exception as e:
                return Response({'error': str(e)}, status=500)
            
            return Response({'message': 'OTP sent. Please Enter OTP to verify your account',
                             'temp_token': temp_token  # Return temp token with OTP details
                             }, status=200)
                
                
        except json.JSONDecodeError:
            return Response({'error': 'Invalid Json format'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500) 
        
class ResendOTPForSMS(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            data = json.loads(request.body)

            temp_token = data.get('temp_token')

            try:
                payload = jwt.decode(temp_token, settings.SECRET_KEY, algorithms=['HS256'])
                mobile_number = payload['mobile_number']
                is_profession = payload['is_profession']
                session_otp_sms = payload['otp']
                session_otp_expiry_time = datetime.datetime.fromtimestamp(payload['expotp'])
                session_otp_expiry_time = timezone.make_aware(session_otp_expiry_time)  # Ensure it's timezone-aware

            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Temporary token expired'}, status=400)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
            
            # if timezone.now() > session_otp_expiry_time:
            #     return JsonResponse({'error': 'OTP has expired'}, status=400)

            # Check if the session already has an OTP
            # session_otp_sms = request.session.get('otp_sms')
            # session_otp_expiry_time = request.session.get('otp_expiry_time')
            
            # Generate a new OTP if the current OTP is expired
            if timezone.now() > session_otp_expiry_time:
                otp_sms = ''.join(random.choices(string.digits, k=5))
                otp_expiry_time = timezone.now() + timedelta(minutes=5)
                
                # Update the temp_token with new OTP details
                temp_token = jwt.encode(
                    {
                        'mobile_number': mobile_number,
                        'is_profession': is_profession,
                        'otp': otp_sms,
                        'exp': timezone.now() + timedelta(hours=5),  # Token expiry
                        'expotp': otp_expiry_time.timestamp()  # OTP expiry
                    },
                    settings.SECRET_KEY,
                    algorithm='HS256'
                )
            else:
                otp_sms = session_otp_sms
            
            # mobile_number = request.session.get('mobile_number')
            # if not mobile_number:
            #     return JsonResponse({'error': "Mobile Number not found in session."}, status=400)
            
            # If the mobile number doesn't start with +91, add it
            if not mobile_number.startswith('+91'):
                mobile_number = '+91' + mobile_number
            
            message = client.messages.create(
                    body=f'Your OTP is {otp_sms}. Do not share this with anyone.',
                    from_=twilio_phone_number,
                    to=mobile_number
                )
            
            return JsonResponse({'message': 'OTP resent Successfully. Please check your Mobile.',
                             'temp_token': temp_token  # Return temp token with OTP details
                             })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class VerifyOTPForSMS(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Extract OTP and other session data
            otp = data.get('otp')
            temp_token = data.get('temp_token')

            # session_otp = request.session.get('otp_sms')
            # session_otp_expiry_time = request.session.get('otp_expiry_time')
            # mobile_number = request.session.get('mobile_number')

            # Decode the temporary token
            try:
                payload = jwt.decode(temp_token, settings.SECRET_KEY, algorithms=['HS256'])
                mobile_number = payload['mobile_number']
                is_profession = payload['is_profession']
                session_otp = payload['otp']
                session_otp_expiry_time = datetime.datetime.fromtimestamp(payload['expotp'])
                # session_otp_expiry_time = timezone.make_aware(session_otp_expiry_time)  # Ensure it's timezone-aware

            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Temporary token expired'}, status=400)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=400)

            # if not session_otp or not session_otp_expiry_time or not mobile_number:
            #     return JsonResponse({'error': 'OTP or mobile number not found'}, status=400)

            # Convert session_otp_expiry_time back to a datetime object
            # otp_expiry_time = timezone.datetime.fromisoformat(session_otp_expiry_time)

            # if timezone.now() > session_otp_expiry_time:
            #     return JsonResponse({'error': 'OTP has expired'}, status=400)

            # Check if OTP is expired
            # if timezone.now() > otp_expiry_time:
            #     return JsonResponse({'error': 'OTP has expired'}, status=400)
            
            # Verify the OTP
            if otp == session_otp:
                # Check if the user with the given mobile number exists
                try:
                    mobile_number_user = UserData.objects.get(mobile_number=mobile_number)
                    user = mobile_number_user.user

                    # If user exists, log them in
                    LoginHistory.objects.create(
                        user=user,
                        ip_address=request.META.get('REMOTE_ADDR'),
                        login_time=timezone.now()
                    )

                    # Create tokens
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)

                    return JsonResponse({
                        'refresh_token': str(refresh),
                        'access_token': access_token,
                        'message': 'Login successful'
                    }, status=200)
                
                except UserData.DoesNotExist:
                    # If the user does not exist, store the mobile number and OTP in the session for registration
                    # request.session['mobile_number'] = mobile_number
                    # request.session['otp_sms'] = otp

                    return JsonResponse({
                        'message': 'User does not exist. Please complete the registration.',
                        'status': 'new_user',
                        'temp_token': temp_token  # Return the same token for signup
                    }, status=200)
            
            else:
                return JsonResponse({'error': 'Invalid OTP'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            # Ensure that an error response is returned in case of an exception
            return JsonResponse({'error': str(e)}, status=500)
        

class SignInView(APIView):
    permission_classes = [AllowAny]
       
    def post(self, request):
        try:
            # Load the incoming data as JSON
            data = json.loads(request.body)
            
            email = data.get('email')
            location = data.get('location')
            temp_token = data.get('temp_token')

            # Decode the temporary token to get the mobile number
            try:
                payload = jwt.decode(temp_token, settings.SECRET_KEY, algorithms=['HS256'])
                mobile_number = payload['mobile_number']
                is_profession = payload['is_profession']
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Temporary token expired'}, status=400)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=400)
            
            if not email:
                return Response({'error': 'Email Required'})
            
            # mobile_number = request.session['mobile_number']
            
            if not mobile_number:
                return Response({'error': 'Mobile number not found'})
            
            # Create User
            user = User.objects.create_user(username=email, email=email)
            
            user_data = UserData(user=user, email=email, mobile_number=mobile_number)
            user_data.save()
            
            serializer = UserDataSerializer(user_data)
            
            user_profile = UserProfile(user=user, location=location, is_professional=is_profession)
            user_profile.save()
            
            serializer = UserProfileSerializer(user_profile)

            # Explicitly set the backend (if you're using a custom backend, specify it here)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            
            LoginHistory.objects.create(
                user=user,
                ip_address=request.META.get('REMOTE_ADDR'),
                login_time=timezone.now()
            )
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return JsonResponse({
                'refresh_token': str(refresh),
                'access_token': access_token
                })
                 
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)