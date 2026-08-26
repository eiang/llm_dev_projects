skills = ["Java","Python","JavaScript","Spring Boot","Docker"]

def normalize_skills(skills: list[str]) -> list[str]:
    return [skill.strip().lower() for skill in skills]


normalized_skills = normalize_skills(skills)
print(normalized_skills)
