from fastapi import APIRouter, Request, Response
from random import randint
from core_database import Query, where, Document

from core_common import core_process_request, core_prepare_response, E
from core_database import get_db
from modules.core.paseli import get_pin as paseli_get_pin, set_pin as paseli_set_pin

import config

router = APIRouter(prefix="/core", tags=["cardmng"])


GAME_ID_MAP = {
    "LDJ": "iidx_id",
    "MDX": "ddr_id",
    "KFC": "sdvx_id",
    "M32": "gitadora_id",
    "PAN": "nostalgia_id",
    "REC": "dancerush_profile_id",  # DRS uses "drs_id" not matching the pattern
    "JDZ": "iidx_id",
    "KDZ": "iidx_id",
}


def get_target_table(game_id):
    target_table = {
        "LDJ": "iidx_profile",
        "MDX": "ddr_profile",
        "KFC": "sdvx_profile",
        "M32": "gitadora_profile",
        "PAN": "nostalgia_profile",
        "REC": "dancerush_profile",
        "JDZ": "iidx_profile",
        "KDZ": "iidx_profile",
    }
    return target_table[game_id]


def get_id_field(game_id):
    """Get the ID field name for a game, e.g. 'iidx_id', 'ddr_id'."""
    if game_id in GAME_ID_MAP:
        return GAME_ID_MAP[game_id]
    return get_target_table(game_id).replace("_profile", "_id")


def get_card_pin(cardid):
    """Get the unified PIN for a card from the paseli table."""
    return paseli_get_pin(cardid)


def set_card_pin(cardid, pin):
    """Set the unified PIN for a card in the paseli table."""
    paseli_set_pin(cardid, pin)


def get_or_create_game_id(game_id, cid):
    """Get the game-specific ID for a card, or generate a new one.
    Looks across all game_version rows for the same card."""
    target_table = get_target_table(game_id)
    id_field = get_id_field(game_id)

    # Find any existing row for this card to get the game ID
    table = get_db().table(target_table)
    existing = table.get(where("card") == cid)
    if existing and existing.get(id_field, 0) != 0:
        return existing[id_field]

    # Generate new ID
    return randint(10000000, 99999999)


def get_profile(game_id, game_version, cid):
    """Get the profile row for a specific (card, game_version). Returns a dict.
    If no profile exists, returns a minimal dict without saving to DB —
    the game client will populate and save it."""
    target_table = get_target_table(game_id)
    id_field = get_id_field(game_id)
    table = get_db().table(target_table)

    profile = table.get(
        (where("card") == cid) & (where("game_version") == game_version)
    )

    if profile is None:
        game_id_val = get_or_create_game_id(game_id, cid)
        profile = Document({"card": cid, "game_version": game_version, id_field: game_id_val})
        # Give JSON columns proper empty containers so iteration works
        if not table._is_legacy:
            for key, typedef in table.schema.items():
                if "JSON" in typedef.upper():
                    profile[key] = {} if "LIST" not in typedef.upper() else []

    return profile


def create_profile(game_id, game_version, cid, pin):
    """Register a card: store PIN in paseli. Profile created by reg."""
    set_card_pin(cid, pin)


@router.post("/{gameinfo}/cardmng/authpass")
async def cardmng_authpass(request: Request):
    request_info = await core_process_request(request)

    cid = request_info["root"][0].attrib["refid"]
    passwd = request_info["root"][0].attrib["pass"]

    stored_pin = get_card_pin(cid)
    if stored_pin is None or passwd != stored_pin:
        status = 116
    else:
        status = 0

    response = E.response(E.authpass(status=status))

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)


@router.post("/{gameinfo}/cardmng/bindmodel")
async def cardmng_bindmodel(request: Request):
    request_info = await core_process_request(request)

    response = E.response(E.bindmodel(dataid=1))

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)


@router.post("/{gameinfo}/cardmng/getrefid")
async def cardmng_getrefid(request: Request):
    request_info = await core_process_request(request)

    cid = request_info["root"][0].attrib["cardid"]
    passwd = request_info["root"][0].attrib["passwd"]

    create_profile(request_info["model"], request_info["game_version"], cid, passwd)

    response = E.response(
        E.getrefid(
            dataid=cid,
            refid=cid,
        )
    )

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)


@router.post("/{gameinfo}/cardmng/inquire")
async def cardmng_inquire(request: Request):
    request_info = await core_process_request(request)

    cid = request_info["root"][0].attrib["cardid"]
    game_version = request_info["game_version"]
    target_table = get_target_table(request_info["model"])

    # Check central card registry first
    if get_card_pin(cid) is None:
        # Card never registered anywhere
        binded = 0
        newflag = 1
        status = 112
    else:
        # Card is known; check if this game has a profile
        profile = get_db().table(target_table).get(
            (where("card") == cid) & (where("game_version") == game_version)
        )
        if profile:
            binded = 1
            newflag = 0
        else:
            binded = 0
            newflag = 1
        status = 0

    response = E.response(
        E.inquire(
            dataid=cid,
            ecflag=1,
            expired=0,
            binded=binded,
            newflag=newflag,
            refid=cid,
            status=status,
        )
    )

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)
