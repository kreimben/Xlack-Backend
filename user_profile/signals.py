from allauth.socialaccount.models import SocialLogin, SocialAccount
from allauth.socialaccount.signals import social_account_added, social_account_updated, social_account_removed
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver

from user_profile.models import UserProfile


@receiver(social_account_added)
def added(request, sociallogin: SocialLogin, **kwargs):
    print('\nadded')
    __fetch_user_data(sociallogin)


@receiver(social_account_updated)
def updated(request, sociallogin: SocialLogin, **kwargs):
    print('\nupdated')
    __fetch_user_data(sociallogin)


@receiver(social_account_removed)
def deleted(request, socialaccount, **kwargs):
    # TODO: Check this functions works in real. (I can't check this in runtime.)
    print('\ndeleted')
    print(f'socialaccount: {socialaccount}')
    print(f'kwargs: {kwargs}')
    UserProfile.objects.filter(user=socialaccount.user).delete()


def __fetch_user_data(sociallogin):
    data = SocialAccount.objects.get(user=sociallogin.user).extra_data
    try:
        profile = UserProfile.objects.get(user=sociallogin.user)

        profile.github_id = data['id']
        profile.bio = data['bio']
        profile.thumbnail_url = data['avatar_url']

        profile.save()
        print(f'profile: {profile}')
    except ObjectDoesNotExist:
        profile = UserProfile.objects.create(
            user=sociallogin.user,
            github_id=data['id'],
            bio=data['bio'],
            thumbnail_url=data['avatar_url']
        )

        profile.save()
        print(f'profile: {profile}')
