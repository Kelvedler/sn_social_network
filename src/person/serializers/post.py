from rest_framework import serializers

from person.models import Post


class PostModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['text', 'person']

    def create(self, validated_data):
        return Post.objects.create(text=validated_data['text'], person=validated_data['person'])
