from django.db import migrations


def create_defaults(apps, schema_editor):
    Profile = apps.get_model("portfolio", "Profile")
    Skill = apps.get_model("portfolio", "Skill")

    Profile.objects.get_or_create(
        full_name="Bichu Biju",
        defaults={
            "professional_title": "AI/ML Enthusiast",
            "introduction": "I’m a Computer Science Engineering student curious about artificial intelligence, machine learning, and the ideas that make technology useful in the real world.",
            "biography": "I’m pursuing Computer Science Engineering with a focus on Artificial Intelligence and Machine Learning. I enjoy learning how intelligent systems work and turning that knowledge into practical software.",
        },
    )

    skills = {
        "Programming": ["Python", "Java", "C", "C++"],
        "AI & data": ["Machine Learning", "Deep Learning", "Artificial Intelligence", "Data Science", "NLP"],
        "Web & tools": ["HTML", "CSS", "JavaScript", "Django", "Git & GitHub", "Jupyter"],
    }
    for category, names in skills.items():
        for order, name in enumerate(names):
            Skill.objects.get_or_create(name=name, category=category, defaults={"display_order": order})


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0001_initial")]
    operations = [migrations.RunPython(create_defaults, migrations.RunPython.noop)]
