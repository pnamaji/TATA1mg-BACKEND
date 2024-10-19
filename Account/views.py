from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from twilio.rest import Client
import json, random, string, logging
from .models import UserData, LoginHistory
from Account.serializers import *


account_sid = 'AC517ca9863822b144521cb743ca0eacc1'  # Replace with your Account SID
auth_token =  'd715da9b6e2b0d79f3ab8e7c2309bd18'    # Replace with your Auth Token
twilio_phone_number = '+14806855921'  # Replace with your Twilio phone number

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

            # Get refresh token from request data
            refresh_token = request.data.get("refresh_token")
            if refresh_token is None:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the refresh token to log the user out
            token = RefreshToken(refresh_token)
            token.blacklist()

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
                
                request.session['otp'] = otp
                request.session['otp_expiry_time'] = otp_expiry_time.isoformat()
                
                send_mail(
                    "OTP",
                    f'OTP is {otp}. Do not share this with anyone.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                return Response({'message': 'OTP Sent Successfully'})
            else:
                return JsonResponse({'error': 'Email Does not exists'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid Json format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500) 
        
class VerifyOTPForEmail(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            
            data = json.loads(request.body)
            
            otp = data.get('otp')
            session_otp = request.session.get('otp')
            session_otp_expiry_time = request.session.get('otp_expiry_time')
            
            if not session_otp or not session_otp_expiry_time:
                return Response({'error': 'Session Data not fount'}, status=400)
            
            # Convert session_otp_expiry_time back to a datetime object
            otp_expiry_time = timezone.datetime.fromisoformat(session_otp_expiry_time)
            
            if timezone.now() > otp_expiry_time:
                return JsonResponse({'error': 'OTP has expired'}, status=400)
            
            if otp == session_otp:
                
                email = request.session.get('email')
                
                email_user = UserData.objects.get(email=email)
                user = email_user.user
                
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
            
            if UserData.objects.filter(mobile_number=mobile_number).exists():
                
                # Generate OTP for SMS
                otp_sms = ''.join(random.choices(string.digits, k=5))
                
                print(otp_sms)
            
                # Set OTP expiration time (5 minutes from now)
                otp_expiry_time = timezone.now() + timedelta(minutes=5)
                
                request.session['otp_sms'] = otp_sms
                request.session['otp_expiry_time'] = otp_expiry_time.isoformat()
                
                try:
                    message = client.messages.create(
                        body=f'Your OTP is {otp_sms}. Do not share this with anyone.',
                        from_=twilio_phone_number,
                        to=mobile_number
                    )
                    print("Successfully")
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=500)
                
                return JsonResponse({'message': 'OTP sent. Please Enter OTP to verify your account'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid Json format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500) 
            

class VerifyOTPForSMS(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            data = json.loads(request.body)
                
            otp = data.get('otp')
            session_otp = request.session.get('otp_sms')
            session_otp_expiry_time = request.session.get('otp_expiry_time')
            
            if not session_otp or not session_otp_expiry_time:
                return JsonResponse({'error': 'OTP not found'}, status=400)

            # Convert session_otp_expiry_time back to a datetime object
            otp_expiry_time = timezone.datetime.fromisoformat(session_otp_expiry_time)

            # Check if OTP is expired
            if timezone.now() > otp_expiry_time:
                return JsonResponse({'error': 'OTP has expired'}, status=400)
            
            if otp == session_otp:
                
                mobile_number = request.session.get('mobile_number')
                
                mobile_number_user = UserData.objects.get(mobile_number=mobile_number)
                user = mobile_number_user.user
                
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
        
        


class SignUp(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            
            data = json.loads(request.body)
            
            email = data.get('email')
            mobile_number = data.get('mobile_number')
            
            # Print the debug info (for development use only)
            print(email, mobile_number)
            
            #  Ensure email or mobile_number doesn't already exist
            if UserData.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            if UserData.objects.filter(mobile_number=mobile_number).exists():
                return JsonResponse({'error': 'Mobile number already exists'}, status=400)
            
            # Ensure all required fields are provided 
            if not ( email and mobile_number):
                return JsonResponse({'error': 'All fields are required'}, status=400)
            
            # Generate OTP for email
            otp_value = ''.join(random.choices(string.digits, k=5))
            
            # Generate OTP for SMS
            otp_sms = ''.join(random.choices(string.digits, k=5))
            
            print(otp_sms)
            
            # Set OTP expiration time (5 minutes from now)
            otp_expiry_time = timezone.now() + timedelta(minutes=5)
            
            print("working")
            
            # Store Data in Session (avoid storing sensitive info like passwords)
            request.session['email'] = email
            request.session['mobile_number'] = mobile_number
            request.session['otp'] = otp_value
            request.session['otp_sms'] = otp_sms
            request.session['otp_expiry_time'] = otp_expiry_time.isoformat()
            
            # Send OTP email
            try:
                send_mail(
                    'OTP',
                    f'Your OTP is {otp_value}. Do not share this with anyone.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                print("Email sent successfully")
            except Exception as e:
                print(f"Failed to send email: {e}")
                return JsonResponse({'error': 'Failed to send OTP via email'}, status=500)
            try:
                message = client.messages.create(
                    body=f'Your OTP is {otp_sms}. Do not share this with anyone.',
                    from_=twilio_phone_number,
                    to=mobile_number
                )
                print("Successfully")
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
            
            return JsonResponse({'message': 'OTP sent. Please Enter OTP to verify your account'}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid Json format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
class ResendOTP(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            # Check if the session already has an OTP
            session_otp_sms = request.session.get('otp_sms')
            session_otp = request.session.get('otp')
            session_otp_expiry_time = request.session.get('otp_expiry_time')
            
            # Check if there's already an OTP and if it's not expired
            if session_otp and session_otp_expiry_time:
                otp_expiry_time = timezone.datetime.fromisoformat(session_otp_expiry_time)
                if timezone.now() < otp_expiry_time:
                    # if OTP is valid, reuse the existing OTP
                    otp_value = session_otp
                    otp_sms = session_otp_sms
                else:
                    # OTP is expired, generate a new one
                    otp_value = ''.join(random.choices(string.digits, k=5))
                    otp_sms = ''.join(random.choices(string.digits, k=5))
                    otp_expiry_time = timezone.now() + timedelta(minutes=5)
                    request.session['otp'] = otp_value
                    request.session['otp_sms'] = otp_sms
                    request.session['otp_expiry_time'] = otp_expiry_time.isoformat()
                    
            else:
                # No OTP found or session expired, generate a new OTP
                otp_value = ''.join(random.choices(string.digits, k=5))
                otp_sms = ''.join(random.choices(string.digits, k=5))
                otp_expiry_time = timezone.now() + timedelta(minutes=5)
                request.session['otp'] = otp_value
                request.session['otp_sms'] = otp_sms
                request.session['otp_expiry_time'] = otp_expiry_time.isoformat()

            # Send OTP email
            email = request.session.get('email')
            if not email:
                return JsonResponse({'error': 'Email not found in session'}, status=400)
            
            send_mail(
                'OTP',
                f'OTP is {otp_value}. Do not share this with anyone.',
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            
            mobile_number = request.session.get('mobile_number')
            if not mobile_number:
                return JsonResponse({'error': "Mobile Number not found in session."}, status=400)
            
            message = client.messages.create(
                    body=f'Your OTP is {otp_sms}. Do not share this with anyone.',
                    from_=twilio_phone_number,
                    to=mobile_number
                )
            
            return JsonResponse({'message': 'OTP resent Successfully. Please check your email.'})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
class verify_otp_view(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
       
    def post(self, request):
        try:
            # Load the incoming data as JSON
            data = json.loads(request.body)

            otp_value = data.get('otp')
            otp_sms = data.get('otp_sms')
            session_sms = request.session.get('otp_sms')
            session_otp = request.session.get('otp')
            session_otp_expiry_time = request.session.get('otp_expiry_time')

            if not session_otp or not session_otp_expiry_time:
                return JsonResponse({'error': 'OTP not found'}, status=400)

            # Convert session_otp_expiry_time back to a datetime object
            otp_expiry_time = timezone.datetime.fromisoformat(session_otp_expiry_time)

            # Check if OTP is expired
            if timezone.now() > otp_expiry_time:
                return JsonResponse({'error': 'OTP has expired'}, status=400)

            # Check if OTP matches
            if otp_value == session_otp:
                if otp_sms == session_sms:
                    email = request.session['email']
                    mobile_number = request.session['mobile_number']
                    
                    # Create User
                    user = User.objects.create_user(username=email, email=email)
                    
                    user_data = UserData(user=user, email=email, mobile_number=mobile_number)
                    user_data.save()
                    
                    serializer = UserDataSerializer(user_data)

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
                    
                    # Optionally log the user in
                    # login(request, user)  # Uncomment this if you want to log the user in
                    
                    # Return a success message along with user data
                    # return JsonResponse({'success': True, 'message': 'OTP verified', 'user_id': user.id})
                else:
                    return JsonResponse({'error': 'Invalid SMS OTP'}, status=400)
            else:
                return JsonResponse({'error': 'Invalid email OTP'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)