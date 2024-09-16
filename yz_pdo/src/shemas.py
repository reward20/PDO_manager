from pydantic import (
    BaseModel,
    Field,
    PositiveInt
)

class PartValidate(BaseModel):
    master_name: str = Field(max_length=32)
    slave_name: str = Field(max_length=32)
    count: PositiveInt

class DetailValidate(BaseModel):
    name_part: str = Field(max_length=32)
    name_detail: str = Field(max_length=128)
    count: PositiveInt

class TableValidate(BaseModel):
    name_part: str = Field(max_length=32)
    name_table: str = Field(max_length=32)
    count: PositiveInt
