from pydantic import BaseModel, EmailStr

class OnboardingInput(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    team: str
    weekly_commitment: int
    tuition_fee: int
    monthly_fee: int
    start_date: str