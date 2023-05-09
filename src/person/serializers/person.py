from rest_framework import serializers

from person.models import Person


class PersonSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=150)
    password = serializers.CharField(min_length=3, max_length=20)

    def get_from_credentials(self, validated_data):
        try:
            person = Person.objects.get(name=validated_data['name'])
            assert person.check_password(validated_data['password'])
        except (Person.DoesNotExist, AssertionError):
            return None
        else:
            return person


class PersonModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ['name', 'password']
        extra_kwargs = {
            'name': {'min_length': 3, 'max_length': 150},
            'password': {'min_length': 8, 'max_length': 20, 'write_only': True}
        }

    def create(self, validated_data):
        person = Person(name=validated_data['name'])
        person.set_password(validated_data['password'])
        person.save()
        return person
