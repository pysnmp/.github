# pysnmp

**Pure-Python SNMP. Brewing free software for the greater good.**

An engine that speaks SNMP v1, v2c and v3, and a MIB distribution that lets it
talk about managed objects by name instead of by number. No C extensions and
no Net-SNMP bindings -- Python all the way down, on Python 3.10 and later.

**pysnmp** and **mibs** are what you use. **pysmi** and **pyasn1** are the
layers underneath; pysnmp reaches them for you.

<!-- BEGIN PROJECTS -->
| Project | Install | Documentation | What it is |
| --- | --- | --- | --- |
| [pysnmp](https://github.com/pysnmp/pysnmp) | `pip install pysnmplib` | [docs](https://pysnmp.github.io/pysnmp/) | The engine. SNMP v1, v2c and v3 as manager, agent or proxy, on asyncio. |
| [mibs](https://github.com/pysnmp/mibs) | live over HTTPS, or installed locally | [docs](https://pysnmp.github.io/mibs/asn1/) | The MIB distribution -- what lets an engine say ifOperStatus rather than .1.8.1. |
| [pysmi](https://github.com/pysnmp/pysmi) | `pip install pysnmp-pysmi` | [docs](https://pysnmp.github.io/pysmi/) | The MIB compiler. ASN.1 sources into pysnmp modules or JSON; comes with the compile extra. |
| [pyasn1](https://github.com/pysnmp/pyasn1) | `pip install pysnmp-pyasn1` | [docs](https://pysnmp.github.io/pyasn1/) | The codec. ASN.1 types with BER, CER and DER, underneath both of the above. |
<!-- END PROJECTS -->

## Start here

```console
$ pip install 'pysnmplib[compile]'
```

The `compile` extra pulls in pysmi, the MIB compiler. Without it pysnmp still
speaks SNMP -- it ships the standard modules an engine resolves at start-up --
but it cannot read a MIB it does not already have, and reading those is most of
what makes SNMP legible.

```python
import asyncio

from pysnmp.hlapi.asyncio import *


async def run():
    snmpEngine = SnmpEngine()
    errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
        snmpEngine,
        CommunityData("public", mpModel=0),
        UdpTransportTarget(("localhost", 161)),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
    )

    for varBind in varBinds:
        print(" = ".join(x.prettyPrint() for x in varBind))

    snmpEngine.transportDispatcher.closeDispatcher()


asyncio.run(run())
```

More of these, for managers, agents, proxies and notification receivers, are in
[the examples directory](https://github.com/pysnmp/pysnmp/tree/main/examples)
and on the [documentation site](https://pysnmp.github.io/pysnmp/).

## How the pieces fit

**pysnmp** is the engine: message processing for v1, v2c and v3, USM
authentication and privacy, VACM access control, the transport dispatcher, and
the high-level API above all of it.

**mibs** supplies the module definitions. It is a distribution, though not one
pip resolves: use it live over HTTPS, or install it locally from the archive or
an OCI image. It is what turns `.1.3.6.1.2.1.2.2.1.8.1 = 2` into
`IF-MIB::ifOperStatus.1 = down`. Optional: an engine starts without it, on the
standard modules pysnmp ships.

**pysmi** compiles the ASN.1 sources those modules are written in. pysnmp
drives it; you call it directly, as `mibdump`, to compile MIBs outside an
engine.

**pyasn1** encodes and decodes -- BER on the wire, CER and DER where a
representation has to be reproducible byte for byte. Normal use never reaches
it by hand.

[Resolving a name and translating a trap](https://pysnmp.github.io/mibs/), end
to end, are on the site.

## How we work

The toolchain is shared, so moving between repositories costs nothing:

- [uv](https://docs.astral.sh/uv/) for environments, with a committed
  lockfile; `uv sync --locked` reproduces exactly what CI runs.
- [ruff](https://docs.astral.sh/ruff/) for lint and formatting against one
  shared rule set, enforced by pre-commit and again in CI. Where there is a
  package to type-check, mypy as well; where there is behaviour to test,
  pytest.
- [Conventional Commits](https://www.conventionalcommits.org/), checked on
  every pull request everywhere. In the three that publish a package they are
  also load-bearing: semantic-release computes the version and the release
  notes from them.
- In those three, `main` carries the released line and `next` is where work
  integrates; a release candidate is cut from `next`, a GA from `main`. This
  repository and the site publish nothing, so they have only `main`.

[CONTRIBUTING.md](https://github.com/pysnmp/.github/blob/main/CONTRIBUTING.md)
has the details, and applies to every repository here.

## Security

Report a vulnerability privately through
[GitHub Security Advisories](https://github.com/pysnmp/pysnmp/security/advisories/new),
not in a public issue. [SECURITY.md](https://github.com/pysnmp/.github/blob/main/SECURITY.md)
says what is supported and what to expect.

SNMPv1 and SNMPv2c have no security by design, and SNMPv3 still specifies MD5,
SHA-1 and DES. pysnmp implements them because the protocol does and warns where
one is configured; that is not a vulnerability report.

## History

These are forks of [Ilya Etingof's](https://github.com/etingof) work, carried
on after he [passed away on 10 August 2022](https://lists.openstack.org/pipermail/openstack-discuss/2022-August/030062.html).
The PySNMP project was originally sponsored by a [PSF](https://www.python.org/psf/)
grant. Everything here stays under the 2-clause BSD license it always had.
