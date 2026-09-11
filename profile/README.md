# pysnmp

**Pure-Python SNMP, from the wire up. Brewing free software for the greater good.**

This organization maintains the Python SNMP stack: an SNMP engine, the MIB
compiler that feeds it, the ASN.1 codec underneath both, and the MIB archive
they read from. No C extensions, no Net-SNMP bindings -- Python all the way
down, on Python 3.10 and later.

<!-- BEGIN PROJECTS -->
| Project | Install | Documentation | What it is |
| --- | --- | --- | --- |
| [pysnmp](https://github.com/pysnmp/pysnmp) | `pip install --pre pysnmplib` | [docs](https://pysnmp.github.io/pysnmp/) | SNMP v1/v2c/v3 engine -- manager, agent and proxy, asyncio throughout. |
| [pysmi](https://github.com/pysnmp/pysmi) | `pip install pysnmp-pysmi` | [docs](https://pysnmp.github.io/pysmi/) | MIB compiler: ASN.1 SMIv1/SMIv2 sources into pysnmp modules or JSON. |
| [pyasn1](https://github.com/pysnmp/pyasn1) | `pip install pysnmp-pyasn1` | [docs](https://pysnmp.github.io/pyasn1/) | ASN.1 types and BER/CER/DER codecs -- what the other two are built on. |
| [mibs](https://github.com/pysnmp/mibs) | -- | [docs](https://pysnmp.github.io/mibs/asn1/) | The MIB archive pysmi and pysnmp fetch from when a module is not on disk. |
<!-- END PROJECTS -->

## Start here

```console
$ pip install --pre pysnmplib
```

`--pre` is not decoration. pysnmp 6.0 is in release candidate and is the line
being maintained; a plain `pip install pysnmplib` resolves 5.0.24, whose
`pysnmp-pyasn1` requirement predates the current releases of that package and
which fails to import against the one it pulls in. Drop the flag once 6.0 is
generally available.

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

An SNMP engine speaks a binary protocol about objects named in MIB modules, so
there are three layers and they are three repositories:

- **pyasn1** encodes and decodes. BER on the wire, CER and DER where a
  signature has to be reproducible.
- **pysmi** reads ASN.1 MIB sources -- SMIv1, SMIv2 and the dialects real
  vendors ship -- and renders them as pysnmp modules or JSON.
- **pysnmp** is the engine: message processing, USM security, VACM access
  control, the transport dispatcher, and the high-level API above all of it.
- **mibs** is the archive the other two fall back to when a MIB module is not
  on disk, served over HTTPS at
  [pysnmp.github.io/mibs/asn1/](https://pysnmp.github.io/mibs/asn1/).

pysnmp ships the standard modules its engine resolves at start-up, so an
engine starts with neither pysmi nor the archive present. Compiling vendor
MIBs at run time is the extra: `pip install --pre 'pysnmplib[compile]'`.

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
