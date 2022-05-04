from decouple import AutoConfig
config = AutoConfig(search_path='..')

SECRET_KEY = config('SECRET_KEY')
MONGODB_HOST = config('MONGODB_HOST')