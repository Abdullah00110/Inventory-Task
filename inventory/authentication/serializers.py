from rest_framework import serializers
from authentication.models import MyUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type' : 'password' }, write_only = True)
    class Meta:
        model = MyUser
        fields = ['email' , 'username', 'password', 'password2', 'tc']
        extra_kwargs = {
            'passsword' : {
                'write_only' : True
            }
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        print(f"This is password ---> {password} and password2 {password2}")
        if password != password2:
            raise serializers.ValidationError("Password and confirm Password dosen't match")    
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        return MyUser.objects.create_user(**validated_data)
    

# Login Serializer

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = MyUser
        fields = ['username', 'password' ]
    
    
