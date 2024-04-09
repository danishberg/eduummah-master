from rest_framework import serializers
from .models import Course, Lesson, UserProgress
from .models import CustomUser

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'date_of_birth', 'details_set']
        read_only_fields = ['details_set']

    def update(self, instance, validated_data):
        # Prevent updating if details are already set
        if instance.details_set:
            raise serializers.ValidationError("User details are already set.")
        
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.details_set = True
        instance.save()
        return instance
