from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from . import models,forms,serializers
from django.contrib.auth.forms import UserCreationForm
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
import jwt
from django.conf import settings
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
from dotenv import load_dotenv
import os 
import time
import datetime
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from allauth.account.forms import \
    default_token_generator as allauth_token_generator
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import int_to_base36, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.http import Http404,HttpResponse
from django.urls import reverse_lazy
from django.views import View


load_dotenv()

#? Neo4j Database
class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def serialize_post(self,result):
        post_data = result.get('post')
        profile = get_object_or_404(models.Profile,id=post_data['profile_id'])
        post_data['profile'] = serializers.ProfileSerializer(profile,many=False).data
        post_data['edit'] = datetime.datetime.fromtimestamp( post_data.get('edit')/1000 )  
        post_data['create'] = datetime.datetime.fromtimestamp( post_data.get('create')/1000 ) 
        return post_data

    def serialize_news(self,result):
        post_data = result.get('news')
        profile = get_object_or_404(models.Profile,id=post_data['profile_id'])
        post_data['profile'] = serializers.ProfileSerializer(profile,many=False).data
        post_data['edit'] = datetime.datetime.fromtimestamp( post_data.get('edit')/1000 )  
        post_data['create'] = datetime.datetime.fromtimestamp( post_data.get('create')/1000 ) 
        return post_data

    def serialize_comment(self,result):
        post_data = result.get('comment')
        profile = get_object_or_404(models.Profile,id=post_data['profile_id'])
        post_data['profile'] = serializers.ProfileSerializer(profile,many=False).data
        post_data['create'] = datetime.datetime.fromtimestamp( post_data.get('create')/1000 ) 
        return post_data



    #!Add profile
    def add_profile_helper(self, tx,username, profile_id):
        query = (
            "CREATE (profile:Profile {profile_id:$profile_id, username:$username, followers_count:0, following_count:0}) RETURN profile"
        )
        result = tx.run(query, username=username, profile_id=profile_id)
        
        try:
                return ([row.data()
                    for row in result])
        except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
                raise
        
    def add_profile(self, profile_id, username):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.add_profile_helper, username, profile_id)
            return result

    #!Is following
    def is_following_profile_helper(self, tx, profile_id, follow_id):
        query = (
            "MATCH (profile:Profile {profile_id:$profile_id}) " 
            "MATCH (following_p:Profile {profile_id:$follow_id}) "
            "RETURN EXISTS ((profile) -[:Following]-> (following_p))"
        )
        result = tx.run(query, profile_id=profile_id, follow_id=follow_id)
        
        try:
                return ([row.data()
                    for row in result])
        except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
                raise
        
    def is_following_profile(self,  profile_id, follow_id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.is_following_profile_helper, profile_id=profile_id, follow_id=follow_id)
            dp=result[0]
            dp_values = dp.values()
            state = False
            for i in dp_values:
                state=i
            return state

    #!Follow profile
    def follow_profile_helper(self, tx, profile_id, follow_id):
        query = (
            "MATCH (profile:Profile {profile_id:$profile_id}) "
            "MATCH (following:Profile {profile_id:$follow_id}) "
            "CREATE (profile) -[:Following]-> (following) "
            "SET profile.following_count=profile.following_count + 1 "
            "SET following.followers_count=following.followers_count + 1 "
            "RETURN following"
        )
        result = tx.run(query, profile_id=profile_id, follow_id=follow_id)
        
        try:
                return ([row.data()
                    for row in result])
        except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
                raise
        
    def follow_profile(self,  profile_id, follow_id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.follow_profile_helper, profile_id, follow_id)
            return result

    #!Unfollow profile
    def unfollow_profile_helper(self, tx, profile_id, follow_id):
        query = (
            "MATCH (profile:Profile {profile_id:$profile_id}) " 
            "MATCH (following:Profile {profile_id:$follow_id}) "
            "MATCH (profile)-[r:Following]->(following) "
            "DELETE r "
            "SET profile.following_count=profile.following_count - 1 "
            "SET following.followers_count=following.followers_count - 1 "
            "RETURN following"
        )
        result = tx.run(query, profile_id=profile_id, follow_id=follow_id)
        
        try:
                return ([row.data()
                    for row in result])
        except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
                raise
        
    def unfollow_profile(self,  profile_id, follow_id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.unfollow_profile_helper, profile_id=profile_id, follow_id=follow_id)
            return result




    #!Add post
    def add_post_helper(self, tx, file, text, profile_id):
        query = (
            "MATCH (profile:Profile {profile_id:$profile_id}) CREATE (post:Post {text:$text, file:$file, profile_id:$profile_id, comment_count:0, like_count:0, create:TIMESTAMP(), edit:TIMESTAMP()}) CREATE (profile) -[:Posted]-> (post) RETURN post"
        )
        result = tx.run(query, text=text, profile_id=profile_id,file=file)
        
        try:
                return ([row.data()
                    for row in result])
        except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
                raise
        
    def add_post(self, file, text, profile_id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.add_post_helper, file, text, profile_id)
            output = self.serialize_post(result[0])
            return output

    #!Delete post
    def delete_post_helper(self, tx, id):
        query = (
            "MATCH (post:Post) "
            "WHERE ID(post)=$id "
            "DETACH DELETE post"
        )
        result = tx.run(query, id=id)
        
        try:
            return ([row.data()
                for row in result])
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
            query=query, exception=exception))
            raise

    def delete_post(self, id):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.execute_write(
                self.delete_post_helper, id)
            return result

    #!Get post
    def get_post_helper(self, tx, id):
        query = (
            "MATCH (post:Post) "
            "WHERE ID(post)=$id "
            "RETURN post"
        )
        result = tx.run(query,id=id)
        
        try:
            return ([row.data()
                for row in result])
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
            query=query, exception=exception))
            raise

    def get_post(self, id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.get_post_helper,id=id)
            if result==[]:
                return "E"
            output = self.serialize_post(result[0])
            return output

    #!Update post
    def update_post_helper(self,tx,file, id,text,delete):
        query = (
            "MATCH (post:Post) "
            "WHERE ID(post)=$id "
            "SET post.text = $text "
            "SET post.update = TIMESTAMP() "
            "SET post.file = $file "
            "RETURN post"
        )
        result = tx.run(query,id=id,text=text,delete=delete,file=file)
        try:
            return ([row.data()
                for row in result])
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
            query=query, exception=exception))
            raise

    def update_post(self,id,file,text,delete):
        if text!=None:
            with self.driver.session(database="neo4j") as session:
                result = session.execute_write(
                self.update_post_helper,id=id,text=text,delete=delete,file=file)
                output = self.serialize_post(result[0])
                return output
        else:
            print("no data given")

    #!Filter post by text
    def filter_post_text_helper(self,tx,text):
        query = (
            "MATCH (post:Post) "+ "WHERE post.text CONTAINS '"+text +"' RETURN post ORDER BY post.create DESC"
        )
        result = tx.run(query,text=text)
        
        try:
            return ([row.data()
                for row in result])
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
            query=query, exception=exception))
            raise

    def filter_post_text(self,text):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.filter_post_text_helper,text)
            arr=[]
            for i in result:
                arr.append(self.serialize_post(i))
            return arr

    #!Get the post that got most likes
    def most_liked_post_helper(self,tx):
        query = (
            "MATCH (post:Post) WHERE post.create > TIMESTAMP()-604800000 RETURN post ORDER BY post.like_count DESC LIMIT 1"
        )
        result = tx.run(query)
        
        try:
            return ([row.data()
                for row in result])
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
            query=query, exception=exception))
            raise

    def most_liked_post(self):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.most_liked_post_helper)
            if result==[]:
                return "E"
            arr=[]
            for i in result:
                arr.append(self.serialize_post(i))
            return arr

    #!Most commented post
    def most_commented_post_helper(self,tx):
        query = (
            "MATCH (post:Post) WHERE post.create > TIMESTAMP()-604800000 RETURN post ORDER BY post.comment_count DESC LIMIT 1"
        )
        result = tx.run(query)
        
        try:
            return ([row.data()
                for row in result])
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
            query=query, exception=exception))
            raise

    def most_commented_post(self):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.most_commented_post_helper)
            if result==[]:
                return "E"
            arr=[]
            for i in result:
                arr.append(self.serialize_post(i))
            return arr


    #!Like a post
    def like_a_post_helper(self,tx,post_id,profile_id):
        query = (
            "MATCH (post:Post) WHERE ID(post)=$post_id MATCH (profile:Profile) WHERE profile.profile_id=$profile_id " 
            "CREATE (profile) -[:Liked]-> (post) SET post.like_count=post.like_count + 1 RETURN post"
        )
        result = tx.run(query,post_id=post_id,profile_id=profile_id)
        
        try:
            return ([row.data()
                for row in result])
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
            query=query, exception=exception))
            raise

    def like_a_post(self,post_id,profile_id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.like_a_post_helper,post_id=post_id,profile_id=profile_id)
            output = self.serialize_post(result[0])
            return result

    #!Check if liked
    def check_if_liked_post_helper(self,tx,post_id,profile_id):
        query = (
            "MATCH (post:Post) "
            "WHERE ID(post)=$post_id "
            "MATCH (profile:Profile {profile_id:$profile_id}) "
            "RETURN EXISTS( (profile) -[:Liked]-> (post) )"
        )
        result = tx.run(query,post_id=post_id,profile_id=profile_id)
        
        try:
            return ([row.data()
                for row in result])
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
            query=query, exception=exception))
            raise

    def check_if_liked_post(self,post_id,profile_id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.check_if_liked_post_helper,post_id=post_id,profile_id=profile_id)
            dp=result[0]
            dp_values = dp.values()
            state = False
            for i in dp_values:
                state=i
            return state

    #!Take back like
    def take_back_like_post_helper(self,tx,post_id,profile_id):
        query = (
            "MATCH (post:Post) WHERE ID(post)=$post_id MATCH (profile:Profile) WHERE profile.profile_id=$profile_id " 
            "MATCH (profile) -[r:Liked]-> (post) SET post.like_count=post.like_count - 1 DELETE r RETURN post"
        )
        result = tx.run(query,post_id=post_id,profile_id=profile_id)
        
        try:
            return ([row.data()
                for row in result])
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
            query=query, exception=exception))
            raise

    def take_back_like_post(self,post_id,profile_id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.take_back_like_post_helper,post_id=post_id,profile_id=profile_id)
            output = self.serialize_post(result[0])
            return output



    #!Add a news
    def add_news_helper(self, tx, image, profile_id, description, title):
        query = (
            "MATCH (profile:Profile {profile_id:$profile_id}) CREATE (news:News {title:$title,description:$description, image:$image, profile_id:$profile_id, create:TIMESTAMP(), edit:TIMESTAMP()}) CREATE (profile) -[:Published]-> (news) RETURN news"
        )
        result = tx.run(query, description=description, profile_id=profile_id,image=image,title=title)
        
        try:
                return ([row.data()
                    for row in result])
        except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
                raise
        
    def add_news(self, image, profile_id, description, title):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.execute_write(
                self.add_news_helper, image, profile_id, description, title)
            output = (self.serialize_news(result[0]))
            return output

    #!Get a news
    def get_news_helper(self, tx, id):
        query = (
            "MATCH (news:News) WHERE ID(news)=$id RETURN news"
        )
        result = tx.run(query, id=id)
        
        try:
                return ([row.data()
                    for row in result])
        except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
                raise
      
    def get_news(self, id):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.execute_write(
                self.get_news_helper, id)
            if len(result)==0:
                return "E"
            output = (self.serialize_news(result[0]))
            return output

    #!Delete a news  
    def delete_news_helper(self, tx, id):
        query = (
            "MATCH (news:News) WHERE ID(news)=$id DETACH DELETE news"
        )
        result = tx.run(query, id=id)
        
        try:
                return ([row.data()
                    for row in result])
        except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
                raise
        
    def delete_news(self, id):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.execute_write(
                self.delete_news_helper, id)
            return result

    #!Update a news  
    def update_news_helper(self, tx, image, id, title, description,delete):
        if delete==True:
            query=(
                "MATCH (news:News) "
                "WHERE ID(news)=$id "
                "SET news.edit=TIMESTAMP() "
                "SET news.title=$title "
                "SET news.description=$description "
                "SET news.image='' "
                "RETURN news"
            )
        else:
            query = (
                "MATCH (news:News) "
                "WHERE ID(news)=$id "
                "SET news.edit=TIMESTAMP() "
                "SET news.title=$title "
                "SET news.description=$description "
                "SET news.image=$image "
                "RETURN news"
            )
        result = tx.run(query, id=id,title=title,description=description,image=image,delete=delete)
        
        try:
                return ([row.data()
                    for row in result])
        except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
                raise
        
    def update_news(self, image, id, title, description,delete):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.update_news_helper,image,id,title,description,delete)
            output = self.serialize_news(result[0])
            return output

    #!Get a comment
    def get_comment_helper(self,tx,comment_id):
        query = (
            "MATCH (comment:Comment) WHERE ID(comment)=$comment_id "
            "RETURN comment"
        )
        result = tx.run(query,comment_id=comment_id)
        
        try:
                return ([row.data()
                    for row in result])
        except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
                raise
        
    def get_comment(self,comment_id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.get_comment_helper,comment_id=comment_id)
            if len(result)==0:
                return "E"
            output = self.serialize_comment(result[0])
            return output

    #!Comment on post
    def post_comment_helper(self,tx,post_id,profile_id,text):
        query = (
            "MATCH (post:Post) WHERE ID(post)=$post_id "
            "MATCH (profile:Profile {profile_id:$profile_id}) "
            "CREATE (comment:Comment {text:$text, profile_id:$profile_id,create:TIMESTAMP()}) "
            "CREATE (profile) -[:Commented]-> (comment) "
            "CREATE (comment) -[:Answered]-> (post)"
            "SET post.comment_count=post.comment_count + 1 "
            "RETURN comment"
        )
        result = tx.run(query,post_id=post_id,profile_id=profile_id,text=text)
        
        try:
                return ([row.data()
                    for row in result])
        except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
                raise
        
    def post_comment(self, post_id, profile_id,text):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.post_comment_helper,post_id=post_id,profile_id=profile_id,text=text)
            output = self.serialize_comment(result[0])
            return output

    #!Delete a comment
    def delete_comment_helper(self,tx,comment_id,profile_id):
        query = (
            "MATCH (comment:Comment) WHERE ID(comment)=$comment_id "
            "MATCH (comment) -[:Answered]-> (post:Post) "
            "SET post.comment_count = post.comment_count - 1 "
            "DETACH DELETE comment"
        )
        result = tx.run(query,comment_id=comment_id,profile_id=profile_id)
        
        try:
                return ([row.data()
                    for row in result])
        except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
                raise
        
    def delete_comment(self,comment_id,profile_id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.delete_comment_helper,comment_id=comment_id,profile_id=profile_id)
            return result

    #!Check if muted
    def check_mute_profile_helper(self,tx,profile_id,mute_id):
        query = (
            "MATCH (profile:Profile {profile_id:$profile_id}) "
            "MATCH (mute:Profile {profile_id:$mute_id}) "
            "RETURN EXISTS ((profile)-[:Muted]->(mute))"
        )
        result = tx.run(query,mute_id=mute_id,profile_id=profile_id)
        
        try:
            return ([row.data()
                for row in result])
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
            query=query, exception=exception))
            raise
        
    def check_mute_profile(self,profile_id,mute_id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.check_mute_profile_helper,mute_id=mute_id,profile_id=profile_id)
            dp=result[0]
            dp_values = dp.values()
            state = False
            for i in dp_values:
                state=i
            return state

    #!Dont mute a profile
    def dont_mute_profile_helper(self,tx,profile_id,mute_id):
        query = (
            "MATCH (profile:Profile {profile_id:$profile_id}) "
            "MATCH (mute:Profile {profile_id:$mute_id}) "
            "MATCH (profile)-[r:Muted]->(mute) "
            "DELETE r"
        )
        result = tx.run(query,mute_id=mute_id,profile_id=profile_id)
        
        try:
            return ([row.data()
                for row in result])
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
            query=query, exception=exception))
            raise
        
    def dont_mute_profile(self,profile_id,mute_id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.dont_mute_profile_helper,mute_id=mute_id,profile_id=profile_id)
            
            return result

    #!Mute a profile
    def mute_profile_helper(self,tx,profile_id,mute_id):
        query = (
            "MATCH (profile:Profile {profile_id:$profile_id}) "
            "MATCH (mute:Profile {profile_id:$mute_id}) "
            "CREATE (profile)-[:Muted]->(mute)"
        )
        result = tx.run(query,mute_id=mute_id,profile_id=profile_id)
        
        try:
            return ([row.data()
                for row in result])
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
            query=query, exception=exception))
            raise
        
    def mute_profile(self,profile_id,mute_id):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self.mute_profile_helper,mute_id=mute_id,profile_id=profile_id)
            return result

#? Inıtalizing the database
app = App(os.getenv('URI'),os.getenv('USER'),os.getenv('PASSWORD'))

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_authenticated'] = user.is_authenticated
        token['is_superuser'] = user.is_superuser

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def Routes(request):
    routes = [
        '/rest-auth/google/',
        '/auth/login',
        '/auth/logout',
        '/auth/user',
        '/auth/password/change',
        '/auth/password/reset',
        '/auth/password/reset/confirm',
        '/register',
        '/login/',
        '/profile/:id',
        '/profile/add',
        '/profile/update',
        '/post/add',
        '/post/:id',
        '/post/:id/update',
        '/post/:id/delete',
    ]
    
    return Response(routes)

@api_view(['POST']) 
def Register(request):
    form = UserCreationForm()
    if request.data:
        mails = [i.email for i in User.objects.all()]
        if request.data.get('email') in mails:
            return Response({"msg_en":"This email already in use. 😢","msg_tr":"Girdiğiniz email kullanımda. 😢"},status=400)
        form = forms.SignupForm(request.data)
        if form.is_valid():
            user = form.save()
            data = {"user":user}
            formprofile = forms.ProfileForm(data)
            if formprofile.is_valid():
                profile = formprofile.save()
                app.add_profile(profile.id,profile.user.username)
                return Response({"msg_en":"Successfully registered. ✨","msg_tr":"Başarıyla kayıt olundu. ✨"},status=200)
            else:
                user.delete()
                return Response({"msg_en":"An error occured. 🤔","msg_tr":"Bir hata oluştu. 🤔"},status=400)
        else:
            print(form.errors)
            return Response({"msg_en":"Data is not valid. 🤨","msg_tr":"Veri doğru değil. 🤨"},status=400)
    else:
        return Response({"msg_en":"There was no data entered. 😒","msg_tr":"Bize veri verilmedi. 😒"},status=400)



#! POST CRUD
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def AddPost(request):
    if request.data:
        profile = models.Profile.objects.filter(user=request.user)
        if len(profile)>0:
            profile=profile[0]
        else:
            return Response({"msg_en":"Couldnt find the profile. 🥲","msg_tr":"Profil bulunamadı. 🥲"},status=400)
        upload = request.FILES.get('upload')
        if upload!=None:
            fss = FileSystemStorage()
            file = fss.save("posts"+"/"+upload.name, upload)
            file_url = fss.url(file)
            post_data = (app.add_post(file=file_url,text=request.data.get('text'),profile_id=profile.id))
        else:
            post_data = (app.add_post(file="",text=request.data.get('text'),profile_id=profile.id))
        app.close()
        return Response({"data":post_data},status=200)
    else:
        return Response({"msg_en":"There was no data entered. 😒","msg_tr":"Bize veri verilmedi. 😒"},status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def GetPost(request,id):
    result = app.get_post(id=id)
    app.close()
    if result=="E":
        return Response({"msg_tr":"Gönderi bulunamadı. 😒","msg_en":"Post not fonund. 😒"},status=400)
    return Response({"msg_en":"Got the post successfully. ✨","msg_tr":"Gönderi başarıyla alındı. ✨","data":result},status=200)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def DeletePost(request,id):
    post = app.get_post(id=id)
    if post=="E":
        return Response({"msg_tr":"Gönderi bulunamadı. 😒","msg_en":"Post not fonund. 😒"},status=400)
    if request.user.id==post.get('profile').get('user').get('id'):
        result = app.delete_post(id=id)
        app.close()
        return Response({"msg_en":"Successfully deleted the post. 👽","msg_tr":"Gönderi başarıyla silindi. 👽"},status=200)
    else:
        return Response({"msg_en":"Users dont match. 😒","msg_tr":"Kullanıcı uyuşmuyor. 😒"},status=400)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def UpdatePost(request,id):
    post = app.get_post(id=id)
    if post=="E":
        return Response({"msg_tr":"Gönderi bulunamadı. 😒","msg_en":"Post not fonund. 😒"},status=400)
    if request.user.id==post.get('profile').get('user').get('id'):
        if request.data:
            if request.data.get('delete')=='true':
                post_data = app.update_post(id=id,file='',text=request.data.get('text'),delete=True)
            else:
                upload = request.FILES.get('upload')
                if upload!=None:
                    fss = FileSystemStorage()
                    file = fss.save("posts"+"/"+upload.name, upload)
                    file_url = fss.url(file)
                    post_data = app.update_post(id=id,file=file_url,text=request.data.get('text'),delete=False)
                else:
                    post_data = app.update_post(id=id,file='',text=request.data.get('text'),delete=False)
            return Response({"msg_en":"Successfully updated the post. 🚀","msg_tr":"Gönderi başarıyla güncellendi. 🚀","data":post_data},status=200)
        else:
            return Response({"msg_en":"There is no data to update. 😒","msg_tr":"Güncelleyecek veri vermediniz. 😒"},status=400)
    else:
        return Response({"msg_en":"Users dont match. 😒","msg_tr":"Kullanıcı uyuşmuyor. 😒"},status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def FilterPostText(request):
    post = app.filter_post_text(text=request.GET.get('text'))
    app.close()
    return Response({"data":post},status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def MostLikedPost(request):
    result = app.most_liked_post()
    if result == "E":
        return Response({"msg_en":"There is no data 🤨","msg_tr":"Veri yok. 🤨"},status=200)
    return Response({"data":result},status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def MostCommentedPost(request):
    result = app.most_commented_post()
    if result == "E":
        return Response({"msg_en":"There is no data 🤨","msg_tr":"Veri yok. 🤨"},status=200)
    return Response({"data":result},status=200)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ToggleLikePost(request,post_id):
    profile = models.Profile.objects.filter(user=request.user)
    if len(profile)>0:
        profile=profile[0]
    else:
        return Response({"msg_en":"Couldnt find the profile. 🥲","msg_tr":"Profil bulunamadı. 🥲"},status=400)
    state = app.check_if_liked_post(post_id,profile.id)
    if state == False:
        result = app.like_a_post(post_id,profile.id)
        app.close()
        return Response({"msg_en":"Successfully liked the post. 😄","msg_tr":"Gönderi başarıyla beğenildi. 😄","data":result},status=200)
    else:
        result = app.take_back_like_post(post_id,profile.id)
        app.close()
        return Response({"msg_en":"Successfully took your like back. 😄","msg_tr":"Beğenin başarıyla geri çekildi. 😄","data":result},status=200)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def AnswerPost(request,post_id):
    profile = models.Profile.objects.filter(user=request.user)
    if len(profile)>0:
        profile=profile[0]
    else:
        return Response({"msg_en":"Couldnt find the profile. 🥲","msg_tr":"Profil bulunamadı. 🥲"},status=400)
    if request.data.get('text')!=None and len(request.data.get('text'))>4:
        result = app.post_comment(post_id=post_id,profile_id=profile.id,text=request.data.get('text'))
        app.close()
        return Response({"msg_en":"Successfully commented. 🌝","msg_tr":"Başarıyla yorum yapıldı. 🌝","data":result},status=200)
    else:
        return Response({"msg_en":"Data is not valid. 🤨","msg_tr":"Veri doğru değil. 🤨"},status=400)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def DeleteAnswer(request,comment_id):
    """Cevabın silinmesini sağlar, comment_id parametresini alır."""
    profile = models.Profile.objects.filter(user=request.user)
    if len(profile)>0:
        profile=profile[0]
    else:
        return Response({"msg_en":"Couldnt find the profile. 🥲","msg_tr":"Profil bulunamadı. 🥲"},status=400)
    comment = app.get_comment(comment_id=comment_id)
    if comment=="E":
        return Response({"msg_en":"Couldnt find the comment. 🫥","msg_tr":"Yorum bulunamadı. 🫥"},status=400)
    id = comment.get('profile').get('id')
    print(profile.id,id)
    if id==profile.id:
        app.delete_comment(comment_id=comment_id,profile_id=profile.id)
        app.close()
        return Response({"msg_en":"Successfully deleted comment. 🌝","msg_tr":"Yorum başarıyla silindi. 🌝"},status=200)
    else:
        return Response({"msg_en":"Users dont mach. 🥲","msg_tr":"Kullanıcılar uyuşmuyor. 🥲"},status=400)


#! PROFILE CRUD
@api_view(['POST']) 
def GoogleAddOrGetProfile(request,id):
    """Profil ekler, user verisini alır."""
    if request.data:
        user = User.objects.get(id = request.data.get('user'))
        profile = models.Profile.objects.filter(user=user)
        if len(profile)>0:
            serializer = serializers.ProfileSerializer(profile[0],many=False)
            return Response({"data":serializer.data},status=200)
        form = forms.ProfileForm(request.data)
        if form.is_valid():
            profile = form.save()
            app.add_profile(username=profile.user.username,profile_id=profile.id)
            app.close()
            serializer = serializers.ProfileSerializer(profile,many=False)
            return Response({"data":serializer.data},status=200)
        else:
            return Response({"msg_en":"Data is not valid. 😥","msg_tr":"Veri doğru değil. 😥"},status=400)
    else:
        return Response({"msg_en":"There was no data entered. 😒","msg_tr":"Bize veri verilmedi. 😒"},status=400)

@api_view(['POST']) 
def AddProfile(request):
    """Profil ekler, user verisini alır."""
    if request.data:
        user = User.objects.get(id = request.data.get('user'))
        profile = models.Profile.objects.filter(user=user)
        if len(profile)>0:
            serializer = serializers.ProfileSerializer(profile[0],many=False)
            return Response(jwt.encode(serializer.data, "secret", algorithm="HS256"),status=200)
        form = forms.ProfileForm(request.data)
        if form.is_valid():
            profile = form.save()
            serializer = serializers.ProfileSerializer(profile,many=False)
            return Response(jwt.encode(serializer.data, "secret", algorithm="HS256"),status=200)
        else:
            return Response({"msg_en":"Data is not valid. 😥","msg_tr":"Veri doğru değil. 😥"},status=400)
    else:
        return Response({"msg_en":"There was no data entered. 😒","msg_tr":"Bize veri verilmedi. 😒"},status=400)

@api_view(['PUT'])    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def UpdateProfile(request):
    """
        Profili günceller bio, profilePhoto verilerini alır.
    """
    profile = get_object_or_404(models.Profile, id=request.user.id)
    if request.data:
        if request.data.get('bio'):
            profile.bio = request.data.get('bio')
        if 'profilePhoto' in request.FILES:
            profile.profilePhoto = request.FILES['profilePhoto']
        profile.save()
        data = serializers.ProfileSerializer(profile,many=False)
        return Response({"msg_en":"Successfully updated profile. 🚀","msg_tr":"Profil başarıyla güncellendi. 🚀","data":data.data},status=200)
    else:
        return Response({"msg_en":"There was no data entered. 😒","msg_tr":"Bize veri verilmedi. 😒"},status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def GetProfile(request,id):
    """
        Profili getirir, userın idsini alır.
    """
    profile = models.Profile.objects.filter(user=User.objects.get(id=id))
    if len(profile)>0:
        data = serializers.ProfileSerializer(profile[0],many=False)
        return Response({"data":data.data},status=200)
    else:
        return Response({"msg_en":"Couldnt find the profile. 🥲","msg_tr":"Profil bulunamadı. 🥲"},status=400)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ToogleProfileFollow(request,follow_id):
    """
        Bir profili takip eder/takipten çıkar, takip edilen kişinin idsi follow_id olarak parametre alınır. 
    """
    profile = models.Profile.objects.filter(user=request.user)
    if len(profile)>0:
        profile=profile[0]
    else:
        return Response({"msg_en":"Couldnt find the profile. 🥲","msg_tr":"Profil bulunamadı. 🥲"},status=400)
    follow = models.Profile.objects.filter(id=follow_id)
    if len(follow)>0:
        follow=follow[0]
    else:
        return Response({"msg_en":"Couldnt find the profile. 🥲","msg_tr":"Profil bulunamadı. 🥲"},status=400)
    if app.is_following_profile(profile.id,follow.id)==True:
        app.unfollow_profile(profile.id,follow.id)
        app.close()
        return Response({"msg_en":"Successfully unfollowed. 🚀","msg_tr":"Başarıyla takipten çıkıldı. 🚀"},status=200)
    else:
        app.follow_profile(profile.id,follow.id)
        app.close()
        return Response({"msg_en":"Successfully followed. 🚀","msg_tr":"Başarıyla takip edildi. 🚀"},status=200)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def MuteProfile(request,mute_id):
    """Bir kişinin sessize alınmasını sağlar, mute_id parametresini alır."""
    profile = models.Profile.objects.filter(user=request.user)
    if len(profile)>0:
        profile=profile[0]
    else:
        return Response({"msg_en":"Couldnt find the profile. 🥲","msg_tr":"Profil bulunamadı. 🥲"},status=400)
    mute = models.Profile.objects.filter(id=mute_id)
    if len(mute)>0:
        mute=mute[0]
    else:
        return Response({"msg_en":"Couldnt find the profile. 🥲","msg_tr":"Profil bulunamadı. 🥲"},status=400)
    state = app.check_mute_profile(profile_id=profile.id,mute_id=mute.id)
    print(state)
    if state==True:
        app.dont_mute_profile(profile_id=profile.id,mute_id=mute.id)
        app.close()
        return Response({"msg_en":"Successfully non-muted "+mute.user.username+". 😄","msg_tr":mute.user.username+" sessizliği başarıyla kaldırıldı. 😄"},status=200)
    else:    
        app.mute_profile(profile_id=profile.id,mute_id=mute.id)
        app.close()
        return Response({"msg_en":"Successfully muted "+mute.user.username+". 😄","msg_tr":mute.user.username+" başarıyla sessize alındı. 😄"},status=200)



#! NEWS CRUD
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def AddNews(request):
    """Haber eklenmesini sağlar, upload, description, title verilerini alır."""
    profile = models.Profile.objects.filter(user=request.user)
    if len(profile)>0:
        profile=profile[0]
    else:
        return Response({"msg_en":"Couldnt find the profile. 🥲","msg_tr":"Profil bulunamadı. 🥲"},status=400)
    
    if request.data:
        if request.FILES.get('upload')!=None:
            upload = request.FILES.get('upload')
            fss = FileSystemStorage()
            file = fss.save("news"+"/"+upload.name, upload)
            file_url = fss.url(file)
            result = app.add_news(image=file_url,profile_id=profile.id,description=request.data.get('description'),title=request.data.get('title'))
        else:
            result = app.add_news(image="",profile_id=profile.id,description=request.data.get('description'),title=request.data.get('title'))
        return Response({"msg_en":"Successfully added news. 🚀","msg_tr":"Haber başarıyla eklendi. 🚀","data":result},status=200)
    else:
        return Response({"msg_en":"There was no data entered. 😒","msg_tr":"Bize veri verilmedi. 😒"},status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def GetNews(request,id):
    """Haber getirilmesini sağlar, haberin idsini parametre alır."""
    result = app.get_news(id)
    if result=="E":
        return Response({"msg_en":"Couldnt find the news. 😶","msg_tr":"Haber bulunamadı. 😶"},status=400)
    return Response({"data":result},status=200)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def DeleteNews(request,id):
    """Haber silinmesini sağlar, haberin idsini parametre alır."""
    result = app.get_news(id)
    if result!="E":
        if result.get('profile').get('user').get('id')!=request.user.id:
            return Response({"msg_tr":"Bunu silmek için yetkiniz yok. 😥","msg_en":"You are not allowed to delete this news. 😥"},status=400)
        else:
            result = app.delete_news(id)
            return Response({"msg_en":"Successfully deleted the news. ✨","msg_tr":"Haber başarıyla silindi. ✨"},status=200)
    else:
        return Response({"msg_en":"Couldnt find the news. 😶","msg_tr":"Haber bulunamadı. 😶"},status=400)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def UpdateNews(request,id):
    """Haberin güncellenmesini sağlar, delete, title, description verilerini alır."""
    result = app.get_news(id)
    if result!="E":
        if result.get('profile').get('user').get('id')!=request.user.id:
            return Response({"msg_tr":"Bunu güncellemek için yetkiniz yok. 😥","msg_en":"You are not allowed to update this news. 😥"},status=400)
        else:
            if request.data:
                if request.data.get('delete')=='true':
                    result = app.update_news('',id,request.data.get('title'),request.data.get('description'),True)
                else:
                    upload = request.FILES.get('upload')
                    if upload!=None:
                        fss = FileSystemStorage()
                        file = fss.save("news"+"/"+upload.name, upload)
                        file_url = fss.url(file)
                        result = app.update_news(file_url,id,request.data.get('title'),request.data.get('description'),False)
                    else:
                        result = app.update_news('',id,request.data.get('title'),request.data.get('description'),False)
                
                return Response({"msg_en":"Successfully updated the news. ✨","msg_tr":"Haber başarıyla güncellendi. ✨","data":result},status=200)
            else:
                return Response({"msg_en":"No data was given. 🫥","msg_tr":"Bize veri verilmedi. 🫥"},status=400)
    else:
        return Response({"msg_en":"Couldnt find the news. 😶","msg_tr":"Haber bulunamadı. 😶"},status=400)

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:5173/login"
    client_class = OAuth2Client