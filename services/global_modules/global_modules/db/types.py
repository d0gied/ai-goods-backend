from sqlalchemy.types import String, TypeDecorator


class Embedding(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return ",".join([f"{value:.8f}" for value in value])

    def process_result_value(self, value, dialect):
        if value is not None:
            return [float(x) for x in value.split(",")]
