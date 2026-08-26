skills = ["Java","Python","JavaScript","Spring Boot","Docker"]

# def normalize_skills(skills: list[str]) -> list[str]:
#     return [skill.strip().lower() for skill in skills]
# 列表推导式
def normalize_skills(skills: list[str]) -> list[str]:
    return list(skill.strip().lower() for skill in skills)

normalized_skills = normalize_skills(skills)
print(normalized_skills)
# Java 
# public class Job {
#     private String title;
#     private List<String> skills;
#     private Integer experience;
# }
# Python DTO
from pydantic import BaseModel
class Job(BaseModel):
    title: str
    skills: list[str]
    experience: int

job = Job(title="Software Engineer", skills=skills, experience=5)
print(job)



