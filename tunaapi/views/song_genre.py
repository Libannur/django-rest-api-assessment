"""View module for handling requests about songGenre types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import SongGenre, Song, Genre


class SongGenreView(ViewSet):
    """Tuna Piano songGenre types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single songGenre type
        
        Returns:
            Response -- JSON serialized songGenre type
        """
        try:
            songGenre = SongGenre.objects.get(pk=pk)
            serializer = SongGenreSerializer(songGenre)
            return Response(serializer.data)
        except SongGenre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all songGenre types

        Returns:
            Response -- JSON serialized list of songGenre types
        """
        songGenres = SongGenre.objects.all()
    
        serializer = SongGenreSerializer(songGenres, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized songGenre instance
        """
        songId = Song.objects.get(pk=request.data["song_id"])
        genreId = Genre.objects.get(pk=request.data["genre_id"])

        songGenre = SongGenre.objects.create(
            song_id= request.data["song_id"],
            genre_id= request.data["genre_id"],
        )
        serializer = SongGenreSerializer(songGenre)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a songGenre

        Returns:
            Response -- Empty body with 204 status code
        """
        songId = Song.objects.get(pk=request.data["song"])
        genreId = Genre.objects.get(pk=request.data["genre"])
        
        songGenre = SongGenre.objects.get(pk=pk)
        songGenre.song_id = songId
        songGenre.genre_id = genreId

        songGenre.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        songGenre = SongGenre.objects.get(pk=pk)
        songGenre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
            


class SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for songGenre types
    """
    class Meta:
        model = SongGenre
        fields = ('id', 'song', 'genre' )
        depth = 1