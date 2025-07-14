# statgen/backend/core/serializers.py
from rest_framework import serializers
from .models import Experiment
from django.contrib.auth.models import User

class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'
        # Adicione esta linha para tornar o owner um campo de leitura
        read_only_fields = ['owner']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Campos que queremos para o registro
        fields = ['id', 'username', 'email', 'password']
        # Garante que a senha não seja enviada de volta na resposta da API
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Cria e retorna um novo usuário, com uma senha hasheada.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
