from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser, generate_username, generate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

class CustomAdminLoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        
        data = super().validate(attrs)
        
        data['username'] = self.user.username
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name

        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'password', 'password2',
                  'class_number', 'class_letter', 'is_teacher', 'is_student',
                  'school_token', 'info_token']
        extra_kwargs = {
            'username': {'required': False},
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password or password2:
            if password != password2:
                raise serializers.ValidationError({"password": "Parollar mos emas"})
        return data

    def create(self, validated_data):
        first_name = validated_data.get('first_name', 'user')
        last_name = validated_data.get('last_name', 'name')

        username = validated_data.get('username') or generate_username(first_name, last_name)

        password = validated_data.get('password')
        password2 = validated_data.get('password2')

        if not password and not password2:
            auto_password = generate_password()
            password = auto_password
            password2 = auto_password

        if password != password2:
            raise serializers.ValidationError({"password": "Parollar mos emas"})

        user = CustomUser(
            username=username,
            first_name=first_name,
            last_name=last_name,
            class_number=validated_data.get('class_number'),
            class_letter=validated_data.get('class_letter'),
            is_teacher=validated_data.get('is_teacher', False),
            is_student=validated_data.get('is_student', False),
            school_token=validated_data.get('school_token'),
            info_token=validated_data.get('info_token'),
            see_password=password
        )
        print(password)
        user.set_password(password)
        user.save()
        self._generated_username = username
        self._generated_password = password

        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['username'] = getattr(self, '_generated_username', instance.username)
        rep['password'] = getattr(self, '_generated_password', None)
        rep['password2'] = getattr(self, '_generated_password', None)  
        return rep
