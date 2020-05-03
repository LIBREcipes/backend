from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import Ingredient, Recipe, RecipeIngredient, MyUser, RecipeStep, File, Token


class IngredientSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Ingredient
        fields = ('__all__')

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = MyUser
        fields = ('uuid', 'username', 'first_name', 'last_name', 'email', 'language', 'password')


class FileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = File
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    ingredient = IngredientSerializer(read_only=True)
    ingredient_uuid = serializers.SlugRelatedField(slug_field='uuid', queryset=Ingredient.objects.all(), write_only=True)

    class Meta:
        model = RecipeIngredient
        exclude = ('recipe',)

class StepSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = RecipeStep
        exclude = ('recipe',)

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, required=False)
    chef = UserSerializer(many=False, read_only=True)
    steps = StepSerializer(many=True, required=False)
    image = FileSerializer(read_only=True)
    image_id = serializers.PrimaryKeyRelatedField(
            source='image', 
            write_only=True,
            queryset=File.objects.all(),
            required=False
        )

    def create(self, validated_data):
        step_data = validated_data.pop('steps', [])
        ingredient_data = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)

        for data in step_data:
            RecipeStep.objects.create(recipe=recipe, **data)
        
        for data in ingredient_data:
            print(data)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=data.pop('ingredient_uuid'), **data)

        return recipe

    def update(self, instance, validated_data):
        if 'steps' in validated_data:
            self.update_steps(instance, validated_data.pop('steps'))

        if 'ingredients' in validated_data:
            self.update_ingredients(instance, validated_data.pop('ingredients'))

        if 'image' in validated_data:
            self.update_image(instance, validated_data.pop('image'))

        instance.name = validated_data.pop('name', instance.name)
        instance.description = validated_data.pop('description', instance.description)
        instance.portion_size = validated_data.pop('portion_size', instance.portion_size)
        instance.portion_type = validated_data.pop('portion_type', instance.portion_type)
        instance.is_public = validated_data.pop('is_public', instance.is_public)

        instance.save()
        return instance
    
    def update_steps(self, instance, steps_data):
        step_dict = dict((i.id, i) for i in instance.steps.all())
        instance_steps = dict((i.step, i) for i in instance.steps.all())

        for step in steps_data:
            if 'id' in step:
                stepCheckId = instance_steps.get(step['step']).id
                if step['id'] is not stepCheckId:
                    step_dict.pop(stepCheckId).delete()

                step_item = step_dict.pop(step['id'])
                serializer = StepSerializer(instance=step_item, data=step, partial=True)
                if serializer.is_valid():
                    serializer.save()
            
            else:
                RecipeStep.objects.create(recipe=instance, **step)
        
        if len(step_dict) > 0:
            for step in step_dict.values():
                step.delete()

        return instance

    def update_ingredients(self, instance, ingredient_data):
        ingredient_dict = dict((i.id, i) for i in instance.ingredients.all())

        for ing in ingredient_data:
            if 'id' in ing:
                ing_item = ingredient_dict.pop(ing['id'])
                ingredient = ing.pop('ingredient_uuid', ing_item.ingredient)
                serializer = RecipeIngredientSerializer(instance=ing_item, data=ing, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(ingredient=ingredient)
            else:
                RecipeIngredient.objects.create(recipe=instance, ingredient=ing.pop('ingredient_uuid'), **ing)

        if len(ingredient_dict) > 0:
            for ing in ingredient_dict.values():
                ing.delete()

    def update_image(self, instance, image):
        if image.owner.id is not self.context['request'].user.id:
            raise serializers.ValidationError('Can not find this file.')
        instance.image = image

    class Meta:
        model = Recipe
        fields = ('__all__')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        returnVal = super().validate(attrs)

        if not self.user.is_confirmed:
            raise exceptions.AuthenticationFailed("You're account has not been verified yet.")

        return returnVal

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # del token['user_id']
        # token['uuid'] = str(user.uuid)

        return token