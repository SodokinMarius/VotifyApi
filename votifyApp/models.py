from django.db import models

from django.conf import settings

from django.utils import timezone

from utils.enums import (
ProgressChoiceEnum, 
TypeVoterEnum,    
NotificationTypeEnum,
TypeElectionEnum,    

)


class Voter(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)  
    voter_type = models.CharField(max_length=100,choices=TypeVoterEnum.items(),default=TypeVoterEnum.CITIZEN.value)
    
    def __str__(self):
        return f'{self.user} de type : {self.voter_type}'

class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(verbose_name="description",max_length=500)
    date_start = models.DateTimeField(null=False, default=timezone.now)
    date_end = models.DateTimeField(null=False, auto_now=False) 
    turn_number = models.IntegerField(default=1)
    progress_status = models.CharField(choices=ProgressChoiceEnum.items(),max_length=200,default=ProgressChoiceEnum.PENDING.value)
    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True) 
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.title
    
    
    def save(self, *args, **kwargs):
        current_time = timezone.now()
        notif_type = ""
        message = ""
      
        """
        Si le vote est crée aujourd'hui et sa date de demarrage est dans le futur, alors c'est mis en pending
        """
        if current_time < self.date_start and self.created_at == current_time:
            self.progress_status = ProgressChoiceEnum.PENDING.value
            notif_type == NotificationTypeEnum.NEW_VOTE.value
            message  =  f" Titre :  {self.title}  \n Organisateur : {self.creator}  \n Date De démarrage : {self.date_start} \n Date de Fin : {self.date_end} \n Acceder à votre Dashboard pour plus de details."
               
        elif self.date_start == current_time :
            self.progress_status = ProgressChoiceEnum.IN_PROGESS.value
            notif_type == NotificationTypeEnum.RAPPEL
            message  =  f" Titre :  {self.title}  \n Organisateur : {self.creator}  \n Date De démarrage : {self.date_start} \n Date de Fin : {self.date_end} \n Acceder à votre Dashboard pour voter."
               
        super(Election, self).save(*args, **kwargs)


class PrivateElection(Election):
    authorized_voters_file = models.FileField(null=True)  
    voters_email = models.JSONField(verbose_name="Mail des Voters",null=True)
 
class Option(models.Model):
    code = models.CharField(max_length=100,null=False,unique=True)
    full_name = models.CharField(max_length=500)
    image = models.ImageField(upload_to="options_images",default="static/images/default_option.jpg")
    vote_counter = models.IntegerField(null=True)
    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    related_election = models.ForeignKey(to=Election,on_delete=models.CASCADE,null=False,related_name="options")

    def __str__(self):
        return  self.code
       

class Vote(models.Model):
    voter = models.ForeignKey(to=Voter,on_delete=models.SET_NULL,null=True)
    election = models.ForeignKey(to=Election,on_delete=models.SET_NULL,null=True)
    choosed_option = models.ForeignKey(to=Option,on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f' Voter :{self.voter} | Election : {self.election} | choosed : {self.choosed_option}'
    
  
class Notification(models.Model):
    notif_type =  models.CharField(max_length=500,choices=NotificationTypeEnum.items())
    notif_content = models.TextField(max_length=1000)
    notif_read_status = models.BooleanField(default=False)
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.notif_type}'
    
class VoteAdminRequest(models.Model) :
    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    subject = models.CharField(max_length=500)
    message = models.TextField(max_length=1000)    
    creator_identity_piece = models.ImageField(upload_to="identity_pieces",default="static/images/default_piece.jpg")
    is_validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    
    def __str__(self):
        return f'{self.user.email} => {self.subject}'

