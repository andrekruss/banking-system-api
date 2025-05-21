from pydantic import BaseModel

class CreateUserDTO(BaseModel):
    name: str
    cpf: str
    telephone: str
    email: str
    password: str

class UserDTO(BaseModel):
    id: str
    name: str
    telephone: str
    email: str
    created_at: str

class UserLoginDTO(BaseModel):
    email: str
    password_hash: str