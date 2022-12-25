from app import create_app

if __name__ == '__main__': 
    create_app(config_name='dev').run()