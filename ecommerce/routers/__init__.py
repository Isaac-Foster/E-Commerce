import importlib
from pathlib import Path

from fastapi import APIRouter, FastAPI

from ecommerce.config import root_path


def configure_routes(app: FastAPI):
    path = Path(root_path)
    routers_path = root_path / "routers"

    notfound_routers = []

    async def load_routers(path: Path):
        paths = []

        if not path.exists():
            #print(f"Diretório não encontrado: {path}")
            return paths

        for item in path.iterdir():
            if item.is_file() and item.suffix == ".py":
                paths.append(item)
                continue

            if item.is_dir():
                new_paths = await load_routers(item)
                paths.extend(new_paths)

        return paths

    async def load_route(path: Path):
        module_name = path.relative_to(routers_path).with_suffix("").as_posix().replace("/", ".")

        try:
            router_module = importlib.import_module(f"ecommerce.routers.{module_name}")
            router_name = "router"

            if hasattr(router_module, router_name):
                router = getattr(router_module, router_name)
                if isinstance(router, APIRouter):
                    app.include_router(router, prefix="/api")
                else:
                    notfound_routers.append(f" -> {module_name}: 'router' não é APIRouter")
            else:
                pass
                #notfound_routers.append(f" -> {module_name}: 'router' não encontrado")

        except Exception as e:
            print(f"Erro ao importar {module_name}: {e}")


    async def initialize_routes():
        routes = await load_routers(routers_path)
        for route in routes:
            await load_route(route)

        if notfound_routers:
            pass
            #print(f"🚨 Erros ao carregar os routers: {''.join(notfound_routers)}")


    app.add_event_handler("startup", initialize_routes)
