from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "college",
            "branch",
            "year",
            "bio",
            "skills",
        ]

        widgets = {
            "college": forms.TextInput(
                attrs={"placeholder": "Enter your college"}
            ),

            "branch": forms.TextInput(
                attrs={"placeholder": "Example: ECE"}
            ),

            "year": forms.TextInput(
                attrs={"placeholder": "Example: 2nd Year"}
            ),

            "bio": forms.Textarea(
                attrs={
                    "placeholder": "Tell us about yourself",
                    "rows": 4
                }
            ),

            "skills": forms.CheckboxSelectMultiple(
    choices=[
        # Programming Languages
        ("Python", "Python"),
        ("C", "C"),
        ("C++", "C++"),
        ("Java", "Java"),
        ("JavaScript", "JavaScript"),
        ("TypeScript", "TypeScript"),
        ("CSharp", "C#"),
        ("Go", "Go"),
        ("Rust", "Rust"),
        ("PHP", "PHP"),

        # Web Development
        ("HTML", "HTML"),
        ("CSS", "CSS"),
        ("React", "React"),
        ("NodeJS", "Node.js"),
        ("Django", "Django"),
        ("Flask", "Flask"),
        ("Bootstrap", "Bootstrap"),
        ("Tailwind", "Tailwind CSS"),

        # Database
        ("SQL", "SQL"),
        ("MySQL", "MySQL"),
        ("PostgreSQL", "PostgreSQL"),
        ("MongoDB", "MongoDB"),
        ("Firebase", "Firebase"),

        # AI / ML
        ("MachineLearning", "Machine Learning"),
        ("DeepLearning", "Deep Learning"),
        ("ArtificialIntelligence", "Artificial Intelligence"),
        ("DataScience", "Data Science"),
        ("ComputerVision", "Computer Vision"),
        ("NLP", "Natural Language Processing"),

        # Hardware / Embedded
        ("Arduino", "Arduino"),
        ("ESP32", "ESP32"),
        ("ESP8266", "ESP8266"),
        ("STM32", "STM32"),
        ("RaspberryPi", "Raspberry Pi"),
        ("IoT", "IoT"),
        ("EmbeddedSystems", "Embedded Systems"),
        ("PCBDesign", "PCB Design"),

        # Tools
        ("Git", "Git"),
        ("GitHub", "GitHub"),
        ("Docker", "Docker"),
        ("Linux", "Linux"),
        ("VSCode", "VS Code"),

        # Other
        ("CyberSecurity", "Cybersecurity"),
        ("CloudComputing", "Cloud Computing"),
        ("UIUX", "UI/UX Design"),
        ("Figma", "Figma"),
        ("Networking", "Computer Networking"),
        ("APIs", "API Development"),
        ("ProblemSolving", "Problem Solving"),
    ]
),
        }