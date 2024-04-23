from uvicorn import run as run_uvicorn
from setup import node_type

def main():

    if node_type == "panel":
        from setup import (
            app_host as host,
            app_port as port,
            app_reload as reload,
            workers
        )
        run_uvicorn('web.web_app:app', host=host, port=port, reload=reload, workers=workers)
    else:
        pass


if __name__ == "__main__":
    main()
