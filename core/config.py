from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str

    MYSQL_HOST: str 
    MYSQL_PORT: int 
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    @property
    def database_url(self):
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"


    class Config:
        env_file = '.env'
        extra = "ignore"