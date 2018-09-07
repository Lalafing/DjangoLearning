from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet
# from snippets.models import Snippet, LANGUAGES_CHOICE, STYLE_CHOICE


# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(
#         required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'testarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(
#         choices=LANGUAGES_CHOICE, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICE, default='friendly')
class SnippetSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(
        view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'title', 'code', 'linenos',
                  'language', 'style', 'owner')

    def create(self, validated_data):
        """
        Create and return a new `Snippet instance, given the validated data.

        Args:
            validated_data (TYPE): Description

        Returns:
            TYPE: Description
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance,
        given the validated data.

        Args:
            instance (TYPE): Description
            validated_data (TYPE): Description

        Returns:
            TYPE: Description
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedIdentityField(
        many=True, view_name='snippets-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')
