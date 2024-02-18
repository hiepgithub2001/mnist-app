from typing import Optional
from pydantic import BaseModel

from dto.submit_parameter_req import HyperParametersDTO

class SubmitTrainingJob(BaseModel):
    user_code_encoded: str
    hyper_parameter : HyperParametersDTO