from importlib import util
from os import path
from glob import glob

from fastapi import APIRouter, Request
from typing import Optional

routers = []
for module_path in [
    f
    for f in glob(path.join(path.dirname(__file__), "**/*.py"), recursive=True)
    if path.basename(f) != "__init__.py"
]:
    spec = util.spec_from_file_location("", module_path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)

    router = getattr(module, "router", None)
    if router is not None:
        routers.append(router)

    if path.basename(module_path) != "api.py":
        for obj in dir(module):
            globals()[obj] = module.__dict__[obj]

router = APIRouter(tags=["slashless_forwarder"])


@router.post("/fwdr")
async def forward_slashless(
    request: Request,
    model: Optional[str] = None,
    f: Optional[str] = None,
    module: Optional[str] = None,
    method: Optional[str] = None,
):
    if f != None:
        module, method = f.split(".")

    # Try to look up the handler function
    func_name = f"{module}_{method}".lower()
    find_response = globals().get(func_name)

    if find_response is None:
        # Fallback: game-specific routing for modules with different naming
        try:
            game_code = model.split(":")[0]
            if game_code == "MDX" and module.startswith("eventlo"):
                find_response = globals().get(f"ddr_{module}_{method}")
            elif game_code == "REC":
                find_response = globals().get(f"drs_{module}_{method}")
            elif game_code == "KFC":
                if module == "eventlog":
                    find_response = globals().get(f"sdvx_{module}_{method}")
                else:
                    sdvx_ver = "".join(filter(str.isdigit, method))
                    find_response = globals().get(f"{module}_{"".join([i for i in method if not i.isdigit()])}")
                    if find_response:
                        return await find_response(sdvx_ver, request)
            elif game_code == "M32":
                if module == "lobby":
                    find_response = globals().get(f"gitadora_{module}_{method}")
                else:
                    gd_module = module.split("_")
                    find_response = globals().get(f"gitadora_{gd_module[-1]}_{method}")
                    if find_response:
                        return await find_response(gd_module[0], request)
        except Exception:
            pass

        if find_response is None:
            print("Try URL Slash 1 (On) if this game is supported.")
            return Response(status_code=404)

    return await find_response(request)


routers.append(router)
