from pydantic import BaseModel

class TicketStatue(BaseModel):
 domain: str
 bug: str
 report:str