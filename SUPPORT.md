# Getting help

## Before you ask

Most questions are answered by the documentation for the package you are using:

- [pysnmp](https://pysnmp.github.io/pysnmp/) -- the engine: managers, agents,
  proxies, notification receivers.
- [pysmi](https://pysnmp.github.io/pysmi/) -- compiling ASN.1 MIB sources.
- [pyasn1](https://pysnmp.github.io/pyasn1/) -- ASN.1 types and codecs.

Each repository also has an `examples/` directory of runnable scripts, which is
usually the fastest route to a working program.

If you need a MIB module, look in the distribution at
[pysnmp.github.io/mibs/](https://pysnmp.github.io/mibs/) before hunting for it
elsewhere -- it is served over HTTPS, shipped as an archive and published as
OCI images.

## Asking a question

Open an issue on the repository the question is about, using the **Question**
template. Include:

- what you are trying to do, and what happened instead;
- the versions: `pip show pysnmplib pysnmp-pysmi pysnmp-pyasn1` and your Python
  version;
- the smallest script that shows the problem, as text rather than a screenshot;
- for anything on the wire, what the other end is -- a device model, or
  `net-snmp`, or another pysnmp process.

For a device that answers some requests and not others, a packet capture is
worth more than any description of it -- redacted first. An issue is public and
SNMPv1 and SNMPv2c carry the community string in cleartext, so an unedited
capture of either publishes a password. Strip community strings, USM
passphrases and addresses, and prefer decoded output to raw bytes.

## What we can and cannot help with

This is volunteer-maintained. Bug reports with a reproduction get looked at.
Questions get answered when someone has time.

What is out of scope here:

- Configuring a particular vendor's SNMP agent. That is the vendor's
  documentation.
- Interpreting what a MIB object means for a given device. The MIB's own
  DESCRIPTION clauses and the vendor are the authority, not us.
- The `pysnmp` distribution on PyPI published by other maintainers, or
  [docs.lextudio.com](https://docs.lextudio.com/snmp/). Those are a different
  fork of the same origin. The packages maintained here are `pysnmplib`,
  `pysnmp-pysmi` and `pysnmp-pyasn1`.

## Commercial support

None is offered by this organization.
