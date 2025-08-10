from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
# Create your models here.

class UserEx(User):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=15, blank=True,null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, default='profile_images/profile.png')
    is_verified = models.BooleanField(default=False)
    status=models.CharField(max_length=150,null=True,blank=True , default='None')

class Group(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groups_created')
    members = models.ManyToManyField(User, through='GroupMember', related_name='group_memberships')  # Changed related_name
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"

class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    media = models.FileField(upload_to='group_media/', blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender.username} in {self.group.name} at {self.sent_at}"

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='private_messages_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='private_messages_received')
    content = models.TextField()
    media = models.FileField(upload_to='private_media/', blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    encrypted = models.BooleanField(default=True)  # For end-to-end encryption

    def __str__(self):
        return f"Private message from {self.sender.username} to {self.receiver.username} at {self.sent_at}"

class Call(models.Model):
    CALL_TYPE_CHOICES = [
        ('voice', 'Voice'),
        ('video', 'Video'),
    ]
    call_type = models.CharField(max_length=5, choices=CALL_TYPE_CHOICES)
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calls_made')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calls_received')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None
    def __str__(self):
        return f"{self.call_type.capitalize()} call from {self.caller.username} to {self.receiver.username} at {self.start_time}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

class Media(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media uploaded by {self.user.username} at {self.created_at}"


class FriendRequest(models.Model):
    from_user = models.ForeignKey(UserEx, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserEx, related_name='received_requests', on_delete=models.CASCADE)
    request_status = models.CharField(max_length=10, choices=(
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({self.request_status})"