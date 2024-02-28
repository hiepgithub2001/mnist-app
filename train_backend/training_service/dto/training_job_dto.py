from typing import Optional
from pydantic import BaseModel

class ParamterDTO(BaseModel):
    batch_size: int
    test_batch_size: int
    epochs: int
    lr: float
    gamma: float
    no_cuda: bool
    no_mps: bool
    seed: int
    log_interval: int
    save_model: bool
    dry_run: bool
    drop_out: float

class SubmitTrainingJob(BaseModel):
    user_decoded_code: str
    paramter_id: int
    paramter: ParamterDTO