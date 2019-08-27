from rom.model import Model
import rom.columns as cols
from datetime import datetime

class BaseModel(Model):

    created_at = cols.DateTime(default=datetime.now)
    updated_at = cols.DateTime()
