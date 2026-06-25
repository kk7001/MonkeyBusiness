from fastapi import APIRouter, Request, Response
from random import randint
from core_database import Query, where, Document

from core_common import core_process_request, core_prepare_response, E
from core_database import get_db
from modules.core.paseli import get_balance as paseli_get_balance, add_spend as paseli_add_spend

import config

router = APIRouter(prefix="/core", tags=["cardmng"])


GAME_ID_MAP = {
    "LDJ": "iidx_id",
    "MDX": "ddr_id",
    "KFC": "sdvx_id",
    "M32": "gitadora_id",
    "PAN": "nostalgia_id",
    "REC": "dancerush_profile_id",
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
    if game_id in GAME_ID_MAP:
        return GAME_ID_MAP[game_id]
    return get_target_table(game_id).replace("_profile", "_id")


# =============================================================================
# Card map table — maps physical card IDs to user account UIDs
# =============================================================================

def _ensure_card_map():
    conn = get_db().conn
    conn.execute(
        "CREATE TABLE IF NOT EXISTS card_map ("
        "  card_id TEXT PRIMARY KEY,"
        "  uid     INTEGER NOT NULL,"
        "  pin     TEXT"
        ")"
    )
    conn.commit()


def resolve_card(card_id):
    """Look up (uid, pin) for a physical card. Creates new UID if card is new."""
    _ensure_card_map()
    conn = get_db().conn
    row = conn.execute(
        "SELECT uid, pin FROM card_map WHERE card_id = ?", (card_id,)
    ).fetchone()
    if row:
        return row["uid"], row.get("pin")
    # New card: create UID and entry
    uid = randint(10000000, 99999999)
    conn.execute(
        "INSERT INTO card_map (card_id, uid) VALUES (?, ?)", (card_id, uid)
    )
    conn.commit()
    return uid, None


def get_card_pin(card_id):
    """Get PIN for a physical card."""
    _ensure_card_map()
    conn = get_db().conn
    row = conn.execute(
        "SELECT pin FROM card_map WHERE card_id = ?", (card_id,)
    ).fetchone()
    return row["pin"] if row else None


def set_card_pin(card_id, pin):
    """Set PIN for a physical card."""
    _ensure_card_map()
    conn = get_db().conn
    conn.execute(
        "UPDATE card_map SET pin = ? WHERE card_id = ?", (pin, card_id)
    )
    conn.commit()


# =============================================================================
# Profile helpers
# =============================================================================

def get_or_create_game_id(game_id, uid):
    target_table = get_target_table(game_id)
    id_field = get_id_field(game_id)
    table = get_db().table(target_table)
    existing = table.get(where("uid") == uid)
    if existing and existing.get(id_field, 0) != 0:
        return existing[id_field]
    return randint(10000000, 99999999)


def get_profile(game_id, game_version, uid):
    target_table = get_target_table(game_id)
    id_field = get_id_field(game_id)
    table = get_db().table(target_table)

    profile = table.get(
        (where("uid") == uid) & (where("game_version") == game_version)
    )

    if profile is None:
        game_id_val = get_or_create_game_id(game_id, uid)
        profile = Document({"uid": uid, "game_version": game_version, id_field: game_id_val})
        # Give JSON columns proper empty containers
        if not table._is_legacy:
            for key, typedef in table.schema.items():
                if "JSON" in typedef.upper():
                    profile[key] = {} if "LIST" not in typedef.upper() else []

    return profile


# =============================================================================
# Endpoints
# =============================================================================

@router.post("/{gameinfo}/cardmng/authpass")
async def cardmng_authpass(request: Request):
    request_info = await core_process_request(request)

    card_id = request_info["root"][0].attrib["refid"]
    passwd = request_info["root"][0].attrib["pass"]

    stored_pin = get_card_pin(card_id)
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

    card_id = request_info["root"][0].attrib["cardid"]
    passwd = request_info["root"][0].attrib["passwd"]

    # Resolve card and store PIN
    uid, _ = resolve_card(card_id)
    set_card_pin(card_id, passwd)

    response = E.response(E.getrefid(dataid=card_id, refid=card_id))
    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)


@router.post("/{gameinfo}/cardmng/inquire")
async def cardmng_inquire(request: Request):
    request_info = await core_process_request(request)

    card_id = request_info["root"][0].attrib["cardid"]
    game_version = request_info["game_version"]
    target_table = get_target_table(request_info["model"])

    # Resolve card to uid
    uid, _ = resolve_card(card_id)

    # Check if profile exists for this (uid, game_version)
    profile = get_db().table(target_table).get(
        (where("uid") == uid) & (where("game_version") == game_version)
    )

    if profile:
        binded = 1
        newflag = 0
        status = 0
    else:
        binded = 0
        newflag = 1
        status = 0

    response = E.response(
        E.inquire(
            dataid=card_id, ecflag=1, expired=0,
            binded=binded, newflag=newflag, refid=card_id, status=status,
        )
    )
    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)
