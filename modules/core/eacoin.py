import config

from fastapi import APIRouter, Request, Response
from core_database import where

from core_common import core_process_request, core_prepare_response, E
from core_database import get_db
from modules.core.paseli import get_balance, add_spend

router = APIRouter(prefix="/core", tags=["eacoin"])

sessid = 0
payments = {}


@router.post("/{gameinfo}/eacoin/checkin")
async def eacoin_checkin(request: Request):
    request_info = await core_process_request(request)
    pcbid = request_info["root"].attrib["srcid"]
    cardid = request_info["root"][0].find("cardid").text

    op = get_db().table("shop").get(where("pcbid") == pcbid)
    op = {} if op is None else op

    bal = get_balance(cardid)

    global sessid
    sessid += 1
    payments[sessid] = cardid

    response = E.response(
        E.eacoin(
            E.sequence(1, __type="s16"),
            E.acstatus(1, __type="u8"),
            E.acid(1, __type="str"),
            E.acname(op.get("opname", config.arcade), __type="str"),
            E.balance(bal, __type="s32"),
            E.sessid(sessid, __type="str"),
            E.inshopcharge(1, __type="u8"),
        )
    )

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)


@router.post("/{gameinfo}/eacoin/checkout")
async def eacoin_checkout(request: Request):
    request_info = await core_process_request(request)

    response = E.response(E.eacoin())

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)


@router.post("/{gameinfo}/eacoin/consume")
async def eacoin_consume(request: Request):
    request_info = await core_process_request(request)
    sessid = int(request_info["root"][0].find("sessid").text)
    payment = int(request_info["root"][0].find("payment").text)

    cardid = payments.get(sessid, None)

    # fallback if server is restarted mid-round for IIDX movie or gacha purchases
    if cardid is None:
        response = E.response(
            E.eacoin(
                E.acstatus(0, __type="u8"),
                E.autocharge(0, __type="u8"),
                E.balance(config.paseli, __type="s32"),
            )
        )

        response_body, response_headers = await core_prepare_response(request, response)
        return Response(content=response_body, headers=response_headers)

    new_balance = add_spend(cardid, payment)

    response = E.response(
        E.eacoin(
            E.acstatus(0, __type="u8"),
            E.autocharge(0, __type="u8"),
            E.balance(new_balance, __type="s32"),
        )
    )

    # del payments[sessid]

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)


@router.post("/{gameinfo}/eacoin/getbalance")
async def eacoin_getbalance(request: Request):
    request_info = await core_process_request(request)

    response = E.response(
        E.eacoin(
            E.acstatus(0, __type="u8"),
            E.balance(config.paseli, __type="s32"),
        )
    )

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)
