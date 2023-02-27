from rest_framework import serializers

from .models import *
from authentication.models import User
from django.core.validators import FileExtensionValidator


class OptionSerializer(serializers.ModelSerializer):
    related_election = serializers.PrimaryKeyRelatedField(queryset=Election.objects.all(),required=True)
    image = serializers.ImageField(
        required=True,
        allow_empty_file=False,
        use_url=False,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])]
    )
    class Meta:
        model = Option
        fields = ['id','code','full_name','image','related_election','vote_counter','creator'] #related_election
        read_only_fields = ['id','creator','vote_counter']
        depth = 1
        
    def create(self, validated_data):
        image = validated_data.pop('image')
        option = Option.objects.create(**validated_data)
        option.image = image
        option.save()
        return option
       
class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ['id','user', 'voter_type']
        read_only_fields = ['id']

class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = ['id','title', 'description','date_start','date_end','turn_number','created_at']
        read_only_fields = ['id','created_at']
        depth = 1
        
class  PrivateElectionSerializer(serializers.ModelSerializer):
    
    authorized_voters_file = serializers.FileField(allow_null=True,required=True)

    class Meta:
        model = PrivateElection
        fields = ['id','title', 'description','authorized_voters_file','voters_email','date_start','date_end','turn_number','created_at']
        read_only_fields = ['id','created_at','voters_email']
        depth = 1
    
        
class VoteSerializer(serializers.ModelSerializer):
     class Meta:
        model = Vote
        fields = ['id','voter', 'election','choosed_option','created_at']
        read_only_fields = ['id','created_at']
        depth = 1

class VoteAdminRequestSerializer(serializers.ModelSerializer):
    creator_identity_piece = serializers.ImageField(
        required=True,
        allow_empty_file=False,
        use_url=False,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])]
    )
    class Meta:
        model = VoteAdminRequest
        fields = ['id','creator', 'subject','message','is_validated','created_at', 'creator_identity_piece']
        read_only_fields = ['id','creator','created_at','is_validated']
        depth = 1

    def create(self, validated_data):
        identity_piece = validated_data.pop('creator_identity_piece')
        vote_admin_request = VoteAdminRequest.objects.create(**validated_data)
        vote_admin_request.creator_identity_piece = identity_piece
        vote_admin_request.save()
        return vote_admin_request
        
        
class NotificationSerializer(serializers.ModelSerializer):
     class Meta:
        model = Notification
        fields = ['id','notif_type', 'notif_content','notif_read_status','sent_on']
        read_only_fields = ['id','sent_on']

    

    

