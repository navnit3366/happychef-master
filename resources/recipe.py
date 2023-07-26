from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.recipe import Recipe, recipe_list

class RecipeListResource(Resource):

    """Will find and return all recipe data by iterating through each item and returning a temporary list"""

    def get(self):

        data = []

        for recipe in recipe_list:
            if recipe.is_publish is True:
                data.append(recipe.data)

        return {"data": data}, HTTPStatus.OK

    """Creates a new recipe item using POST command. 
    
    It does this by getting the JSON data back from the request using request.get_json
    and then creates the recipe object and stores that in recipe_list
    Finally, it returns the recipe record with an HTTP status code 201 CREATED"""

    def post(self):
        data = request.get_json()

        recipe = Recipe(name=data["name"],
                        description=data["description"],
                        num_of_servings=data["num_of_servings"],
                        cook_time=data["cook_time"],
                        directions=data["directions"]
        )

        recipe_list.append(recipe)

        return recipe.data, HTTPStatus.CREATED

class RecipeResource(Resource):

    """Searches in our recipe_list for the given recipe ID. 
    Will ony return when finding a match that is published"""

    def get(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id and recipe.is_publish == True), None)

        if recipe is None:
            return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND

        return recipe.data, HTTPStatus.OK

    """This put method gets the recipe details from the client request using request.get_json
    and updates the recipe object. Then it returns the HTTP status code 200 OK
    
    Great example of a n00b!3 code smell. I have no idea how to fix the
    issue where a few of the data points populate as lists as opposed to 
    strings/integers. Will be fun to figure that out later."""

    def put(self, recipe_id):
        data = request.get_json()

        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND

        recipe.name = data["name"]
        recipe.description = data["description"]
        recipe.num_of_servings = data["num_of_servings"]
        recipe.cook_time = data["cook_time"]
        recipe.directions = data["directions"]

        return recipe.data, HTTPStatus.OK

    """Write a script that deletes a recipe once called"""

    def delete(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND

        recipe_list.remove(recipe)

        return {}, HTTPStatus.OK

class RecipePublishResource(Resource):

    """The following put method will locate the recipe with the
    passed-in recipe_id and update the is_publish status to True.
    This indicates that the recipe has been published successfully."""

    def put(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND

        recipe.is_publish = True

        return {}, HTTPStatus.NO_CONTENT

    """The following delete method is the opposite of the previous put method.
    This piece of code sets is_publish to false instead of true.
    """

    def delete(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND

        recipe.is_publish = False

        return {}, HTTPStatus.NO_CONTENT
