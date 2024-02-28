class LogDTO:
    def __init__(self, id=None, content=None, batch=None):
        self.id = id
        self.content = content
        self.batch = batch

    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=json_data.get('id'),
            content=json_data.get('content'),
            batch=json_data.get('batch')
        )

    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'batch': self.batch
        }