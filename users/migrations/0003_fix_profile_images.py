from django.db import migrations

def fix_images(apps, schema_editor):
    Profile = apps.get_model('users', 'Profile')
    default_url = 'https://res.cloudinary.com/dbdqfgqti/image/upload/v1751310469/default_oygkle.jpg'

    for profile in Profile.objects.all():
        if str(profile.image).startswith('media/') or str(profile.image).startswith('/media/'):
            profile.image = default_url
            profile.save()

class Migration(migrations.Migration):

    dependencies = [
        ('users', 'users/migrations/0002_alter_profile_image.py'),  # Replace with actual last migration
    ]

    operations = [
        migrations.RunPython(fix_images),
    ]
