import pytest

from cashu.core.b_dhke import hash_to_curve, step1_alice, step2_bob, step3_alice
from cashu.core.secp import PrivateKey, PublicKey


def test_hash_to_curve():
    result = hash_to_curve(
        bytes.fromhex(
            "0000000000000000000000000000000000000000000000000000000000000000"
        )
    )
    assert (
        result.serialize().hex()
        == "0266687aadf862bd776c8fc18b8e9f8e20089714856ee233b3902a591d0d5f2925"
    )

    result = hash_to_curve(
        bytes.fromhex(
            "0000000000000000000000000000000000000000000000000000000000000001"
        )
    )
    assert (
        result.serialize().hex()
        == "02ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5"
    )


def test_hash_to_curve_iteration():
    """This input causes multiple rounds of the hash_to_curve algorithm."""
    result = hash_to_curve(
        bytes.fromhex(
            "0000000000000000000000000000000000000000000000000000000000000002"
        )
    )
    assert (
        result.serialize().hex()
        == "02076c988b353fcbb748178ecb286bc9d0b4acf474d4ba31ba62334e46c97c416a"
    )


def test_step1():
    """"""
    B_, blinding_factor = step1_alice(
        "test_message", blinding_factor=b"00000000000000000000000000000001"  # 32 bytes
    )

    assert (
        B_.serialize().hex()
        == "0243379106c73dfc635cd1422f406e83fbfa25be83bb3620aefc08f2b89d02d777"
    )
    assert blinding_factor.private_key == b"00000000000000000000000000000001"


def test_step2():
    B_, _ = step1_alice(
        "test_message",
        blinding_factor=bytes.fromhex(
            "0000000000000000000000000000000000000000000000000000000000000001"
        ),  # 32 bytes
    )
    a = PrivateKey(
        privkey=bytes.fromhex(
            "0000000000000000000000000000000000000000000000000000000000000001"
        ),
        raw=True,
    )
    C_ = B_.mult(a)
    assert (
        C_.serialize().hex()
        == "02a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2"
    )


def test_step3():
    # C = C_ - A.mult(r)
    C_ = PublicKey(
        bytes.fromhex(
            "02b15f14ae9259c101cdbc437e8877b1ca5d4af3a0c0684866b38d8c8d0b6f6374"
        ),
        raw=True,
    )
    r = PrivateKey(
        privkey=bytes.fromhex(
            "0000000000000000000000000000000000000000000000000000000000000001"
        )
    )

    A = PublicKey(
        pubkey=b"\x02"
        + bytes.fromhex(
            "0000000000000000000000000000000000000000000000000000000000000001",
        ),
        raw=True,
    )
    C = step3_alice(C_, r, A)

    assert (
        C.serialize().hex()
        == "03398f7153b381ce54d57962a5e03ce0a4f3b79755e882c972b788e8488e59b0c9"
    )
